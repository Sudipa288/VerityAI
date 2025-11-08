# VerityAI
# 🌾 VerityAI — Domain-Specific AI for Agriculture

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-RAG%20Pipeline-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 🚀 Overview

**VerityAI** is a domain-specific **AI system for agriculture**, designed to empower farmers, policymakers, and agri-startups with intelligent, data-driven insights.  
It combines **retrieval-augmented generation (RAG)** with verified agricultural datasets to provide trustworthy, region-aware, and actionable answers.

By integrating data on **government benefits, regional crop varieties, soil conditions, and climate**, VerityAI acts as a smart agricultural assistant that transforms raw data into meaningful knowledge.

---

## 🧠 Core Concept

Agricultural data is often scattered across government portals and research databases.  
VerityAI unifies this information using **AI-powered knowledge retrieval** and **context-aware reasoning**, ensuring users receive accurate, reliable, and region-specific insights.

> “Not just another chatbot — VerityAI is an agricultural knowledge engine.”

---

## 🌾 Key Features

- 🧑‍🌾 **Domain-Specific Intelligence:** Trained on agriculture-exclusive datasets like government schemes and regional crop information.  
- 🔎 **RAG-Powered Insights:** Uses Retrieval-Augmented Generation for precise, explainable answers.  
- 🌦️ **Region-Aware Analysis:** Suggests optimal crops and schemes based on local climate and soil data.  
- 📊 **Decision Support:** Helps with subsidy eligibility, fertilizer planning, and sustainable farming choices.  
- 🔒 **Verified Information:** Relies on authenticated government and open-data agricultural sources.

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| **Language Model** | Gemini 2.5 Flash  / HuggingFace Models |
| **Knowledge Retrieval** | RAG with FAISS / Chroma Vector Store |
| **Backend** | Python (Flask) |
| **Frontend** | Streamlit / React |
| **Data Sources** | Govt. Agri Schemes, Crop & Soil Databases, Regional Weather Patterns |

---

## ⚙️ How It Works

1. **User Query Input:**  
   Example — “What are the government schemes available for rice farmers in West Bengal?”

2. **Retriever System:**  
   The query is embedded and matched with relevant documents from the agricultural dataset.

3. **Context Augmentation:**  
   The retrieved data is added as context for the language model.

4. **Response Generation:**  
   The LLM generates a context-aware, accurate answer.

