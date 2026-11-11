
# Milestone 6: Secure Deployment Workflow

## Project
Secure Delivery Defect and Station Performance Dashboard

## Deployment Overview

For my Flask dashboard, I created a GitHub Actions
workflow that automatically checks my application
whenever changes are pushed to the main branch.

Before releasing an updated version, I want to make
sure the application builds correctly, passes its
security tests, and does not contain known dependency
vulnerabilities.

My automated CI checks are working. Packaging,
deployment, approval, and post-deployment verification
are documented below as planned release steps.

## Deployment Workflow

### Step 1: Build

Trigger:
A push or pull request to the main branch, or a
manual GitHub Actions workflow run.

Actions:
- Check out the source code.
- Set up Python 3.14.
- Install dependencies from requirements.txt.
- Validate Python files using compileall.

Evidence:
Successful GitHub Actions build validation.

Pass Criteria:
Dependencies install and Python validation
completes without errors.

### Step 2: Test

Actions:
- Run five automated pytest security tests.
- Run Bandit static code analysis.
- Run pip-audit to check dependencies.

Evidence:
GitHub Actions logs showing:
- Five pytest tests passed.
- Bandit identified zero issues.
- pip-audit found no known vulnerabilities.

Pass Criteria:
All required CI jobs succeed.

Failure Action:
Stop the release and correct the issue before
requesting deployment approval.

### Step 3: Package

Planned Actions:
- Select a reviewed Git commit.
- Record its commit SHA and release version.
- Create a release package from the approved source.
- Exclude .env, database files, and other secrets.
- Include requirements.txt and deployment instructions.
- Record a SHA-256 checksum for the package.

Release Artifact:
Versioned application source package and
its associated deployment documentation.

Pass Criteria:
The release package contains the expected application
files, excludes sensitive local files, and can be
identified by its commit SHA and checksum.

### Step 4: Deploy

Target Environments:
- Local development: Existing Flask application.
- GitHub Actions: Automated CI testing.
- Staging: Planned controlled deployment environment.
- Production: Future environment, not yet deployed.

Responsible Role:
An authorized developer or release owner.

Approval Gate:
The release owner reviews passing CI results,
the risk register, and the proposed release package
before authorizing deployment.

Planned Actions:
- Approve the reviewed release.
- Configure required environment secrets.
- Install the approved release package in staging.
- Use a production-capable WSGI server.
- Configure HTTPS and secure session cookies.
- Record the deployed version and commit SHA.

Pass Criteria:
Only an approved release is deployed, with no
secrets stored in source code.

### Step 5: Verify

Planned Actions:
- Confirm the application starts.
- Confirm the login page loads.
- Verify authenticated dashboard access.
- Verify team-member and manager role restrictions.
- Check HTTP security headers.
- Review application error logs.
- Confirm the deployed commit matches the release.

Pass Criteria:
Required functional and security checks pass,
with no release-blocking errors.

Failure Action:
Stop the release, investigate the issue,
and follow the rollback procedure.

## Connection to Previous Security Risks

### Risk 1: Broken Access Control

Previous Risk:
A team member might access manager-only records
or administrator functions.

Deployment Control:
Automated pytest role-based access tests.

How It Reduces Risk:
GitHub Actions runs these tests when code changes
are uploaded. A failing test stops the CI workflow
and signals that the access-control problem must
be reviewed before approving a release.

### Risk 2: Accidentally Exposing Secrets

Previous Risk:
A secret key could accidentally be placed
in source code or committed to GitHub.

Deployment Controls:
Environment variables, GitHub Actions secrets,
.gitignore, and pre-release secret review.

How They Reduce Risk:
The application reads SECRET_KEY from its
environment rather than storing the secret
directly in the Python source code.

GitHub Actions uses a separate protected secret
for automated testing.

Before a release, the developer must also review
the source package and Git history for exposed
credentials. A dedicated secret scanner is a
planned improvement and is not yet part of CI.

## Deployment Status

Completed:
- GitHub Actions CI workflow.
- Python validation.
- Five automated security tests.
- Bandit security analysis.
- Dependency audit.
- GitHub Actions secret configuration.
- Local Flask application testing.

Planned:
- Automated release packaging.
- Formal release approval and deployment gate.
- Staging environment deployment.
- Post-deployment verification.
- Production deployment.

## Repository Evidence

Repository:
https://github.com/Ramo3695/Secure-Delivery-Defect-Dashboard

CI Workflow Source:
.github/workflows/security-checks.yml

Environment Guide:
docs/milestone-6/environment-setup.md

This document defines the complete intended
deployment process. The current GitHub Actions
workflow automates build validation and testing,
but it does not yet package or deploy the application.