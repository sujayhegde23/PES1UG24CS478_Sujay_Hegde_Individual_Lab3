# Lab 3: Component Modelling & Architectural Pattern Selection

**Course:** Software Engineering Lab (UE24CS252AA) — Lab 3  
**Assigned System:** Self-Service Coffee Kiosk System  
**Student:** Sujay Hegde | **SRN:** PES1UG24CS478 | **Section:** 4-H  
**Institution:** Department of Computer Science & Engineering, PES University  

---

## 📌 Deliverable Artifacts Index

| Deliverable Item | File Name | Format | Description |
| :--- | :--- | :---: | :--- |
| **UML Component Diagram (High-Res)** | [**`Architecture_Diagram.png`**](./Architecture_Diagram.png) | PNG | Visual component diagram with Presentation, Business, and Data layers, 5 components, and 4 ball-and-socket interfaces. |
| **UML Component Diagram (Vector)** | [**`Architecture_Diagram.pdf`**](./Architecture_Diagram.pdf) | PDF | Scalable vector PDF export of the UML component diagram. |
| **Draw.io Source Model** | [**`Architecture_Diagram.drawio`**](./Architecture_Diagram.drawio) | XML / Draw.io | Fully editable Diagrams.net / Draw.io schema with UML 2 component shapes and connectors. |
| **Written Justification Document** | [**`Architecture_Justification_Document.docx`**](./Architecture_Justification_Document.docx) | Word (.docx) | Official 1-page Word document following the exact student handout structure. |
| **Written Justification Document (PDF)** | [**`Architecture_Justification_Document.pdf`**](./Architecture_Justification_Document.pdf) | PDF | Printable 1-page PDF document with metadata, justification, and component table. |
| **Complete Architecture Specification** | [**`Architecture_Specification.md`**](./Architecture_Specification.md) | Markdown | Detailed technical design document with scenario review, style comparison, security & performance analysis. |
| **Full Specification PDF** | [**`Architecture_Specification.pdf`**](./Architecture_Specification.pdf) | PDF | Compiled full specification report including embedded diagram and tables. |

---

## ☕ UML Component Diagram Preview

![Self-Service Coffee Kiosk System — UML Component Diagram](./Architecture_Diagram.png)

---

## 🏛️ Architecture Selection & Justification Summary

> **Architecture Selection:** *"We chose Layered Architecture for the Self-Service Coffee Kiosk System."*

### 1. Architectural Choice
We selected the classic **3-Tier Layered Architecture** consisting of:
1. **Presentation Layer:** `User Interface Component` (Touch Screen interaction)
2. **Business Layer:** `Order Manager Component`, `Payment Service Component`, and `Receipt Printer Component`
3. **Data Layer:** `Database Component` (Menu, pricing, and audit records)

Each layer encapsulates discrete responsibilities with top-down dependencies, communicating through explicit UML provided (ball) and required (socket) interfaces.

### 2. Two Scenario-Related Reasons
- **Reason 1 — Modularity & Hardware Decoupling:** The kiosk directly interfaces with physical peripherals (touchscreen, EMV credit card reader terminal, and thermal receipt printer). Layered architecture isolates hardware-specific drivers into dedicated components, shielding core ordering domain logic from driver modifications or hardware vendor swaps.
- **Reason 2 — Elimination of Unnecessary Distributed Complexity:** The coffee kiosk is a single autonomous terminal serving customers sequentially. Adopting microservices would add networking latency and distributed failure points, whereas Layered architecture provides ultra-fast in-process IPC calls (<10ms) and straightforward kiosk deployment.

### 3. Security Advantage
- **Strict Layer Isolation & PCI-DSS Protection:** All credit card interactions are encapsulated strictly within the `Payment Service Component`. The Touch Screen UI layer has zero visibility into raw cardholder data buffers or database storage, preventing memory-scraping attacks on the public kiosk terminal.

### 4. Performance Benefit
- **Zero-Network IPC Overhead & In-Memory Pre-fetching:** All components communicate through local IPC or direct in-memory method invocations rather than network hops. Menu data (Espresso, Americano, Latte) and pricing matrices are loaded from the `Database Component` into local memory caches at startup, guaranteeing instant touch responsiveness (<10ms) during peak café rush hours.

---

## 🧩 Summary of System Components & Interfaces

| Component Name | Layer | UML Interfaces (Ball & Socket) | Key Functional Responsibilities |
| :--- | :--- | :--- | :--- |
| **User Interface Component** | Presentation | **Requires:** `Order Interface` (Socket) | Handles touch screen events; presents 3 coffee types (Espresso, Americano, Latte) and 2 drink sizes (Small, Large); displays order and payment status. |
| **Order Manager Component** | Business | **Provides:** `Order Interface` (Ball)<br/>**Requires:** `Payment Interface`, `Receipt Interface`, `Database Interface` (Sockets) | Central domain coordinator; validates selections; calculates order prices with taxes; coordinates payment authorization and receipt dispatch. |
| **Payment Service Component** | Business | **Provides:** `Payment Interface` (Ball) | Hardware abstraction bridge for EMV card reader terminal; enforces Credit Card Only policy; performs PCI-compliant tokenization and approval. |
| **Receipt Printer Component** | Business (HW) | **Provides:** `Receipt Interface` (Ball) | Direct hardware driver connection (ESC/POS protocol); formats itemized receipt slips with order ID and breakdown; monitors paper status. |
| **Database Component** | Data Layer | **Provides:** `Database Interface` (Ball) | Local relational storage (SQLite/JDBC); manages menu items, pricing matrices, and transaction history. |
