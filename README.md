# Project_1: Industrial AI Hub

This repository contains a unified **Industrial AI Hub** designed for resource-efficient, hardware-aware MLOps on Intel-based systems (specifically i7-1195G7).

## 🚀 Key Components

1.  **Industrial MCP Hub (`industrial_mcp/`)**:
    - **Backend (`app.py`)**: FastAPI server providing real-time APIs for system monitoring and AI analysis.
    - **Live Dashboard (`dashboard/`)**: A premium, interactive web interface for factory-floor monitoring and AI expert consultation.
    - **RAG Agent (`industrial_agent.py`)**: A LangChain-powered agent that combines Multimodal Vision (Gemini) with a local Technical Manual (RAG).
    - **Hardware Guard**: Integrated logic to manage RAM and use OpenVINO for Intel CPU acceleration.

2.  **AI Engine Integration**:
    - Supports **OpenVINO** for optimized inference.
    - Uses lightweight **YOLOv8n (Nano)** for vision tasks to maintain system stability.

## 🛠️ Getting Started

1.  Clone the repository.
2.  Install dependencies: `pip install -r industrial_mcp/requirements.txt`.
3.  Set your `GOOGLE_API_KEY` for Multimodal RAG.
4.  Run the backend: `python industrial_mcp/app.py`.
5.  Open `http://localhost:8000/live.html` in your browser.

## 🏛️ Architecture

The project follows a **Sense-Think-Act** loop, where raw data is sensed by vision models, processed with architectural knowledge (RAG), and acted upon via the dashboard or automated CAD triggers.
