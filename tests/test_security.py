
import os
import sys
import time
import importlib

import pytest


@pytest.fixture(scope="module")
def test_app(tmp_path_factory):
    # Use a separate database for automated testing.
    test_directory = tmp_path_factory.mktemp("security_tests")

    import models

    original_database = models.DATABASE
    models.DATABASE = test_directory / "test_dashboard.db"

    # Flask requires a SECRET_KEY from the environment.
    # The CI workflow supplies its own GitHub Actions secret.
    try:
        sys.modules.pop("app", None)
        application_module = importlib.import_module("app")
        application = application_module.app
        application.config["TESTING"] = True

        # Create fictional users in the temporary database.
        models.create_user(
            "testassociate",
            "TestingOnlyPass123!",
            "team_member",
        )
        models.create_user(
            "testmanager",
            "TestingOnlyPass123!",
            "manager",
        )
        models.create_user(
            "testadmin",
            "TestingOnlyPass123!",
            "admin",
        )

        yield application

    finally:
        models.DATABASE = original_database


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def log_in_as(client, username):
    import models

    with models.get_connection() as connection:
        user = connection.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,),
        ).fetchone()

    assert user is not None

    with client.session_transaction() as session:
        session["user_id"] = user["id"]
        session["last_activity"] = time.time()


def test_dashboard_requires_login(client):
    response = client.get("/dashboard")

    assert response.status_code == 302


def test_team_member_cannot_manage_records(client):
    log_in_as(client, "testassociate")

    response = client.get("/manage-records")

    assert response.status_code == 403


def test_manager_can_manage_records(client):
    log_in_as(client, "testmanager")

    response = client.get("/manage-records")

    assert response.status_code == 200


def test_manager_cannot_access_admin(client):
    log_in_as(client, "testmanager")

    response = client.get("/admin")

    assert response.status_code == 403


def test_admin_can_access_admin_page(client):
    log_in_as(client, "testadmin")

    response = client.get("/admin")

    assert response.status_code == 200