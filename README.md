# llm-market-analyst
Got it ✅
Here’s your updated **README.md** with the **Docker section removed** and an emphasis on **local LLM model usage with Ollama + gemma3n**, including installation and download instructions.

---

# Market Metrics Analysis & Ticker App

## 📌 Project Overview

This repository provides a **market analysis toolkit** and a **web-based ticker application** for financial data exploration, **powered by a local LLM model via Ollama (gemma3n)**.

Instead of relying on cloud-based AI APIs, this project uses **locally hosted LLM models** for data analysis and natural language insights.
This makes your workflow **faster, privacy-friendly, and cost-effective**.

The project consists of:

* **`market_analyst.py`** → Core data processing and market analysis functions.
* **`ticker_app.py`** → A Streamlit-powered web interface that uses the **gemma3n local LLM** for insights.
* **`market_metrics_EDA.ipynb`** → Jupyter Notebook for exploratory data analysis (EDA) on market metrics.
* **`requirements.txt`** → Dependency list to replicate the environment.

---

## 🚀 Features

* Fetch live & historical market data using **Yahoo Finance (yfinance)**.
* Run **natural language analysis** on market metrics with a **local LLM**.
* Fully offline inference — **no API key required**.
* Interactive UI for exploring tickers and AI-generated insights.
* Ready-to-use **exploratory data analysis notebook** for research.

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/market-metrics.git
cd market-metrics
```

### 2. Install Python Dependencies

```bash
python3 -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Install Ollama

Ollama lets you run large language models **locally** on your machine.

#### macOS

```bash
brew install ollama
```

#### Windows

Download the installer from:
👉 [https://ollama.com/download](https://ollama.com/download)

#### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

---

## 📥 Download the gemma3n Model

Once Ollama is installed, pull the **gemma3n** model:

```bash
ollama pull gemma3n
```

Verify installation:

```bash
ollama list
```

You should see `gemma3n` in the list.

---

## ▶️ Usage

### 1. Start the Ollama Service

Ollama needs to be running in the background:

```bash
ollama serve
```

### 2. Run the Web App

```bash
streamlit run ticker_app.py
```

* Opens in your browser at `http://localhost:8501`.
* Enter stock tickers, adjust parameters, and get **AI-assisted market insights**.

### 3. Run Market Analysis from CLI

```bash
python market_analyst.py
```

This will process market data and return both numeric analysis and **LLM-generated summaries**.

### 4. Explore EDA in Jupyter Notebook

```bash
jupyter notebook market_metrics_EDA.ipynb
```

---

## ⚙️ Configuration

* **`ticker_app.py`** → UI defaults & AI prompts.
* **`market_analyst.py`** → Analysis logic & data pipeline.
* Modify the Ollama model name in the code if you want to try a different local model.

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file.

---

Do you want me to also **add a "Local LLM Prompt Examples" section** in the README so users know exactly what kind of market-related questions they can ask gemma3n? That would make the README more engaging for non-technical users.

