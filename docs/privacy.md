# Privacy Policy

## Summary

This tool is designed to minimise personal data processing in the simulation engine.

Authentication is provided by **Clerk**. Account-level personal data is handled by Clerk as a third-party identity provider.

The application backend does not persist simulation inputs or simulation outputs per user.

---

## Authentication

Some application routes require sign-in. Authentication is managed by Clerk.

When using authenticated routes:

- Clerk may process account information (for example, email address and authentication metadata).
- The API validates JWT bearer tokens issued by Clerk.
- The API does not store user account profiles in the project database (no project user database is used in this PoC).

---

## Personal Data Processed by This Project

The simulation engine and API are designed not to collect or persist household PII within project-owned storage.

The project does not intentionally request or store:

- Name
- Address or postcode
- National Insurance number
- Date of birth
- Device identifiers

However, authentication-related personal data may be processed by Clerk under Clerk’s policies.

---

## No Bank Linking

This tool does **not** connect to, integrate with, or request access to any bank account, payment account, or financial institution. You do not share any credentials, open banking tokens, or account data with this platform.

---

## No Statement Uploads

You cannot and do not upload bank statements, payslips, tax returns, or any other financial documents. All inputs are entered manually by the user as numerical values.

---

## Data Not Stored

The numerical inputs you enter into the stress test form are:

- Used **in-memory** to compute your results.
- **Not persisted** to any database, file, or log.
- **Not transmitted to third parties by the simulation engine** for analytics/marketing purposes.
- **Discarded** immediately after your results are returned.

We do not operate any analytics, tracking pixels, session recording, or behavioural data collection on this platform.

---

## Cookies

This tool does not use tracking or analytics cookies.

Authentication/session cookies or browser storage may be used by Clerk for identity and session management.

---

## GDPR Considerations

Under the UK General Data Protection Regulation (UK GDPR) and the Data Protection Act 2018:

Project-operated simulation processing remains minimal and non-persistent.

For authentication and account data, Clerk acts as a third-party provider and its own legal terms, lawful basis, and data subject processes apply.

If you believe that any personal data has been inadvertently collected or processed, please contact us immediately so we can investigate and remedy the situation.

---

## Third-Party Services

This tool integrates with Clerk for authentication.

This tool does not integrate with third-party analytics, advertising, or data enrichment services.

If the tool is deployed using a cloud hosting provider, standard infrastructure-level logging (e.g. access logs) may be retained by the hosting provider in accordance with their own privacy policies. These logs are infrastructure-level and are not used to profile or identify individual users.

---

## Changes to This Policy

This privacy policy may be updated from time to time. Any changes will be reflected in the repository and versioned accordingly.

---

*This document was last reviewed: 2026-03-04.*
