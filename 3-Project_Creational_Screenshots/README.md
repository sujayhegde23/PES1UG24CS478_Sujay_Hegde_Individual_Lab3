# Lab 2: GitHub and Jira Evidence

**Sujay Hegde | PES1UG24CS478 | BPS #47**
**System:** Domain & SSL Certificate Expiry Alert System

| Evidence | Corrected report | Original screenshots |
| --- | --- | --- |
| Kanban | [Report](jira/Kanban_Evidence_Report.pdf) | Six captures: initial board, requirements, epic hierarchy, work breakdown, and FR-001 details |
| Scrum | [Report](jira/Scrum_Evidence_Report.pdf) | Seven captures: sprint configuration, backlog, hierarchy, active board, scope-change report, and burndown |
| Bug Tracker | [Report](jira/Bug_Tracker_Evidence_Report.pdf) | Two captures: four-defect backlog and BB-1 detail |
| GitHub repository/history | [Screenshots and capture details](github/README.md) | Live repository page and main-branch commit history |

[All 15 original screenshots and their source page numbers](jira/README.md) are available as PNGs. The screenshots were extracted at original dimensions, without changing the Jira content. The student's supplied PDF reports are preserved in [source_reports](jira/source_reports/). Their cover/header SRN placeholders are corrected in the newly generated reports linked above.

## What the evidence establishes

Kanban captures show seven requirements and six scenario epics, with implementation work items in an expanded hierarchy. Scrum captures show sprint setup and reporting; visible sprint work is in To Do. The source report describes 26 planned story points, but the captures do not establish a completed sprint. Bug Tracker shows four Medium-priority defects in To Do and the SSL 15-day alert issue details.

These screenshots document a lab simulation; they do not demonstrate that the monitoring application was implemented or tested.

## Regenerate the corrected reports

After installing the dependencies in `../2-Architectural_Diagram`, run:

```powershell
node generate_evidence_reports.mjs
```

The generator reads `jira/Evidence_Provenance.json` and the existing PNGs. It also exports the Lab 1 one-page use-case specification.
