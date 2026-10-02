# Work Breakdown Structure and Execution Steps

**Sujay Hegde | PES1UG24CS478 | BPS #47 - Domain & SSL Certificate Expiry Alert System**

The hierarchy and work-package dictionary describe the project's work. Status reflects available artifacts, not an invented schedule or completed production implementation. Sujay Hegde is the owner of each work package.

## 1. Hierarchical WBS

```text
1.0 Domain & SSL Certificate Expiry Alert System
  1.1 Requirements and planning
    1.1.1 Define actors, scope, five FRs, and two NFRs
    1.1.2 Model use cases and acknowledgment flow
    1.1.3 Produce RTM and SRS
    1.1.4 Organize Jira epics, backlog, and defect evidence
  1.2 Secure configuration and persistence
    1.2.1 Authentication and role authorization
    1.2.2 Asset registry and dashboard CRUD
    1.2.3 Durable records, unique alert keys, and audit events
  1.3 Monitoring and notification
    1.3.1 Daily scheduler and TLS adapter
    1.3.2 WHOIS adapter, parsing, timeouts, and retries
    1.3.3 Threshold alert lifecycle and acknowledgment
    1.3.4 48-hour escalation and notification delivery
    1.3.5 Monthly report generation and email
  1.4 Verification and operations
    1.4.1 Functional tests, 1,000-asset benchmark, HTTPS security checks
    1.4.2 Fault isolation, recovery, and monthly availability monitoring
  1.5 Assignment documentation and evidence
    1.5.1 Separate coffee-kiosk architectural exercise
    1.5.2 GitHub and Jira evidence indexing
    1.5.3 Actual Copilot generation and evidence capture
    1.5.4 Final README, PDFs, and submission review
```

## 2. Work-package dictionary

| Package | Output / completion criterion | Requirement | Depends on | Current status |
| --- | --- | --- | --- | --- |
| WP-1.1 | Approved requirements, actors, use cases, flow, RTM, SRS | All seven | None | Documents prepared |
| WP-1.2 | Jira setup and defect evidence indexed with source pages | All seven | WP-1.1 | Captured setup evidence available; sprint completion not asserted |
| WP-2.1 | Login/session security and authorization checked on every protected route | FR-003, FR-004, NFR-001 | WP-1.1 | Starter role guard only; production auth planned |
| WP-2.2 | Asset CRUD dashboard backed by durable registry; removed asset excluded from scans | FR-004 | WP-2.1 | Starter registry fixture only; dashboard/persistence planned |
| WP-2.3 | Transactional alert/scan/audit storage; duplicate and race tests pass | FR-001 to FR-005 | WP-2.2 | Planned |
| WP-3.1 | Actual TLS adapter and daily job detect expiry and validation failure | FR-001 | WP-2.2, WP-2.3 | Injected fixtures available; live adapter/scheduler planned |
| WP-3.2 | WHOIS parser and bounded retries handle unavailable registry data | FR-002, NFR-002 | WP-2.2 | Injected fixtures available; live adapter planned |
| WP-3.3 | Alert thresholds and acknowledgment state transitions tested | FR-001, FR-002, FR-003 | WP-3.1, WP-3.2 | Starter logic and fixtures available; durable integration planned |
| WP-3.4 | Escalation at 48h; actual mail delivery and retry evidence | FR-003 | WP-3.3 | Starter deadline logic available; mail integration planned |
| WP-3.5 | All-asset summary; scheduled monthly delivery, identity, and retry checks | FR-005 | WP-3.1, WP-3.2, WP-3.4 | Starter report fixture only; scheduling/mail planned |
| WP-4.1 | TC-001 to TC-012 executed; benchmark below 180s and HTTPS verified | Five FRs, NFR-001 | WP-2.1 to WP-3.5 | Core unit tests available; integration/security/performance planned |
| WP-4.2 | Failure isolation, recovery, and measured 99.9% monthly availability | NFR-002 | WP-3.2, WP-4.1 | Starter failure fixture available; operational measurement planned |
| WP-5.1 | Coffee-kiosk diagram and one-page justification exported | Separate Lab 3 handout | None | Available in folder 2 |
| WP-5.2 | Real repository/history and Jira screenshots indexed | Assignment evidence | WP-1.2 | Available in folder 3 |
| WP-5.3 | Run GitHub Copilot on project code; retain prompt/output and real screenshot or repository link | Assignment item 5 | WP-1.1 | Pending actual Copilot session; Codex starter supplied |
| WP-5.4 | All deliverables linked; PDFs readable; no missing or falsely attributed evidence | Assignment checklist | WP-5.1 to WP-5.3 | Documentation prepared; Copilot evidence outstanding |

## 3. Execution steps and review gates

1. Review the seven baseline requirements and actor permissions. Resolve production decisions in SRS section 9 before selecting adapters.
2. Implement authentication, registry CRUD, and durable storage. Gate: unauthorized mutation rejected and removed domains excluded from the next scan.
3. Integrate TLS and WHOIS adapters and the daily scheduler. Gate: controlled real endpoints produce correct expiry/error records with bounded attempts.
4. Integrate alert notifications, acknowledgment, and 48-hour escalation. Gate: thresholds are correct; duplicate daily notifications and acknowledgment/escalation races are prevented.
5. Integrate monthly report scheduling and mail. Gate: every current asset is represented, including failed checks, and report retries do not duplicate logical reports.
6. Execute the RTM verification plan. Gate: functional integration evidence, the defined performance benchmark, and HTTPS/role checks are recorded separately from prototype unit tests.
7. Deploy health monitoring and observe availability over a complete month. Gate: measured availability meets NFR-002; failures and recovery procedures are documented.
8. Complete the actual Copilot session, capture evidence, verify all links and exported PDFs, and review the assignment checklist before submission.

## 4. Risk and mitigation

| Risk | Effect | Planned mitigation / verification |
| --- | --- | --- |
| WHOIS expiry absent or rate-limited | False healthy status or missed registration warning | Preserve unknown/error state; bounded retries; TC-004, TC-013 |
| Invalid or expired TLS certificate | Handshake failure hides expiry | Explicit validation failure; controlled endpoint integration in TC-002 |
| Duplicate job execution | Repeated warnings or escalations | Stable keys and durable atomic state; repeat/concurrent-worker tests |
| Acknowledgment races escalation | Unnecessary security notification | Transactional conditional update; acknowledgment and deadline integration tests |
| Provider latency exceeds benchmark | NFR-001 fails | Record latency profile; bounded concurrency and timeout budget; TC-011 |
| Screenshot or generated-code attribution unsupported | Incomplete evidence submission | Preserve provenance; capture actual pages; retain actual Copilot output before marking WP-5.3 complete |

No calendar deadlines or production completion percentages are asserted. The existing Scrum report's 26 planned points describe that captured sprint; they are not an estimate for this complete WBS.
