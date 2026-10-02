# Requirements Table: Domain & SSL Certificate Expiry Alert System

## Functional Requirements (FR)

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| FR-001 | Functional | The system shall initiate TLS handshakes against monitored domains daily, extract certificate expiration dates, and trigger alerts at 30, 15, and 3 days before expiry. | High | Pass: Alert queued for certificate expiring in 15 days; Fail: Expired certificate ignored without notification. | Prevents downtime due to expired SSL certificates by ensuring administrators receive timely warnings. |
| FR-002 | Functional | The system shall perform daily WHOIS lookups for all monitored domains to extract domain registration expiry dates and alert at 45, 30, and 7 days before expiry. | High | Pass: WHOIS data parsed and alerts sent at 45 days. Fail: System crashes on WHOIS rate limit. | Ensures domains are renewed before they are released or bought by unauthorized third parties. |
| FR-003 | Functional | The system shall provide an escalation ladder to notify the Security Officer if a SysAdmin does not acknowledge an expiry alert within 48 hours for high-priority domains. | Medium | Pass: Security Officer receives escalation email after 48h of inaction. | Guarantees that critical expiring assets are brought to management's attention if the primary contact is unavailable. |
| FR-004 | Functional | The system shall allow SysAdmins to add, modify, or remove domains and associated endpoints from the monitoring list via a secure dashboard. | High | Pass: Domain successfully added and appears in the next daily scan. | Required for the system to adapt to the organization's changing infrastructure and domain portfolios. |
| FR-005 | Functional | The system shall generate a monthly summary report detailing the health of all monitored domains and certificates, and email it to all stakeholders. | Low | Pass: Report generated on the 1st of the month with 100% of monitored assets. | Provides high-level visibility to Security Officers regarding the overall compliance and security posture. |

## Non-Functional Requirements (NFR)

| ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| NFR-001 | Performance & Security | The monitoring engine shall scan a list of 1,000 domains and SSL endpoints in under 3 minutes. | High | Pass: Benchmarking tests confirm target latency and security standards under simulated peak load. | Ensures the system can scale efficiently without consuming excessive resources or causing scan overlaps. |
| NFR-002 | Reliability & Availability | The system must guarantee 99.9% uptime and gracefully handle temporary failures of external WHOIS or DNS servers by implementing exponential backoff retries. | High | Pass: System correctly retries failed WHOIS lookups 3 times before logging a persistent error, without crashing. | Network utilities rely on external services that can occasionally fail; resilience is necessary to avoid false alarms or missed expirations. |
