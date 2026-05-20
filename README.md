# Gemini Clone - Automated DevOps Pipeline

This project is a monolithic Python web application featuring a frontend interface modelled after Google Gemini web application, powered by a Large Language Model (LLM) backend via OpenRouter. 

It acts as the vehicle for demonstrating a fully automated DevOps Server Pipeline (CI/CD).

---

### DevOps Pipeline Architecture
This repository implements a 4-tier DevOps pipeline:

1. **Level 1 (Pipeline):** Source code is maintained on GitHub. Pushes trigger GitHub Actions (CI server) to run automated tests. Upon passing, code is automatically deployed to a Vercel production server. Pull Requests automatically deploy to a Vercel test server (Preview Deployments).
2. **Level 2 (Instrumentation):** Vercel Web Analytics is injected into the production build to gather live visitor and performance statistics.
3. **Level 3 (Verification):** The monolithic application is fully functional, capable of interacting with the LLM API and maintains conversation context dynamically.
4. **Level 4 (Automation):** Any pushes to the `main` branch that pass the `pytest` suite automatically trigger a deferred deployment build on Vercel without manual intervention.