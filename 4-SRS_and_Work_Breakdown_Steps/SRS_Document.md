# Software Requirements Specification

**Project:** Domain & SSL Certificate Expiry Alert System - BPS #47

**Student:** Sujay Hegde | **SRN:** PES1UG24CS478 | **Institution:** PES University

**Version:** 1.0 | **Prepared:** 2 October 2026

## 1. Introduction

### 1.1 Purpose

Specify the behavior, interfaces, constraints, and acceptance procedures for a service that checks domain registration and SSL/TLS expiry and warns responsible administrators. The intended readers are SysAdmins, Security Officers, the developer, and the lab evaluator.

### 1.2 Scope

The service maintains a monitored asset list, performs daily TLS and WHOIS checks, issues threshold-based alerts, tracks acknowledgment and escalation, and emails monthly summaries. It assists renewal decisions; it does not buy domains, renew certificates, modify DNS records, or replace a certificate authority.

### 1.3 Terms and references

An asset is a domain registration or a configured TLS endpoint. An expiry alert is a notification tied to an asset, expiry date, and threshold. Acknowledgment records responsibility for an alert; it does not mean renewal occurred. WHOIS provides registration information; TLS is used to obtain endpoint certificate information. FR, NFR, RTM, and WBS mean functional requirement, non-functional requirement, requirements traceability matrix, and work breakdown structure.

