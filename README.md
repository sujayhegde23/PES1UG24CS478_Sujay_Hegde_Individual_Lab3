# Software Engineering Labs - Sujay Hegde

**SRN:** PES1UG24CS478
**Institution:** PES University, Department of Computer Science & Engineering

| Lab | Scenario | Deliverables |
| --- | --- | --- |
| 1 - Requirements Engineering | BPS #47: Domain & SSL Certificate Expiry Alert System | [Requirements](1-RE/Requirements.md), [RTM](1-RE/RTM_Table.md), [RTM PDF](1-RE/RTM_Table.pdf), [use-case diagram](1-RE/UseCaseDiagram.md), [one-page flow specification](1-RE/UseCaseSpecification.pdf) |
| 2 - Jira Project Setup | BPS #47: Domain & SSL Certificate Expiry Alert System | [Original Jira screenshots and evidence reports](3-Project_Creational_Screenshots/README.md) |
| 3 - Component Modelling | Self-Service Coffee Kiosk System | [Component diagram, editable source, and one-page justification](2-Architectural_Diagram/README.md) |
| 4 - SRS and Work Breakdown | BPS #47: Domain & SSL Certificate Expiry Alert System | [SRS](4-SRS_and_Work_Breakdown_Steps/SRS_Document.md), [WBS](4-SRS_and_Work_Breakdown_Steps/Work_Breakdown_Structure.md), [combined PDF](4-SRS_and_Work_Breakdown_Steps/SRS_and_Work_Breakdown_Steps.pdf) |
| 5 - Code and Copilot Evidence | BPS #47: Domain & SSL Certificate Expiry Alert System | [Runnable starter, tests, and prepared Copilot prompt](5-Github_Copilot_Generated_Code/README.md); actual Copilot provenance pending |

The Lab 3 handout describes the coffee kiosk scenario and gives Order Manager and Payment Service as starting components. The reference repository uses that scenario too. Accordingly, Lab 3 uses the coffee kiosk while Labs 1 and 2 retain BPS #47.

```text
PES1UG24CS478_Sujay_Hegde_Individual_Lab3/
├── 1-RE/
├── 2-Architectural_Diagram/
│   ├── Architecture_Diagram.drawio
│   ├── Architecture_Diagram.svg / .png / .pdf
│   ├── Architecture_Justification_Document.docx / .pdf
│   └── Architecture_Specification.md / .pdf
├── 3-Project_Creational_Screenshots/
│   ├── github/
│   └── jira/
├── 4-SRS_and_Work_Breakdown_Steps/
└── 5-Github_Copilot_Generated_Code/
```

![Coffee kiosk UML component diagram](2-Architectural_Diagram/Architecture_Diagram.png)
Run `npm test` inside `5-Github_Copilot_Generated_Code` to execute the 12 unit tests. These cover injected lookup fixtures, expiry thresholds, retries, alert lifecycle, registry mutation, role checks, and summary completeness. They do not certify the full production FR/NFR targets. The RTM records the remaining integration, performance, security, and availability procedures.
