# Task 3 — STRIDE Analysis and Threat Model Documentation

**Project:** Amazon Delivery Defect and Station Performance Dashboard  
**Status:** Proposed threat model based on Milestone 1 requirements and planned Level 1 Flask/SQLite architecture; controls are not yet verified as implemented.

## Risk rating method

Use a qualitative **likelihood × impact** method. Rate likelihood and impact Low (1), Medium (2), or High (3). The risk score is their product: **High = 6–9**, **Medium = 3–4**, **Low = 1–2**. Each row in the threat register includes its likelihood and impact scores; these are preliminary design judgments, not measured incident frequencies.

## STRIDE analysis coverage

At least six distinct components, data flows, or boundary crossings are covered: (1) browser → authentication, (2) browser → Flask API/RBAC, (3) input validation → business service → database, (4) business service → database writes, (5) sessions → browser, (6) API/login availability, (7) audit logging path, (8) API errors → browser, (9) restricted file/database storage, and (10) exports → browser. The accompanying CSV includes ten threat scenarios and ties each to Milestone 1 abuse cases and security requirements.

## Preliminary risk assumptions

The application stores fictional data only and does not connect to Amazon production systems. High ratings emphasize unauthorized account actions and data integrity; Medium ratings include availability and leakage under the proposed local/demo scope. These are initial design assessments, not results of penetration tests or production observations.

## Diagram cross-reference

TB-1 = browser/user zone; TB-2 = Flask application zone; TB-3 = restricted storage zone. Controls from Milestone 1 SR-01–SR-10 appear in the accompanying Level 1 architecture.

**Figure/Table caption:** Table 1. STRIDE threat register for the proposed delivery defect dashboard: affected flows, attack scenarios, qualitative risks, impacts, mitigations, and Milestone 1 traceability.
