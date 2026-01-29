# Academic Assistant Agent

## Overview

**Academic Assistant Agent** is a conversational system capable of:

- Answering academic questions using structured reasoning and retrieved documentation
- Executing academic actions (such as enrollments and grade registration) through external tools
- Autonomously deciding whether a user request is **informational** or **action-oriented**

The system is designed to strictly separate **reasoning** from **actions**, ensuring safety, determinism, and extensibility.

---

## Key Capabilities

### Informational Queries
The agent can answer questions such as:

- *Can John Doe enroll in Physics II?*
- *What are the requirements to enroll in a course?*
- *Why is a student not eligible for enrollment?*

These queries are handled through a **centralized informational graph** that combines:

- **Knowledge Graph (KG)** — deterministic reasoning over academic data
- **RAG (Retrieval-Augmented Generation)** — academic rules and policies

---

### Action Requests
The agent can execute actions such as:

- Enrolling a student in a course
- Registering a grade for a student

All actions are executed **exclusively** through an **MCP Server**, which enforces academic rules and protects database integrity.

Examples:

- *Enroll John Doe in Math I for year 2025*
- *Register grade 7 in Physics I for John Doe for 2025*

---

## High-Level Architecture

```
User
 ↓
CLI / Chat UI
 ↓
Router Agent (LLM)
 ├─ Informational Strategy
 │   └─ Informational Graph (LangGraph)
 │       ├─ Entity Extraction
 │       ├─ Knowledge Graph Reasoning
 │       ├─ RAG (Academic Rules)
 │       └─ Synthesis
 │
 └─ Action Strategy
     └─ Entity Resolution (strict)
         └─ MCP Server (FastAPI)
             └─ SQLite Database
```

---

## Routing Logic

The **Router Agent** (LLM-based) decides autonomously whether a user request is:

- **Informational**
- **Action-oriented**

No keyword-based routing or manual `if/else` logic is used.

---

## Informational Graph

The informational pipeline is implemented using **LangGraph** and follows a fixed, centralized flow:

1. **Entity Extraction**
2. **Knowledge Graph Reasoning**
3. **RAG**
4. **Synthesis**

---

## MCP Server (Actions)

The action layer is implemented as an **MCP Server using FastAPI**.

### Design Principles

- The MCP Server is the **only mechanism** allowed to perform actions
- It does **not trust the LLM**
- All business rules are revalidated defensively
- The MCP layer protects database integrity

---

## Database

- SQLite is used for simplicity and portability
- The source of truth is clearly defined:
  - Academic results → `grade`
  - Enrollments → `enrollment`
  - Academic status → `student`

---

## Project Structure

```
academic-assistant-agent/
├─ src/
│  ├─ infrastructure/
│  ├─ response/
│  │  ├─ action/
│  │  │  └─ mcp/
│  │  ├─ agent/
│  │  ├─ informational/
│  │  └─ strategies/
│  └─ ui/
├─ main.py
├─ requirements.txt
├─ .env
└─ README.md
```

*(Folders are listed in alphabetical order to match VS Code explorer view.)*

---

## Running the Project

### 1. Setup environment

