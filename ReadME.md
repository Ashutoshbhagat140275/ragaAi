# RagaAI: Multi-Agent Financial Market Assistant

## Overview

RagaAI is a multi-source, multi-agent finance assistant that delivers spoken market briefs and answers to user questions via a Streamlit web app. It leverages advanced data-ingestion pipelines (APIs, web scraping, document loaders), indexes embeddings in a vector store for Retrieval-Augmented Generation (RAG), and orchestrates specialized agents (API, scraping, retrieval, analytics, LLM, voice) via FastAPI microservices. Voice I/O is powered by open-source toolkits, and text agents are built with frameworks like LangGraph and CrewAI.

---

## Features

- **Multi-source Data Ingestion:** Fetches real-time and historical stock data from APIs (e.g., yfinance), web scraping, and document loaders.
- **Vector Store & RAG:** Embeds and indexes financial data in a Chroma vector database for efficient retrieval and context-aware answers.
- **Agent Orchestration:** Specialized agents handle API calls, scraping, analytics, LLM reasoning, and voice I/O.
- **Voice Interaction:** Converts answers to speech using gTTS and plays them in the Streamlit frontend.
- **Modular Microservices:** FastAPI backend exposes endpoints for data ingestion, question answering, and more.
- **Open Source & Extensible:** All code is open-source and documented for easy extension and deployment.

---

## Project Structure

```
RagaAi/
│
├── backend/
│   └── fastapi1.py         # FastAPI backend with data ingestion, RAG, and agent orchestration
│
├── frontend/
│   └── streamlit1.py       # Streamlit frontend for user interaction and voice output
│
├── chroma/                 # Chroma vector database files (auto-generated)
│
├── ReadME.md               # Project documentation
└── requirements.txt        # Python dependencies
```

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd RagaAi
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Run the FastAPI Backend

```sh
cd backend
uvicorn fastapi1:app --reload
```

### 4. Run the Streamlit Frontend

Open a new terminal:

```sh
cd frontend
streamlit run streamlit1.py
```

---

## Usage

- **Add Data:** Use the "add_data" button in the Streamlit app to fetch and store the latest stock data.
- **Ask Questions:** Enter your financial question in the Streamlit app. The system will retrieve relevant context and generate a spoken answer.
- **Voice Output:** Answers are converted to speech and played automatically in the browser.

---

## Technologies Used

- **FastAPI**: Backend microservices
- **Streamlit**: Frontend web app
- **yfinance, nsetools**: Financial data ingestion
- **Chroma**: Vector database for RAG
- **LangGraph, CrewAI**: Agent orchestration (can be extended)
- **gTTS**: Text-to-speech for voice output
- **deep-translator**: Language translation
- **Google Generative AI**: LLM for answer generation

---

## Logging & Documentation

- All AI-tool usage and agent actions are logged for transparency.
- Code is modular and documented for easy understanding and extension.

---

## License

This project is open-source and available under the MIT License.

---

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [Chroma](https://www.trychroma.com/)
- [gTTS](https://pypi.org/project/gTTS/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [CrewAI](https://github.com/joaomdmoura/crewAI)

---

**For questions or contributions, please open an issue or pull request on GitHub.**