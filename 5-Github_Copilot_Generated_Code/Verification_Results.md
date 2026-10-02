# Starter Verification Results

**Sujay Hegde | PES1UG24CS478 | BPS #47**

Executed on 2 October 2026 with Node.js 24.16.0 using `npm test` in this folder.

Result: **12 tests passed, 0 failed.**

The suite checks TLS/WHOIS threshold boundaries and expired/invalid dates; duplicate threshold notifications; transient recovery; bounded persistent failure; acknowledgment; the 48-hour escalation boundary and priority; registry edits and removal; unauthorized mutations; failed/unknown lookup reporting and isolation; retrying pending notification delivery; and preservation of the last successful lookup after failure.

`npm run demo` also completed with two fixture-based expiry notifications and an all-asset summary. Neither command sends actual email or contacts real TLS/WHOIS endpoints.

This is evidence for the local Codex-authored prototype. It is not Copilot provenance, live-adapter validation, a 1,000-asset benchmark, an HTTPS audit, a concurrency test, or monthly uptime evidence. Full acceptance procedures are in [the RTM](../1-RE/RTM_Table.md).
