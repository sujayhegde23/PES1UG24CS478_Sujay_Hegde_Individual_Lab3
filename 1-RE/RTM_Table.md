# Requirements Traceability Matrix

**Student:** Sujay Hegde | **SRN:** PES1UG24CS478

**Project:** BPS #47 - Domain & SSL Certificate Expiry Alert System

This matrix traces the seven baseline requirements to the use cases, proposed BPS #47 modules, work packages, and verification procedures. The coffee-kiosk diagram in folder 2 is a separate handout exercise and does not implement these requirements. Test coverage below is a plan; it does not establish that a deployed application meets a requirement.

| Requirement | Summary / priority | Use cases | Proposed modules | WBS package | Verification IDs | Current evidence |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | Daily TLS checks; alerts at 30, 15, 3 days and for expired certificates / High | UC-003 Scan; UC-004 Handle Alert | Scheduler, TLS Adapter, Alert Engine | WP-3.1, WP-3.3 | TC-001, TC-002 | Requirements and Jira BB-1; starter policy tests only |
| FR-002 | Daily WHOIS checks; alerts at 45, 30, 7 days / High | UC-003; UC-004 | Scheduler, WHOIS Adapter, Alert Engine | WP-3.2, WP-3.3 | TC-003, TC-004 | Requirements and Jira BB-2; injected lookup/retry tests only |
| FR-003 | Acknowledge alerts; escalate high-priority alerts after 48h / Medium | UC-004; UC-005 Acknowledge; UC-006 Escalate | Alert Engine, Notification Adapter, Auth | WP-3.3, WP-3.4 | TC-005, TC-006 | Flow specification and Jira BB-3; starter state/timer tests only |
| FR-004 | Authorized domain/endpoint add, edit, remove / High | UC-001 Manage; UC-002 Authenticate | Registry, Auth, Dashboard | WP-2.1, WP-2.2 | TC-007, TC-008 | Jira BB-4; starter registry/role tests only |
| FR-005 | Monthly all-asset summary emailed to stakeholders / Low | UC-007 Monthly Report | Reporting, Notification Adapter, Scheduler | WP-3.5 | TC-009, TC-010 | Jira reporting work items; starter report fixture only |
| NFR-001 | 1,000 assets under 180s; HTTPS and role controls / High | All protected user operations; UC-003 | Bounded-concurrency Scanner, Auth, HTTPS Gateway | WP-2.1, WP-4.1 | TC-011, TC-012 | Benchmark and deployed HTTPS verification pending |
| NFR-002 | 99.9% monthly availability; bounded backoff retries / High | UC-003; system-wide | Lookup Adapters, Monitoring, Persistence | WP-3.2, WP-4.2 | TC-004, TC-013, TC-014 | Starter retry/isolation tests only; availability measurement pending |

## Verification procedures

| ID | Procedure | Expected result | Level / status |
| --- | --- | --- | --- |
| TC-001 | Supply TLS expiry fixtures at 30, 15, 3, 31, and 0 days; repeat a scan | Alerts at specified thresholds and expiry; repeated threshold scan creates no duplicate | Unit fixtures implemented; live TLS integration pending |
| TC-002 | Run the daily job against a controlled valid and expired TLS endpoint | Read certificate expiry, record an expired-certificate warning, and preserve validation errors | Integration / planned |
| TC-003 | Supply WHOIS expiry fixtures at 45, 30, 7, and 46 days | Alerts at 45, 30, 7; no threshold alert at 46 | Unit fixtures implemented; live WHOIS integration pending |
| TC-004 | Fail a lookup transiently, then persistently | At most three retries after the initial attempt, increasing delays; persistent error recorded | Unit fixtures implemented |
| TC-005 | Acknowledge an open alert before 48h; then run escalation | Actor/time recorded; no pending escalation is sent | Unit fixture implemented |
| TC-006 | Check high-priority alert at 47h59m and 48h; check low-priority alert at 48h | Escalate once at/after 48h only for the unacknowledged high-priority alert | Unit fixture implemented |
| TC-007 | Add, edit, and remove an asset; perform the next scan | Registry reflects edits; removed asset is not scanned | Unit fixture implemented; dashboard integration pending |
| TC-008 | Attempt mutation as Security Officer and an unknown role | Both denied; authorized SysAdmin succeeds | Unit fixture implemented; session security pending |
| TC-009 | Produce report after mixed successful and failed scans | Every current asset appears; unknown/failed results are explicit | Unit fixture implemented |
| TC-010 | Exercise first-of-month schedule and stakeholder mail delivery | One report per month; delivery records and retry behavior retained | Integration / planned |
| TC-011 | Scan 1,000 assets using a recorded environment and latency/failure profile | Total elapsed time below 180 seconds including timeout records | Performance / planned |
| TC-012 | Visit deployed HTTPS dashboard; test unauthenticated access and role changes | HTTPS enforced; protected requests denied without valid authorization | Security / planned |
| TC-013 | Fail one asset while another succeeds | Failed asset logged; other asset still scanned; worker stays alive | Unit fixture implemented |
| TC-014 | Measure service health throughout one calendar month | Available service minutes / monitored minutes >= 99.9% | Operational / planned |

## Defect traceability

| Captured Jira defect | Requirement | Planned regression |
| --- | --- | --- |
| BB-1: Missing 15-day SSL alert | FR-001 | TC-001, TC-002 |
| BB-2: WHOIS failure without retry | FR-002, NFR-002 | TC-004, TC-013 |
| BB-3: Missing 48-hour escalation | FR-003 | TC-005, TC-006 |
| BB-4: Removed domain still scanned | FR-004 | TC-007 |

The source screenshots show these defects in To Do. Starter tests do not change their Jira status or prove resolution in a production application. See [requirements](Requirements.md), [SRS](../4-SRS_and_Work_Breakdown_Steps/SRS_Document.md), [WBS](../4-SRS_and_Work_Breakdown_Steps/Work_Breakdown_Structure.md), and [starter code status](../5-Github_Copilot_Generated_Code/README.md).
