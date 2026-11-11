
# Milestone 6: Release, Rollback, and Monitoring Plan

## Project
Secure Delivery Defect and Station Performance Dashboard

## 1. Release Information

Planned Release Version: v1.0.0

Release Status:
Planned staging release. The application has not
been deployed to a production environment.

Responsible Roles:
- Release Owner: Authorized developer responsible
  for reviewing and approving deployment.
- Deployment Operator: Authorized developer
  responsible for deploying the approved version.
- Rollback Decision Owner: Release Owner.
- Rollback Execution Owner: Deployment Operator.

For this course project, I would perform these
roles with approval documented before deployment.

## 2. Release Approval

Before deploying an updated version, I would:

1. Review the GitHub Actions results.
2. Confirm all five pytest security tests passed.
3. Review Bandit and pip-audit results.
4. Review the security risk register.
5. Confirm there are no unresolved release-blocking risks.
6. Verify that no secrets are included in the package.
7. Approve the release and record the decision.

Release Gate:
Deployment is authorized only after the release
owner approves the reviewed version.

Evidence:
GitHub Actions logs and a recorded approval decision.

## 3. Release Identification

Each release will have:
- A version number, such as v1.0.0.
- A Git commit SHA.
- A source package checksum.
- A deployment date and environment.

The deployed release will be identified by its
version and commit SHA in deployment records.

## 4. Rollback Triggers

I would start a rollback if:

- The application fails to start.
- Users cannot log in.
- Team members can access manager-only pages.
- Managers can access administrator functions.
- Critical security headers are missing.
- Application errors prevent normal operations.
- Sensitive information is accidentally exposed.

## 5. Rollback Procedure

If verification fails, I would:

1. Stop the release and prevent further changes.
2. Notify the release owner.
3. Identify the last approved working version.
4. Review the failed deployment and error logs.
5. Restore the previous approved application package.
6. Restore the previous configuration if it changed.
7. Restart the application using the restored version.
8. Run the functional and security verification checks.
9. Record the rollback outcome and related issue.
10. Investigate the root cause before another release.

Rollback Decision:
The release owner authorizes rollback.

Rollback Execution:
The deployment operator restores the approved version.

## 6. Data and Configuration Restoration

Data Restoration:
The dashboard currently uses local SQLite data.
A normal code-only rollback should not require
database restoration if the schema and records
were unchanged.

If a release changes the database schema or data,
I would stop the release and restore a verified
backup only when required.

Before any data restoration, I would preserve the
current database for investigation and verify that
the backup is from the correct environment.

Configuration Restoration:
I would restore the last approved environment
settings and deployment configuration.

Secret values would remain in an approved secret
store rather than the release package.

I would not restore or reuse a secret known
to be compromised.

## 7. Deployment Verification Checklist

### Functional Verification

[ ] Application starts without errors.
Pass: The application starts and responds.
Fail: Startup errors or unavailable service.

[ ] Login page opens.
Pass: HTTP 200 and login form is displayed.
Fail: Error response or missing page.

[ ] Authorized manager accesses /dashboard.
Pass: HTTP 200 with the dashboard displayed.
Fail: Access denied or application error.

[ ] Authorized manager accesses /manage-records.
Pass: HTTP 200.
Fail: Unexpected denial or application error.

### Security Verification

[ ] Unauthenticated user cannot access /dashboard.
Pass: Redirect to login.
Fail: Protected content is returned.

[ ] Team member cannot access /manage-records.
Pass: HTTP 403 Forbidden.
Fail: Management content is accessible.

[ ] Manager cannot access /admin.
Pass: HTTP 403 Forbidden.
Fail: Administrator content is accessible.

[ ] Security headers are present.
Pass: CSP, X-Frame-Options, and
X-Content-Type-Options return expected values.
Fail: Any required header is missing.

[ ] Secrets are excluded from release files.
Pass: No actual secret values are found.
Fail: A sensitive value is included.

## 8. Post-Release Monitoring

After deployment, I would review:

- Application startup and error logs.
- HTTP 403 and 500 responses.
- Unexpected authentication failures.
- Login rate-limit events.
- Session timeout behavior.
- GitHub Actions results for the deployed commit.
- Security findings and remediation backlog.

Monitoring Evidence:
Application logs, deployment records,
GitHub Actions logs, and verification results.

## 9. Remediation and Escalation

If a deployment verification check fails:

1. Document the failed check and affected feature.
2. Review application and deployment logs.
3. Stop further deployment activity.
4. Determine whether the issue can be safely corrected.
5. If release-blocking, initiate rollback.
6. Retest after the correction or rollback.
7. Record the result in the issue backlog.

Escalation:
For this course project, I would notify the
release owner and document the issue.

In a real organization, critical security issues
would also be escalated to the security team
and application owner.

A confirmed secret exposure would require
immediate credential rotation and investigation.

## 10. Current Project Status

Completed:
- Local Flask application implementation.
- Five automated role-based access tests.
- Successful GitHub Actions CI workflow.
- Bandit security analysis.
- pip-audit dependency check.
- Environment and secrets documentation.

Planned:
- Versioned release package creation.
- Formal deployment approval.
- Staging deployment.
- Release verification.
- Monitoring evidence collection.
- Rollback testing.

This document describes the intended release and
recovery process. It does not claim that a
production release or rollback has occurred.