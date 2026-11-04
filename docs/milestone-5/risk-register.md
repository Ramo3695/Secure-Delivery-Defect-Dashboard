
# Milestone 5: Security Risk Register

## Project
Secure Delivery Defect and Station Performance Dashboard

## Testing Environment
Local Flask application using fictional delivery data.

## Risk R-01: Missing Content Security Policy

- Finding ID: F-01
- Original Severity: Medium
- Likelihood: Moderate
- Source: OWASP ZAP
- Affected Component: Flask HTTP response headers
- Risk: Without a CSP, the browser has fewer restrictions
  on which scripts and other resources can load.
- Business Impact: Increased exposure to malicious
  content and potential information disclosure.
- Corrective Action: Added a Content-Security-Policy
  header in app.py.
- Mitigation: Restrict permitted content sources.
- Status: Resolved original finding
- Retest Evidence: CSP header present; original
  missing-header alert no longer reported.
- Residual Risk: The policy still permits unsafe-inline
  CSS, which ZAP identified as a separate finding.
- Backlog Item: M5-SEC-01
- Acceptance Criteria: CSP is returned on application
  responses, and the missing-CSP alert is absent.
- Completion Status: Completed and retested

## Risk R-02: Missing Anti-clickjacking Protection

- Finding ID: F-02
- Original Severity: Medium
- Likelihood: Moderate
- Source: OWASP ZAP
- Affected Component: Flask HTTP response headers
- Risk: Another website could attempt to display
  the application inside a frame.
- Business Impact: A user could be tricked into
  interacting with application controls.
- Corrective Action: Added X-Frame-Options: DENY
  and CSP frame-ancestors 'none' in app.py.
- Mitigation: Prevent other websites from framing
  the application.
- Status: Resolved
- Retest Evidence: Header present; original
  anti-clickjacking alert no longer reported.
- Residual Risk: Other forms of user deception
  remain possible.
- Backlog Item: M5-SEC-02
- Acceptance Criteria: Responses contain
  X-Frame-Options: DENY and frame-ancestors 'none'.
- Completion Status: Completed and retested

## Risk R-03: Missing Content-Type Protection

- Finding ID: F-03
- Original Severity: Low
- Likelihood: Low
- Source: OWASP ZAP
- Affected Component: Flask HTTP response headers
- Risk: Browsers might interpret certain content
  differently from its declared content type.
- Business Impact: Increased risk of unsafe
  content handling.
- Corrective Action: Added
  X-Content-Type-Options: nosniff in app.py.
- Status: Resolved
- Retest Evidence: Header present; original
  missing-header alert no longer reported.
- Residual Risk: Content types must still be
  assigned correctly.
- Backlog Item: M5-SEC-03
- Acceptance Criteria: Responses contain nosniff.
- Completion Status: Completed and retested

## Risk R-04: Server Version Disclosure

- Finding ID: F-04
- Original Severity: Low
- Likelihood: Low
- Source: OWASP ZAP
- Affected Component: Flask development server
- Risk: HTTP responses expose the Werkzeug and
  Python versions.
- Business Impact: The information could help
  an attacker research version-specific weaknesses.
- Corrective Action: Planned production deployment
  using a supported WSGI server and appropriate
  server-header configuration.
- Status: Open
- Retest Evidence: Version information remains
  visible in the Server response header.
- Residual Risk: Version information remains exposed
  in the local development environment.
- Backlog Item: M5-SEC-04
- Acceptance Criteria: Deployment configuration
  is reviewed and unnecessary version disclosure
  is removed or minimized.
- Completion Status: Planned

## Risk R-05: CSP Allows Inline Styles

- Finding ID: F-05
- Original Severity: Medium (new retest alert)
- Likelihood: Moderate
- Source: OWASP ZAP
- Affected Component: CSP configuration and HTML
- Risk: The policy includes style-src 'unsafe-inline'.
- Business Impact: The policy provides weaker
  protection against certain style-injection risks.
- Corrective Action: Planned migration of inline CSS
  to approved external stylesheets, followed by
  removal of unsafe-inline from the CSP.
- Status: Open
- Retest Evidence: ZAP reported the unsafe-inline
  CSP alert after the security headers were added.
- Residual Risk: Inline CSS remains permitted.
- Backlog Item: M5-SEC-05
- Acceptance Criteria: Application styling works
  without unsafe-inline, and a new ZAP scan no
  longer reports the finding.
- Completion Status: Planned

## Risk Prioritization

The medium-risk findings receive higher priority
because they affect browser security protections.

The missing CSP and anti-clickjacking headers were
addressed first because both could be corrected
without changing the application database or roles.

The remaining CSP unsafe-inline finding is prioritized
for additional remediation. Server version disclosure
will be addressed during production deployment planning.

Risk likelihood estimates are preliminary judgments
for this local development project.