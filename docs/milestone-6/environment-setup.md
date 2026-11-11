
# Milestone 6: Environment Configuration Guide

## Project
Secure Delivery Defect and Station Performance Dashboard

## Environment

This application uses Python, Flask, and SQLite.
Development and testing are performed locally.
GitHub Actions runs automated security checks.

## Required Configuration

### SECRET_KEY
Purpose:
Protects Flask session integrity.

Location:
Local .env file or an approved environment
secret store.

Example:
SECRET_KEY=<generated-random-value>

The example is a placeholder, not a real key.

### CI_FLASK_SECRET_KEY
Purpose:
Provides a separate secret for automated tests.

Location:
GitHub repository settings under
Secrets and variables > Actions.

Value:
A separately generated random secret.

## Access Control

Only authorized repository administrators should
manage GitHub Actions secrets. Access to the
local .env file should be limited to the developer
or authorized deployment personnel.

## Local Setup Instructions

1. Clone the private GitHub repository.
2. Create and activate a Python virtual environment.
3. Install dependencies using:
   pip install -r requirements.txt
4. Create a local .env file.
5. Generate a unique random SECRET_KEY.
6. Add the key to .env without sharing its value.
7. Run the application with:
   python app.py
8. Confirm the application opens locally.
9. Run:
   python -m pytest -q

## GitHub Actions Setup

1. Open the repository Settings.
2. Select Secrets and variables > Actions.
3. Create a repository secret named
   CI_FLASK_SECRET_KEY.
4. Enter a newly generated secret value.
5. Save the secret.
6. Run Secure Dashboard CI.
7. Verify that tests and security checks pass.

## Preventing Secret Exposure

- Never commit .env files.
- Never commit local SQLite database files.
- Keep actual secret values out of screenshots.
- Do not print secret values in CI logs.
- Review staged changes before committing.
- If a secret is exposed, revoke or rotate it,
  check the repository history, and investigate
  whether it was used.

## Verification

The .gitignore file excludes .env and *.db files.

The command:

git ls-files .env dashboard.db

returned no tracked files during Milestone 6.

The GitHub Actions workflow also completed
successfully using a separately configured
repository secret.

## Deployment Note

The current application uses local HTTP development
settings. Before production deployment, HTTPS,
secure session cookies, production server configuration,
and appropriate database storage must be configured
and verified.