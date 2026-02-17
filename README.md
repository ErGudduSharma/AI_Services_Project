# 🤖 Intelligent AI Services Suite

A stateful, multi-agent workflow engine built with **LangGraph**, **Google Gemini Pro**, and **FastAPI**. This system transforms unstructured business requests into structured, validated, and synthesized solutions through an autonomous agentic pipeline.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangGraph-Strategic-blue?style=for-the-badge)
![Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange?style=for-the-badge&logo=google-gemini)

## 🚀 Key Features

- **Autonomous Planning**: Naturally understands complex business intents and crafts an execution plan.
- **AI-Driven Data Extraction**: Uses LLMs to extract entities (IDs, Amounts) from raw conversational text.
- **Stateful Orchestration**: Powered by LangGraph to maintain context across multiple specialized agents.
- **Deterministic Guardrails**: Combines AI reasoning with hard-coded validation logic for security and compliance.
- **Premium Dashboard**: A split-view animated UI showing the real-time "thinking process" and final solution.

## 🏗️ Architecture Workflow

1.  **Request Reception**: FastAPI captures the user request via a POST endpoint.
2.  **Planner**: Gemini Pro generates a list of logical steps.
3.  **Extractor**: The engine converts unstructured text into a JSON state (Customer ID, Amount, status).
4.  **Validator**: Checks the data against business rules (e.g., Amount < 100k).
5.  **Approver**: Finalizes the status based on validation flags.
6.  **Synthesizer**: Gemini Pro summarizes the entire journey into a professional response.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **Orchestration**: LangGraph (StateGraph)
- **AI Model**: Google Gemini 1.5 Flash (via `google-generativeai`)
- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (Glassmorphism), Marked.js

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ErGudduSharma/AI_Services_Project.git
   cd AI_Services_Project
   ```

2. **Set up Environment Variables**:
   Create a `.env` file and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn app:app --reload
   ```

5. **Access the Dashboard**:
   Open `http://127.0.0.1:8000` in your browser.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

---
Built with ❤️ by [ErGudduSharma](https://github.com/ErGudduSharma)
