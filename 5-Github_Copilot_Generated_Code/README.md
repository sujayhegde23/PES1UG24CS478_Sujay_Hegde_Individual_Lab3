# Code and GitHub Copilot Evidence

**Sujay Hegde | PES1UG24CS478 | BPS #47**

**Copilot evidence status: pending.** No actual GitHub Copilot session, generated output, or screenshot was provided. The code in this folder was authored by Codex as starter material. Its presence does not satisfy the Copilot-specific authorship requirement.

## Runnable starter code

- [Monitoring core](monitoring_core.mjs): expiry policy, bounded lookup retries, asset registry, acknowledgment, escalation, and report fixtures.
- [Unit tests](monitoring_core.test.mjs): threshold boundaries, duplicate alerts, transient/persistent failures, 48-hour deadline, role guards, removed assets, and report completeness.
- [Demo](demo.mjs): fixed sample inputs and collected notification events.

Run with Node.js 20 or newer, without installing dependencies:

```powershell
npm test
npm run demo
```

The prototype uses injected lookup/mail adapters and in-memory state. It does not implement live TLS/WHOIS lookup, an HTTPS dashboard, authentication sessions, persistent storage, a daily/monthly scheduler, concurrent-worker safety, or availability/performance monitoring. Unit fixtures do not establish the full FR/NFR acceptance targets.

## Complete the Copilot deliverable

Use the [prepared Copilot prompt](Copilot_Prompt.md) with GitHub Copilot in your editor on a copy of this starter or a new implementation. Review and test its output, commit the accepted Copilot changes, and save a genuine screenshot or link to that specific code/commit. Record the session in [Copilot_Evidence.md](Copilot_Evidence.md). Retain the original starter's authorship rather than relabeling it.

[Repository folder](https://github.com/sujayhegde23/PES1UG24CS478_Sujay_Hegde_Individual_Lab3/tree/complete/individual-checklist/5-Github_Copilot_Generated_Code) contains the current starter. This link becomes Copilot evidence only after actual Copilot-generated changes and provenance are recorded.
