
# Milestone 7: Incident Response Plan

## Project
Secure Delivery Defect and Station Performance Dashboard

## Incident Scenario
A team member attempts to access manager-only delivery records.

## 1. Preparation
Before an incident happens, I would make sure role-based
access controls are enabled, audit logging is working,
and authorized personnel know how to review security events.

## 2. Detection
I would review the security audit log for authorization
failures. Repeated denied attempts from the same account
or session would be treated as suspicious activity.

The event type "authorization_failure" with the outcome
"denied" helps identify an attempted unauthorized action.

## 3. Containment
If repeated unauthorized attempts were detected, I would
review the affected account and temporarily restrict access
if there were signs of compromise.

I would preserve the audit log evidence and verify that
the protected records had not been modified.

## 4. Eradication
I would investigate why the attempts occurred and determine
whether the account was compromised or the user was attempting
to bypass their assigned permissions.

If a vulnerability were identified, I would correct the
authorization logic and review similar routes for weaknesses.

## 5. Recovery
After correcting the issue, I would retest the application
to confirm that team members still receive HTTP 403 when
requesting manager-only pages.

I would also verify that managers can still access the
functions required for their jobs.

## 6. Communication
I would document the incident, including when it occurred,
the affected route, the account role, and the response taken.

For a serious incident, I would notify the application
owner and security team so they could determine whether
additional investigation was necessary.

## 7. Lessons Learned
After resolving the incident, I would review what worked
and what could be improved.

One improvement would be creating an automated alert when
several authorization failures happen within a short period.

This would help identify suspicious activity sooner instead
of relying only on someone manually checking the audit log.

## Incident Evidence

- Test account role: team_member
- Attempted route: /manage-records
- Application result: HTTP 403 Access Denied
- Audit event: authorization_failure
- Audit outcome: denied
- Evidence: Browser screenshot and audit log screenshot

## Current Status

The simulated unauthorized access attempt was completed
successfully in the local test environment.

The application denied access and recorded the event.
No successful unauthorized access was demonstrated.

Automated alerting and a production incident response
process remain planned improvements.