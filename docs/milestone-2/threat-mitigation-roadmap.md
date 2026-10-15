# Task 5 — Threat Prioritization and Mitigation Roadmap

**Project:** Amazon Delivery Defect and Station Performance Dashboard  
**Document status:** Planned design; mitigations are not yet confirmed as implemented.  
**Basis:** Milestone 1 security requirements (SR-01–SR-10) and Milestone 2 STRIDE threat register.

## Ranking method

The threat register calculates risk as **likelihood (1–3) × impact (1–3)**: High = 6–9, Medium = 3–4, Low = 1–2. All five threats selected below score **6 (High; 2 × 3 for T-02, T-04, T-03, and T-05; 3 × 2 for T-01)**. For ties, rank first the threats that can enable broader compromise of account privileges and record integrity, then those that expose authenticated sessions. T-07 is also High but is ranked below the top five because the planned early work emphasizes preventive identity, authorization, and input safeguards; audit protection remains required in the backlog.

| Rank | ID | Risk and likely impact | Why this rank | Planned mitigation | Planned implementation / verification |
|---|---|---|---|---|---|
| 1 | **T-02** | **High (6)** — Unauthorized account/role changes or modified operational records | Direct admin-endpoint abuse could undermine multiple permissions and records at once. | Enforce RBAC on protected API routes and individual records; deny access by default; test unauthorized role access. | **Weeks 2–3** — implement RBAC with authentication; **Week 7** — verify with role-based negative tests. |
| 2 | **T-01** | **High (6)** — Unauthorized access to accounts and fictional operational records | Login is an early trust boundary; compromise grants entry to protected features. | Password hashing; secure authentication; login throttling and temporary lockout; secure session cookies. | **Weeks 2–3** — implement authentication; **Week 7** — verify brute-force and login tests. |
| 3 | **T-04** | **High (6)** — Lost or changed defect/route records and inaccurate dashboard trends | Integrity of the core performance records is essential to the application's purpose. | Check permission and record ownership/scope on each write/delete; use database transactions; record audit events. | **Weeks 4–5** — secure CRUD operations; **Week 7** — verify edit/delete permissions and logs. |
| 4 | **T-03** | **High (6)** — Data corruption or manipulated database queries | Untrusted form input could damage records or circumvent intended data processing. | Apply server-side type, length, and range checks; use parameterized SQL; reject malformed input. | **Weeks 4–5** — validation and database access work; **Week 7** — test invalid-input and injection scenarios. |
| 5 | **T-05** | **High (6)** — Session reuse and unauthorized actions without the user's password | An unattended or stolen session bypasses the need to guess a password. | Use HttpOnly/Secure/SameSite cookies, session idle expiration, logout invalidation, CSRF protection for state-changing actions, and HTTPS when deployed. | **Weeks 2–3** — session safeguards; **Week 7** — verify inactivity, logout, and session misuse tests. |

## Follow-up work that remains required

- **T-07 (High):** Protect audit logs from alteration and record sensitive actions (**Weeks 5–6**); verify in **Week 7**.
- **T-06 (Medium):** API rate/request limits and monitoring (**Weeks 5–6**); verify in **Week 7**.
- **T-08 (Medium):** Generic errors and restricted diagnostics (**Weeks 4–5**); verify in **Week 7**.
- **T-09 (Medium):** Restricted local database/backups and encryption of sensitive backups or deployed storage, as applicable (**Weeks 5–6**); verify in **Week 7**.
- **T-10 (Medium):** Authorized report exports and nonpublic storage paths (**Weeks 5–6**); verify in **Week 7**.

## Backlog handoff

In Task 6, create or update Jira backlog items for **every mitigation and follow-up action**, not only the top five. Link each item to its threat ID and security requirement(s). Include a backlog export/screenshot in the report and save the milestone artifacts and version/commit evidence to GitHub.

**Report caption:** Table 2. Ranked top-five threats and planned implementation/verification roadmap for the Secure Delivery Defect and Station Performance Dashboard.
