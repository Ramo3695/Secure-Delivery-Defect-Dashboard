
# Milestone 5: Security Findings and Retesting

## Project Information
Project: Secure Delivery Defect and Station Performance Dashboard

Testing Tools:
- Bandit 1.9.4 (SAST)
- OWASP ZAP 2.17.0 (DAST)
- VS Code and curl (manual verification)

Test Environment:
- Local Flask application
- URL: http://127.0.0.1:5000
- Fictional test accounts and delivery records

## Static Security Testing

Bandit scanned app.py and models.py.

Results:
- Lines of code scanned: 383
- High-severity findings: 0
- Medium-severity findings: 0
- Low-severity findings: 0

Bandit did not identify issues covered by its scanning rules.
Additional dynamic testing was performed using OWASP ZAP.

## Security Findings

### F-01: Missing Content Security Policy
- Source: OWASP ZAP
- Location: Flask HTTP response headers, app.py
- Severity: Medium
- Validation Status: True positive
- Description: The application did not return a CSP header.
- Business Impact: Reduced browser protection against
  malicious content and potential information disclosure.
- Traceability: SR-04 input/output protection;
  STRIDE information disclosure and tampering.
- Priority: High because browser-side protections
  were missing.
- Remediation: Added CSP header in app.py.
- Retest Status: Original missing-header finding resolved.
- Residual Risk: CSP still allows unsafe-inline styles.

### F-02: Missing Anti-clickjacking Protection
- Source: OWASP ZAP
- Location: Flask response headers, app.py
- Severity: Medium
- Validation Status: True positive
- Description: The application lacked anti-framing controls.
- Business Impact: Users might be tricked into clicking
  application controls inside another website.
- Traceability: STRIDE spoofing and user-interface
  deception; security-header configuration.
- Priority: High because account and record-management
  features require protection from unauthorized interaction.
- Remediation: Added X-Frame-Options: DENY and
  frame-ancestors 'none'.
- Retest Status: Resolved.
- Residual Risk: Other social-engineering attacks remain.

### F-03: Missing X-Content-Type-Options
- Source: OWASP ZAP
- Location: Flask response headers, app.py
- Severity: Low
- Validation Status: True positive
- Description: The application did not set nosniff.
- Business Impact: Browsers could interpret content
  differently from the declared content type.
- Traceability: Output-handling security requirement;
  HTTP response configuration.
- Priority: Medium because the fix is simple and
  improves defensive configuration.
- Remediation: Added X-Content-Type-Options: nosniff.
- Retest Status: Resolved.
- Residual Risk: Content types still require validation.

### F-04: Server Version Disclosure
- Source: OWASP ZAP
- Location: Flask development server response header
- Severity: Low
- Validation Status: True positive
- Description: The Server header reveals Werkzeug
  and Python version information.
- Business Impact: An attacker could use version
  details to investigate known vulnerabilities.
- Traceability: SR-09 secure error handling and
  information-disclosure threat.
- Priority: Low in the controlled local environment,
  but must be addressed before deployment.
- Remediation: Planned production WSGI deployment
  and server-header configuration review.
- Retest Status: Unchanged.
- Residual Risk: Version information remains visible.

### F-05: CSP Allows Inline Styles
- Source: OWASP ZAP retest
- Location: CSP in app.py and HTML templates
- Severity: Medium
- Validation Status: True positive
- Description: CSP includes style-src 'unsafe-inline'.
- Business Impact: Weaker browser enforcement against
  certain style-injection attacks.
- Traceability: SR-04 output protection and
  browser security configuration.
- Priority: High because it is the remaining
  medium-risk configuration finding.
- Remediation: Planned removal of inline CSS
  and tightening of the CSP.
- Retest Status: Open, newly identified.
- Residual Risk: Inline styling remains permitted.

## Before-and-After Retesting

### Remediation 1: Content Security Policy

Original Result:
OWASP ZAP reported a missing CSP header (Medium).

Corrective Action:
Added Content-Security-Policy to Flask responses.

Retest:
The CSP header appeared in curl and ZAP responses.
The original missing-header alert was no longer reported.

Outcome:
Resolved original finding.

Remaining Risk:
ZAP reported a separate medium-risk alert for
style-src 'unsafe-inline'. Further hardening is planned.

### Remediation 2: Anti-clickjacking Protection

Original Result:
OWASP ZAP reported a missing anti-clickjacking
header (Medium).

Corrective Action:
Added X-Frame-Options: DENY and
CSP frame-ancestors 'none'.

Retest:
Both controls were present in HTTP responses.
The original anti-clickjacking alert was absent
from the fresh ZAP scan.

Outcome:
Resolved.

Remaining Risk:
The application still requires routine testing
and deployment security reviews.

### Additional Remediation: Content-Type Protection

Original Result:
X-Content-Type-Options was missing (Low).

Corrective Action:
Added X-Content-Type-Options: nosniff.

Retest:
The header was present and the missing-header
alert was no longer reported.

Outcome:
Resolved.

## Overall Testing Conclusion

The initial ZAP scan identified missing security
headers that could weaken browser protections.
I updated the Flask application to add CSP,
anti-clickjacking protection, and content-type
protection.

During retesting, I confirmed that the original
missing-header findings were no longer reported.
However, ZAP identified a new CSP configuration
issue, and the development server still exposes
version information.

These remaining findings will be tracked in
the project risk register and backlog.