The baseline is [BPS #47](../1-RE/47_SE_Lab1_SE_Problem_Statements.pdf) and [Requirements.md](../1-RE/Requirements.md). [Use cases](../1-RE/UseCaseDiagram.md), the [acknowledgment flow](../1-RE/UseCaseSpecification.md), and the [RTM](../1-RE/RTM_Table.md) provide supporting models. Folder 2's coffee kiosk is an independent architecture exercise from the Lab 3 handout.

## 2. Overall description

### 2.1 Product perspective

Proposed BPS #47 design: a browser dashboard calls an authenticated application service. A scheduler starts daily checks and escalation evaluations. TLS and WHOIS adapters supply expiry information to the alert engine. A persistent repository stores assets, scan results, alerts, acknowledgment events, and delivery records. A notification adapter sends alerts and reports. These modules are a proposed project design; they are not the coffee-kiosk components.

### 2.2 Actors and privileges

| Actor | Responsibilities | Permissions |
| --- | --- | --- |
| SysAdmin | Maintain monitoring configuration; inspect and acknowledge alerts; read reports | Add/edit/remove authorized assets; acknowledge authorized alerts |
| Security Officer | Review escalations and monthly summaries | Read assigned asset/alert information; no monitoring-list mutation |
| External Scheduler | Trigger time-based background work | Start daily scans, check escalation deadlines, request monthly reports through a service identity |

### 2.3 Operating assumptions and constraints

The eventual service needs outbound DNS, WHOIS, TLS, and mail access, an HTTPS dashboard, durable storage, and an accurate clock. Lookup responses can be missing, malformed, rate-limited, or unavailable. No assumption is made that every registry returns WHOIS expiry data. Unknown expiry is displayed as unknown, with a diagnostic, rather than as healthy. Network timeouts, retry budgets, and concurrency limits must be configured before benchmarking.

Times are stored in UTC. Certificate thresholds use remaining UTC time; a date-only registration expiry must retain its source precision. The prototype uses injected UTC fixtures; production WHOIS parsing and scheduling remain future integration work.

## 3. External interfaces

### 3.1 Dashboard

Provide a monitored-assets list, add/edit/remove form, latest scan status, expiry warnings, an acknowledgment action, escalation status, and report access. Show unavailable results and the timestamp of the last successful check. Require authentication and verify permission on the server for each operation.

### 3.2 Lookup interfaces

TLS adapter input: hostname and endpoint port, with timeout and server-name indication. Output: certificate expiry and validation status, or an explicit error. An expired or invalid certificate must not silently become a successful result. WHOIS adapter input: domain. Output: normalized registration expiry and source metadata, or an explicit unavailable/parse error. Keep raw response parsing separate from alert policy.

### 3.3 Notification and storage interfaces

Notifications carry asset identity, expiry date, threshold, alert ID, and relevant contacts. Delivery uses a configured mail provider; credentials are excluded from reports and source control. Failed delivery is recorded and retried within a bounded budget. Storage mutations use transactions so acknowledgment and escalation cannot both win an uncoordinated race. Use a stable alert key based on asset, expiry, and threshold to prevent duplicate daily notifications.

## 4. Functional requirements

The following summarizes the existing five requirements without introducing additional FR identifiers. The complete descriptions, priorities, acceptance criteria, and rationales remain in the baseline requirements table.

| ID | Required behavior | Priority | Acceptance focus |
| --- | --- | --- | --- |
| FR-001 | Daily TLS checks; certificate alerts at 30, 15, and 3 days before expiry; expired certificates reported | High | 15-day fixture produces an alert; expiry is never silently ignored |
| FR-002 | Daily WHOIS checks; registration alerts at 45, 30, and 7 days | High | Correct threshold warnings; lookup failure recorded without crashing |
| FR-003 | Authorized acknowledgment; Security Officer escalation for high-priority assets unacknowledged after 48 hours | Medium | Before-deadline acknowledgment suppresses escalation; overdue alert escalates once |
| FR-004 | Secure dashboard supports adding, modifying, and removing domains and endpoints | High | Current registry drives the next scan; removed assets are excluded |
| FR-005 | Generate monthly all-asset summary and email stakeholders | Low | First-of-month report includes every monitored asset and unknown/error states |

## 5. Non-functional requirements

| ID | Target | Measurement |
| --- | --- | --- |
| NFR-001 | Scan 1,000 configured domains/endpoints in less than 180 seconds; HTTPS and role-based dashboard access | Record machine, concurrency, network profile, timeout budget, asset mix, and elapsed wall time. Include timeout records in the scan result. Exercise unauthenticated and unauthorized requests against deployed HTTPS routes. |
| NFR-002 | At least 99.9% monthly service availability; at most three exponential-backoff retries after a failed initial WHOIS/DNS attempt | Measure health over a full calendar month. Inject transient/persistent failures and verify increasing retry delays, bounded attempts, error logs, and continued processing of other assets. |

These are acceptance targets, not measured achievements. A simulated unit test does not establish performance, HTTPS deployment, or monthly uptime.

## 6. Data model and business rules

| Entity | Principal fields | Integrity rule |
| --- | --- | --- |
| Monitored asset | ID, domain, endpoint port, owner, security contact, priority, enabled flag | Unique configured identity; authorized mutation only |
| Scan result | Asset ID, kind (TLS/WHOIS), checked time, expiry, status, error | Preserve latest success and most recent failure separately |
| Expiry alert | ID, asset, kind, expiry, threshold, created time, state | Stable unique key prevents repeated threshold alerts |
| Acknowledgment | Alert ID, actor, timestamp | Authorized actor; atomic state transition |
| Escalation/delivery | Alert/report ID, recipient, state, attempts, timestamp | Record failures; do not claim delivery before provider success |
| Monthly report | Month, generated time, asset snapshots, delivery state | One logical report per reporting month; retries reuse report identity |

An expired asset raises an expiry warning regardless of the normal pre-expiry threshold. A lookup failure is separate from an expiry alert. Asset removal prevents future scans; audit records may be retained according to an agreed retention policy. Renewed expiry dates create a new alert cycle. Acknowledged alerts stop pending escalation but do not suppress future renewal-cycle alerts.

## 7. Workflows and failure handling

Daily check: scheduler selects current enabled assets; adapters perform bounded lookups; scan results are recorded; alert policy checks the appropriate threshold; notification dispatch is recorded. One lookup failure must not abort unrelated assets.

Acknowledgment: authenticated SysAdmin opens the alert, permission is checked, state changes atomically, and an audit event is written. At or after 48 hours, the scheduler selects still-unacknowledged high-priority alerts and attempts escalation. Production storage must prevent duplicate escalation under concurrent workers.

Monthly report: take a consistent current-asset snapshot, include success/unknown/error states, generate the summary, and dispatch to configured stakeholders. Persist a monthly identity so a restarted job cannot create duplicate reports.

## 8. Verification and release criteria

Run the 14 verification procedures in the [RTM](../1-RE/RTM_Table.md). Unit fixtures may validate thresholds, bounded retries, acknowledgment, registry changes, and report completeness. Separate integration tests must validate actual TLS/WHOIS/mail adapters, database transactions, daily/monthly scheduling, and dashboard authorization. The performance benchmark and monthly health measurement require their own recorded evidence.

Release requires all five FRs to pass their acceptance procedures, both NFRs to meet their measured targets, and all unresolved integration issues to be recorded. Captured Jira defects BB-1 through BB-4 remain To Do unless the actual Jira records are updated with verified results.

## 9. Open decisions and current implementation status

Production database, mail provider, WHOIS parser, deployment environment, benchmark profile, retention period, and scheduler timezone are to be selected during implementation. The folder-5 starter is a local core prototype using injected lookup and notification adapters and in-memory state. It does not provide the production dashboard, live scanning, persistent transactions, scheduling, or operational monitoring. Copilot provenance requires an actual Copilot session or existing Copilot-generated repository.
