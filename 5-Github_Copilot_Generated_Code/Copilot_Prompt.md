# Prepared GitHub Copilot Prompt

This is a prompt prepared for a future Copilot session, not a record of a session that already occurred.

Paste the following into GitHub Copilot Chat while the BPS #47 requirements, RTM, SRS, and starter code are available as context:

> Implement the Domain & SSL Certificate Expiry Alert System for Sujay Hegde, PES1UG24CS478, BPS #47. Preserve the five FR identifiers and two NFR identifiers in Requirements.md. Review the starter monitoring_core.mjs and its tests, then implement live lookup adapters and durable storage in separate modules. TLS monitoring alerts at 30, 15, and 3 days and explicitly reports expired or invalid certificates. WHOIS monitoring alerts at 45, 30, and 7 days and returns unknown when expiry data cannot be parsed. Retry failed lookups at most three times after the initial attempt, with configurable exponential backoff and timeouts. Do not let one lookup failure stop other assets. Keep lookup success separate from notification delivery failure. Persist stable alert keys, acknowledgement audit events, and escalation states. Only authorized SysAdmins can change assets or acknowledge alerts; high-priority unacknowledged alerts escalate after 48 hours. Monthly summaries include all monitored assets and error/unknown states. Inject the clock and external providers for tests. Use an atomic storage operation to prevent concurrent duplicate alerts or escalation. Document remaining dashboard, scheduling, mail, benchmark, and operational requirements explicitly. Never claim a measured performance target or monthly availability from unit tests. Do not commit secrets. Explain generated changes and how to run the tests.

Suggested follow-up after reviewing the output:

> Add integration tests against controlled TLS/WHOIS fixtures and transactional storage. Map tests to the RTM IDs, include timeout, renewal, duplicate-worker, and acknowledgement/escalation race cases, and report actual results. Preserve the distinction between simulated tests and live production acceptance evidence.