```bash
python -m venv .venv_aag
source .venv_aag/bin/activate  # Windows: .venv_aag\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file:

```
OPENAI_API_KEY=your_key_here
DB_PATH=path_to_sqlite_db
RULES_PATH=path_to_academic_rules.md
```

### 3. Start the MCP API server

```bash
uvicorn src.response.action.mcp.server:app --reload
```

### 4. Start the chat interface

```bash
python main.py
```

---

## Design Decisions

- Strict separation between reasoning and actions
- Deterministic validation at the MCP layer
- LLMs are advisors, never authorities

---

## Test Data Available (Initial Database State)

> **Note:** The following subsection describes the **entire initial dataset** available in the database for testing purposes. All examples and expected behaviors in this project are based on this predefined data.

To facilitate evaluation and manual testing, the database is preloaded with a **small but coherent academic dataset**.
The following data is available at startup:

### Students
The system contains four students with different academic statuses:

- **John Doe** — REGULAR  
  (Has already passed *Math I*)
- **John McClane** — REGULAR  
  (No enrollments or grades yet)
- **Jane Smith** — REGULAR  
  (Currently enrolled in *Physics I*)
- **Mark Brown** — FREE  
  (Cannot enroll in new courses)

---

### Professors
Two professors are available and assigned to courses:

- **Dr. Albert Newton** — teaches *Math I*
- **Dr. Marie Curie** — teaches *Physics I* and *Physics II*

---

### Subjects
The academic curriculum includes three subjects:

- **Math I**
  - Level: 1
  - Term: 1
- **Physics I**
  - Level: 1
  - Term: 2
- **Physics II**
  - Level: 2
  - Term: 1

---

### Courses (Year 2025)
Each subject has an associated course for the academic year **2025**:

- *Math I (2025)* — taught by Dr. Albert Newton
- *Physics I (2025)* — taught by Dr. Marie Curie
- *Physics II (2025)* — taught by Dr. Marie Curie

---

### Prerequisites (Correlativities)
The following prerequisite rules are enforced:

- **Physics I** requires **Math I**
- **Physics II** requires **Physics I**

These rules are used by both the Knowledge Graph (for reasoning)
and the MCP Server (for defensive validation).

---

### Enrollments
Initial enrollments are:

- **John Doe** is enrolled in *Math I (2025)*
- **Jane Smith** is enrolled in *Physics I (2025)*

---

### Grades
The following grade has already been registered:

- **John Doe**
  - Subject: *Math I*
  - Score: 8.0
  - Result: **PASSED**

This allows testing prerequisite-based eligibility, for example:
- John Doe **can** enroll in *Physics I*
- John Doe **cannot** enroll in *Physics II* (missing *Physics I*)

---

This dataset is intentionally minimal and deterministic,
making it suitable for validating both **informational reasoning**
and **action execution** without ambiguity.


---

## Supported Functionalities

This PoC intentionally supports a **limited and explicit set of academic functionalities**.
Any request outside these capabilities is handled gracefully and never guessed.

### Knowledge Graph (Informational)

The Knowledge Graph currently supports:

- Enrollment eligibility evaluation  
  - Determines whether a student can enroll in a subject
  - Considers:
    - Student academic status
    - Approved prerequisite subjects
- Explanatory academic reasoning  
  - Provides clear reasons when enrollment is not allowed
- Academic rules consultation  
  - Uses RAG to retrieve and cite enrollment policies

The KG **does not** currently support:

- Listing enrollments
- Listing grades
- Professor or course assignment queries
- Aggregations or reporting queries

---

### MCP Server (Actions)

The MCP Server supports the following actions only:

#### enroll_student
- Enrolls a student in a course for a given year
- Validates:
  - Student existence
  - Academic status (REGULAR)
  - Subject and course existence
  - Duplicate enrollments
  - Prerequisite fulfillment (based on approved grades)

#### register_grade
- Registers a grade for an existing enrollment
- Validates:
  - Enrollment existence
  - Score range
  - Prevention of re-grading approved enrollments

No other academic actions are supported in this version.


---

## Proof of Concept Notes

This project is implemented as a **Proof of Concept (PoC)**.

For transparency and ease of understanding during evaluation and testing, the CLI intentionally prints
additional internal information on each user request:

```python
print(f"[Decision] Route: {decision.route.value}")
print(f"[Reason] {decision.reason}")
```

These logs allow observers to clearly see:

- Which route was selected by the Router Agent (**informational** vs **action**)
- The LLM-generated reasoning behind that routing decision

These prints are meant for debugging and demonstration purposes only and would typically be
removed or replaced by structured logging in a production-ready system.


---

## Final Notes

This project demonstrates how to build a **safe, extensible, and well-structured AI agent**
that combines LLM-based reasoning with deterministic systems without compromising data integrity.
