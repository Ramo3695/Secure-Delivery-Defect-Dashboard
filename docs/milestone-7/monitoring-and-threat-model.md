
# Milestone 7: Monitoring and Threat-Model Updates

## Project
Secure Delivery Defect and Station Performance Dashboard

## 1. Monitoring and Logging Benefits

### Accountability

Security logging helps me track what happens in the
application and whether an action was successful or denied.

For example, during my incident simulation, a team member
attempted to access /manage-records. The application returned
HTTP 403 and recorded the authorization failure.

This provides evidence that the access-control system worked.

My current audit log records the timestamp, event type,
outcome, and role. It does not identify a specific account,
so individual accountability is limited.

### Repudiation Control

Repudiation occurs when someone denies performing an action.

Keeping audit records helps an organization investigate
disputed activities.

In my dashboard, the audit log records the type and outcome
of an action. This provides supporting evidence, but the
current logs cannot conclusively identify an individual.

A future improvement would be adding a protected internal
account identifier and event ID without storing usernames,
passwords, or session tokens in the log.

The audit log would also need protection against unauthorized
modification or deletion.

### Faster Detection

Logging can help identify suspicious behavior before it
becomes a larger security incident.

For example, repeated authorization failures could indicate
that someone is attempting to access restricted information.

Currently, I can review these events manually in
logs/security_audit.log.

An automated alert would help identify repeated failures
without requiring someone to constantly review the logs.

## 2. Three Monitoring Improvements

### Improvement 1: Repeated Authorization Failure Alerts

Current Situation:
Authorization failures are recorded in the audit log.

Planned Improvement:
Generate an alert when the same account has three or more
authorization failures within five minutes.

Log Source:
logs/security_audit.log

Response:
Review the events, verify the account's assigned role,
and investigate possible misuse or account compromise.

Additional Requirement:
Add a protected, non-sensitive account identifier to
support reliable per-account detection.

### Improvement 2: Application Error Monitoring

Current Situation:
The application handles HTTP 500 errors and records
application_error events.

Planned Improvement:
Monitor repeated application errors and alert the release
owner when several errors occur within a short period.

Log Source:
Application error logs and security audit events.

Response:
Review the affected release, investigate the failure,
and determine whether rollback is needed.

### Improvement 3: Audit Log Integrity and Retention

Current Situation:
The application writes audit events to a local rotating
log file that is excluded from GitHub.

Planned Improvement:
Store logs in a restricted central location with
appropriate access controls, retention, and backups.

Log Source:
Centralized copies of security_audit.log.

Response:
Investigate missing, altered, or unexpectedly deleted
audit records.

This would help preserve reliable evidence during
security investigations.

## 3. Updated Threat Model

Threat ID: TM-07

Threat Category:
Repudiation and operational security monitoring failure.

Protected Assets:
Delivery records, management permissions, and audit evidence.

Threat Scenario:
A team member repeatedly attempts to access manager-only
records. The application denies the requests, but without
monitoring, the attempts could go unnoticed.

Potential Business Impact:
Suspicious activity might not be investigated promptly.
If a related access-control weakness is introduced later,
sensitive delivery information could be exposed or changed.

Existing Controls:
- Server-side role-based access control.
- HTTP 403 responses for unauthorized requests.
- Audit logging for authorization failures.
- Automated pytest access-control tests.

Evidence:
The Milestone 7 incident simulation returned HTTP 403
and generated an authorization_failure event.

Remaining Weaknesses:
- No automated alerting for repeated denied requests.
- Current audit events do not include a protected account ID.
- Local logs are not centrally monitored.

Planned Mitigation:
Add alerting for repeated access denials, use a protected
account identifier for event correlation, and monitor logs
through an approved centralized logging system.

Validation:
Repeat the incident simulation using fictional accounts.
Confirm that three denied attempts within five minutes
produce an alert and that no sensitive credentials are logged.

Status:
Existing prevention and event logging verified.
Automated monitoring improvements planned.

## 4. Current Project Status

Completed:
- Role-based access control.
- Automated access-control testing.
- Authentication and authorization event logging.
- Simulated unauthorized access attempt.
- HTTP 403 denial evidence.
- Audit log evidence.

Planned:
- Automated security alerts.
- Protected account-level event correlation.
- Centralized log storage.
- Log-integrity monitoring.
- Ongoing operational monitoring after deployment.