# ShopEasy AI Support Agent 🛍️🤖

An intelligent E-commerce Customer Support Chatbot built with **FastAPI**, **Google Gemini API**, and a custom **RAG (Retrieval-Augmented Generation)** pipeline.

## 🚀 Features
- **Context-Aware Answers:** Uses local .md knowledge base (delivery.md, eturn_policy.md, etc.) to answer accurately.
- **Gemini 3.5 Flash Integration:** Fast and cost-effective AI responses.
- **Modern UI:** Clean, responsive chat interface (HTML/CSS/JS).
- **CORS Enabled:** Secure communication between frontend and backend.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, Uvicorn
- **AI/LLM:** Google Gemini API (gemini-3.5-flash-lite)
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Tools:** dotenv, Pydantic

## ⚙️ How to Run Locally
1. Clone the repository:
   \\\ash
   git clone https://github.com/your-username/ecommerce-support-agent.git
   cd ecommerce-support-agent
   \\\
2. Create and activate a virtual environment:
   \\\ash
   python -m venv venv
   .\venv\Scripts\activate
   \\\
3. Install dependencies:
   \\\ash
   pip install -r requirements.txt
   \\\
4. Add your API key in \.env\:
   \\\env
   GEMINI_API_KEY=your_api_key_here
   \\\
5. Start the server:
   \\\ash
   uvicorn main:app --reload
   \\\
6. Open \http://127.0.0.1:8000\ in your browser.

## 📸 Screenshots
*(Add a screenshot of your chatbot here)*

## 📄 License
MIT License
