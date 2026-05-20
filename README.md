# Gemini Clone - Automated DevOps Pipeline

This project is a monolithic Python web application featuring a frontend interface modelled after Google Gemini, powered by a Large Language Model (LLM) backend via OpenRouter. 

It acts as the vehicle for demonstrating a fully automated DevOps Server Pipeline (CI/CD) for **SWE40006 Software Deployment and Evolution**.

## 👥 Team Members
* Ashley Jong (102780087)
* Daniel Tiong (102777801)

## 🛠️ Technology Stack
* **Frontend:** HTML, CSS, JavaScript (Vanilla, no build tools required)
* **Backend:** Python, FastAPI, Uvicorn
* **AI Integration:** OpenRouter API (google/gemini-3.5-flash)
* **CI/CD Pipeline:** GitHub Actions, Vercel
* **Testing:** Pytest
* **Dependency Management:** `uv`

## 🚀 DevOps Pipeline Architecture
This repository implements a 4-tier DevOps pipeline:

1. **Level 1 (Pipeline):** Source code is maintained on GitHub. Pushes trigger GitHub Actions (CI server) to run automated tests. Upon passing, code is automatically deployed to a Vercel Production server. Pull Requests automatically deploy to a Vercel Test Server (Preview Deployments).
2. **Level 2 (Instrumentation):** Vercel Web Analytics is injected into the production build to gather live visitor and performance statistics.
3. **Level 3 (Verification):** The monolithic application is fully functional, capable of interacting with the LLM API, and maintains conversation context dynamically.
4. **Level 4 (Automation):** Any pushes to the `main` branch that pass the `pytest` suite automatically trigger a deferred deployment build on Vercel without manual intervention.

## 💻 Local Development Setup

We use `uv` for lightning-fast dependency management.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/devops-llm-app.git
   cd devops-llm-app
   ```

2. **Setup environment variables:**
   Create a `.env` file in the root directory and add your OpenRouter API key:
   ```env
   OpenRouter-API-Keys=your_api_key_here
   ```

3. **Install dependencies and start the server:**
   ```bash
   uv sync
   uv run uvicorn api.index:app --reload
   ```
   *The application will be available at `http://127.0.0.1:8000/`*

## 🧪 Automated Testing
To run the automated integration and unit test suite locally:
```bash
uv run pytest test_app.py -v
```
This tests the frontend delivery, backend state management, error handling, and real API connectivity to the LLM.
