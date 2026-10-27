import os
import time
from datetime import date
from functools import wraps
import sqlite3

from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    abort,
)
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from models import (
    initialize_database,
    initialize_delivery_records,
    verify_user,
    create_user,
    create_delivery_record,
    get_delivery_records,
    get_user_by_id,
)

# Load configuration
load_dotenv()

app = Flask(__name__)

secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY must be configured in .env.")

app.secret_key = secret_key

# Cookie security for local HTTP development
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,
)

# CSRF protection for POST forms
csrf = CSRFProtect(app)

# SR-07: Limit login requests
# Memory storage is suitable for this local demonstration.
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

# SR-08: Inactivity timeout in seconds
SESSION_TIMEOUT = 1 * 60

initialize_database()
initialize_delivery_records()


@app.before_request
def check_session_timeout():
    if "user_id" not in session:
        return None

    now = time.time()
    last_activity = session.get("last_activity")

    if (
        last_activity is None
        or now - last_activity > SESSION_TIMEOUT
    ):
        session.clear()
        return redirect(url_for("home"))

    session["last_activity"] = now
    return None


# SR-01: Require authentication
def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")

        if user_id is None:
            return redirect(url_for("home"))

        user = get_user_by_id(user_id)

        if user is None:
            session.clear()
            return redirect(url_for("home"))

        session["username"] = user["username"]
        session["role"] = user["role"]

        return function(*args, **kwargs)

    return wrapper


# SR-03: Role-based access control
def role_required(*allowed_roles):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user_id = session.get("user_id")

            if user_id is None:
                return redirect(url_for("home"))

            user = get_user_by_id(user_id)

            if user is None:
                session.clear()
                return redirect(url_for("home"))

            if user["role"] not in allowed_roles:
                abort(403)

            return function(*args, **kwargs)

        return wrapper

    return decorator


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return render_template("login.html")


# SR-07: Five login attempts per 15 minutes per IP
@app.route("/login", methods=["POST"])
@limiter.limit("5 per 15 minutes")
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if (
        not username
        or not password
        or len(username) > 50
    ):
        return render_template(
            "login.html",
            error="Invalid username or password.",
        ), 400

    user = verify_user(username, password)

    if user is None:
        return render_template(
            "login.html",
            error="Invalid username or password.",
        ), 401

    session.clear()

    session["user_id"] = user["id"]
    session["username"] = user["username"]
    session["role"] = user["role"]
    session["last_activity"] = time.time()

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session["role"],
        records=get_delivery_records(),
    )


@app.route("/manage-records", methods=["GET", "POST"])
@login_required
@role_required("manager", "admin")
def manage_records():
    if request.method == "POST":
        route_id = request.form.get(
            "route_id", ""
        ).strip()

        zone = request.form.get(
            "zone", ""
        ).strip()

        defect_input = request.form.get(
            "defect_count", ""
        ).strip()

        route_date = request.form.get(
            "route_date", ""
        ).strip()

        # SR-04: Server-side input validation
        if not (
            3 <= len(route_id) <= 20
            and route_id.isalnum()
        ):
            error = (
                "Route ID must contain "
                "3-20 letters or numbers."
            )

        elif zone not in {"A", "B", "C", "D"}:
            error = "Please select a valid zone."

        elif not defect_input.isdecimal():
            error = "Defect count must be a whole number."

        elif not 0 <= int(defect_input) <= 1000:
            error = (
                "Defect count must be "
                "between 0 and 1000."
            )

        else:
            try:
                parsed_date = date.fromisoformat(
                    route_date
                )

                if parsed_date > date.today():
                    raise ValueError()

            except ValueError:
                error = (
                    "Enter a valid date "
                    "that is not in the future."
                )

            else:
                create_delivery_record(
                    route_id,
                    zone,
                    int(defect_input),
                    parsed_date.isoformat(),
                    session["user_id"],
                )

                return redirect(url_for("dashboard"))

        return render_template(
            "manage_records.html",
            error=error,
        ), 400

    return render_template("manage_records.html")


@app.route("/admin")
@login_required
@role_required("admin")
def admin_panel():
    return """
    <h1>Administrator Panel</h1>
    <p>Access granted: Administrator only.</p>
    <a href="/dashboard">Return to Dashboard</a>
    """

# Milestone 4: Administrator-created user accounts
@app.route("/admin/create-user", methods=["GET", "POST"])
@login_required
@role_required("admin")
def admin_create_user():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        try:
            create_user(username, password, role)
        except ValueError:
            return render_template(
                "create_user.html",
                error="Check the username, password, and role."
            ), 400
        except sqlite3.IntegrityError:
            return render_template(
                "create_user.html",
                error="That username is unavailable."
            ), 400

        return render_template(
            "create_user.html",
            success="User account created successfully."
        )

    return render_template("create_user.html")

# SR-09: Safe error messages
@app.errorhandler(403)
def forbidden(error):
    return """
    <h1>403 - Access Denied</h1>
    <p>You do not have permission to access this page.</p>
    <a href="/dashboard">Return to Dashboard</a>
    """, 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "error.html",
        message="The requested page could not be found.",
    ), 404


@app.errorhandler(429)
def too_many_requests(error):
    return (
        "<h1>Too Many Requests</h1>"
        "<p>Too many login attempts. "
        "Please try again later.</p>",
        429,
    )


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error(
        "An internal server error occurred.",
        exc_info=True,
    )

    return render_template(
        "error.html",
        message=(
            "Something went wrong. "
            "Please try again later."
        ),
    ), 500


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False)