
# Milestone 4: Secure Authentication and Authorization

## Project
Secure Delivery Defect and Station Performance Dashboard

## Current Version
Milestone 4 development version

## Authentication Design
- Python Flask handles application authentication.
- SQLite stores user accounts and assigned roles.
- Werkzeug hashes passwords before storage.
- Valid credentials establish an authenticated Flask session.
- Invalid credentials are rejected.
- Logout clears the authenticated session.
- Flask-Limiter restricts repeated login requests.
- Flask-WTF provides CSRF protection.

## Role-Based Authorization
Three roles are implemented:
- Admin: Dashboard, Manage Records, Admin Panel,
  and Create User Account.
- Manager: Dashboard and Manage Records.
- Team Member: Dashboard only.

Backend decorators verify user roles against SQLite.

## Session Security
- HTTPOnly session cookies.
- SameSite=Lax session cookies.
- Session clearing during login and logout.
- Automatic expiration after inactivity.
- One-minute timeout currently configured
  for Milestone 4 demonstration.
- HTTPS and Secure cookies required for deployment.

## Security Threat Mitigation
- Spoofing: Password hashing, authentication,
  and login rate limiting.
- Elevation of Privilege: Backend role checks
  and restricted administrator routes.
- Information Disclosure: Protected routes,
  generic error messages, and disabled debug mode.

## Remaining Security Work
- Restore the intended 15-minute session timeout
  after the demonstration.
- Add persistent rate-limit storage.
- Configure HTTPS and Secure cookies.
- Add comprehensive audit logging.
- Expand automated security tests.
- Review account lifecycle and password-reset controls.