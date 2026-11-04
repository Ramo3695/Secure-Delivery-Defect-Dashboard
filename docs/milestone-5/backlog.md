
# Milestone 5: Security Remediation Backlog

## Project
Secure Delivery Defect and Station Performance Dashboard

## M5-SEC-01: Add Content Security Policy
- Related Finding: F-01 / R-01
- Priority: High (medium-severity finding)
- Status: Completed and retested
- Changed File: app.py
- Action: Added a Content-Security-Policy header.
- Acceptance Criteria:
  - CSP header appears in HTTP responses.
  - OWASP ZAP no longer reports the original
    missing-CSP-header finding.
- Result: Passed. The original finding was resolved.
- Remaining Work: Address the separate unsafe-inline
  CSP finding under M5-SEC-05.

## M5-SEC-02: Prevent Clickjacking
- Related Finding: F-02 / R-02
- Priority: High (medium-severity finding)
- Status: Completed and retested
- Changed File: app.py
- Action: Added X-Frame-Options: DENY and
  CSP frame-ancestors 'none'.
- Acceptance Criteria:
  - X-Frame-Options: DENY is returned.
  - CSP contains frame-ancestors 'none'.
  - The original ZAP clickjacking alert disappears.
- Result: Passed.

## M5-SEC-03: Prevent Content-Type Sniffing
- Related Finding: F-03 / R-03
- Priority: Medium (low-severity finding)
- Status: Completed and retested
- Changed File: app.py
- Action: Added X-Content-Type-Options: nosniff.
- Acceptance Criteria:
  - Responses contain X-Content-Type-Options: nosniff.
  - The original missing-header alert disappears.
- Result: Passed.

## M5-SEC-04: Reduce Server Version Disclosure
- Related Finding: F-04 / R-04
- Priority: Low
- Status: Planned
- Responsible Artifact: Production deployment
  configuration and hosting documentation.
- Action: Replace Flask's development server with
  a supported production WSGI deployment and
  minimize unnecessary server-version disclosure.
- Acceptance Criteria:
  - The production deployment uses an approved server.
  - Response headers are reviewed for version disclosure.
  - The deployed application is retested.
- Intended Completion: Before production deployment.

## M5-SEC-05: Strengthen CSP Inline-Style Restrictions
- Related Finding: F-05 / R-05
- Priority: High (medium-severity finding)
- Status: Planned
- Responsible Artifacts: HTML templates, CSS files,
  and CSP configuration in app.py.
- Action: Move inline CSS into external stylesheets
  and remove 'unsafe-inline' from the style-src policy.
- Acceptance Criteria:
  - Dashboard and forms retain their styling.
  - CSP no longer permits unsafe-inline styles.
  - OWASP ZAP no longer reports the CSP inline-style alert.
- Intended Completion: Next security-hardening iteration.

## Priority Summary

1. M5-SEC-05: Strengthen the remaining CSP restriction.
2. M5-SEC-04: Address server disclosure before deployment.

The first three items have already been implemented
and retested successfully. The remaining two items
will be addressed in future security improvements.

## Testing Evidence

- Static Analysis: Bandit 1.9.4, zero issues identified.
- Original DAST: OWASP ZAP 2.17.0.
- Retest DAST: OWASP ZAP 2.17.0.
- Target: http://127.0.0.1:5000
- Test Data: Fictional delivery and user records.