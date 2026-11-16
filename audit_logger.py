
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from logging.handlers import RotatingFileHandler

LOG_DIRECTORY = Path(__file__).resolve().parent / "logs"
LOG_DIRECTORY.mkdir(exist_ok=True)

LOG_FILE = LOG_DIRECTORY / "security_audit.log"

logger = logging.getLogger("security_audit")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)


ALLOWED_EVENTS = {
    "authentication",
    "authorization_failure",
    "validation_failure",
    "record_create",
    "record_update",
    "record_delete",
    "application_error",
}

ALLOWED_OUTCOMES = {
    "success",
    "failure",
    "denied",
}


def log_security_event(event_type, outcome, role="unknown"):
    """
    Record an approved security event without logging
    passwords, session tokens, or submitted form data.
    """
    if event_type not in ALLOWED_EVENTS:
        raise ValueError("Invalid security event type")

    if outcome not in ALLOWED_OUTCOMES:
        raise ValueError("Invalid event outcome")

    if role not in {"admin", "manager", "team_member", "unknown"}:
        role = "unknown"

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "outcome": outcome,
        "role": role,
    }

    logger.info(json.dumps(event))