
import json
import logging

import pytest

import models
from audit_logger import log_security_event, logger


@pytest.fixture
def audit_test_environment(tmp_path, monkeypatch):
    # Use a temporary database, not dashboard.db.
    test_database = tmp_path / "audit_test.db"
    monkeypatch.setattr(models, "DATABASE", test_database)

    models.initialize_database()
    models.initialize_delivery_records()

    # Capture audit logs in a temporary file.
    test_log = tmp_path / "audit_test.log"
    handler = logging.FileHandler(test_log, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(message)s"))

    monkeypatch.setattr(logger, "handlers", [handler])

    try:
        models.create_user(
            "auditmanager",
            "TestingOnlyPass123!",
            "manager",
        )

        with models.get_connection() as connection:
            user = connection.execute(
                "SELECT id FROM users WHERE username = ?",
                ("auditmanager",),
            ).fetchone()

        models.create_delivery_record(
            "AUDIT101",
            "A",
            2,
            "2026-11-15",
            user["id"],
        )

        with models.get_connection() as connection:
            record = connection.execute(
                "SELECT id FROM delivery_records WHERE route_id = ?",
                ("AUDIT101",),
            ).fetchone()

        yield record["id"], test_log

    finally:
        handler.flush()
        handler.close()


def test_record_update_audit(audit_test_environment):
    record_id, test_log = audit_test_environment

    # Update a fictional record in the test database.
    with models.get_connection() as connection:
        result = connection.execute(
            """
            UPDATE delivery_records
            SET defect_count = ?
            WHERE id = ?
            """,
            (4, record_id),
        )
        assert result.rowcount == 1

    # Log the update after the database transaction succeeds.
    log_security_event(
        "record_update",
        "success",
        "manager",
    )

    with models.get_connection() as connection:
        updated = connection.execute(
            "SELECT defect_count FROM delivery_records WHERE id = ?",
            (record_id,),
        ).fetchone()

    assert updated["defect_count"] == 4

    events = [
        json.loads(line)
        for line in test_log.read_text().splitlines()
    ]

    assert any(
        event["event_type"] == "record_update"
        and event["outcome"] == "success"
        and event["role"] == "manager"
        for event in events
    )

    print("Record update: SUCCESS")
    print("Audit event: record_update / success")


def test_record_delete_audit(audit_test_environment):
    record_id, test_log = audit_test_environment

    # Delete a fictional record from the test database.
    with models.get_connection() as connection:
        result = connection.execute(
            "DELETE FROM delivery_records WHERE id = ?",
            (record_id,),
        )
        assert result.rowcount == 1

    # Log the deletion after the transaction succeeds.
    log_security_event(
        "record_delete",
        "success",
        "manager",
    )

    with models.get_connection() as connection:
        deleted = connection.execute(
            "SELECT id FROM delivery_records WHERE id = ?",
            (record_id,),
        ).fetchone()

    assert deleted is None

    events = [
        json.loads(line)
        for line in test_log.read_text().splitlines()
    ]

    assert any(
        event["event_type"] == "record_delete"
        and event["outcome"] == "success"
        and event["role"] == "manager"
        for event in events
    )

    print("Record deletion: SUCCESS")
    print("Audit event: record_delete / success")