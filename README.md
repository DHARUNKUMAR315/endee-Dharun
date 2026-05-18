---
title: AI Ticket Router
emoji: 🎟️
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# AI Powered Intelligent Ticket Routing & Resolution Agent

A production-ready, Full-Stack Agentic AI Support Assistant that intelligently routes, escalates, and resolves IT Service issues using Semantic Vector Search. Built natively on top of the **Endee C++ Matrix Engine** running effortlessly inside Docker. 

## 🔥 Key SaaS Interface Features
- **Semantic Classification & Routing:** Uses `SentenceTransformers` (`all-MiniLM-L6-v2`) to route unstructured IT issues directly to the right department.
- **Agentic Confidence Thresholds:** Automatically detects ambiguity and intelligently escalates (Hold/Progress) vs instantly resolves (Complete).
- **Multi-Departmental Dashboards:** Dedicated analytics pages for **Network, Security, Application, Database, and Infrastructure** telemetry with simulated historic volume metrics.
- **User Profile State:** Retains session history of individual user ticket queries across multi-page traversals using stateful tracking.
- **Complete Dockerization:** Both the Endee database and the Streamlit Interface run side-by-side in seamlessly bridged containers.

---

## 🛠️ One-Click Deployment (Local)

The entire backend and user interface is fully containerized! Follow these simple steps to run the enterprise suite natively on your machine:

### 1. Build & Launch the Full Stack
From the root of the repository (where `docker-compose.yml` is located), command Docker to build the Python AI environment and deploy the Endee database:
```bash
docker compose up -d --build
```
*(Note: Initial build may take 1-3 minutes to download PyTorch and required Machine Learning libraries into the container).*

### 2. Procedural Data Ingestion
Because the Endee Docker container starts fresh, you must seed it with the historical enterprise knowledge base. Run the ingestion pipeline to index the 1,000 synthetic tickets:
```bash
cd demo/ticket_agent
python data_pipeline.py
```

### 3. Launch the AI Dashboard
Docker has already exposed your custom SaaS container! Simply open your browser to interact with the Cognitive Routing Engine at:
👉 **http://localhost:8504**

---

## 🧠 System Architecture

1. **User Input:** Employee submits a messy, unstructured IT issue.
2. **PII & Sentiment Analysis:** Evaluates stress lexicons (e.g. *“urgent”*, *“server crashed”*) to bypass generic queues and upgrade priority dynamically.
3. **Encoding Pipeline:** `MiniLM` maps the complex issue to a 384-dimensional dense math vector.
4. **Endee Engine Search:** Identifies similar historic hardware/software footprints stored in the unified vector database.
5. **Agentic Router Decision:**
    - `> 85% Match:` **Autonomous Resolution** (Instantly closed without human intervention).
    - `30% - 85% Match:` **Routed to Human Dept** (With AI workflow recommendations generated in UI).
    - `< 30% Match:` **Manual Escalation** (Ambiguity override sent to Tier 2).
