import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def read_knowledge_base():
    knowledge_text = ""
    # knowledge ????????? ?? .md ???? ???
    if os.path.exists("knowledge"):
        for filename in os.listdir("knowledge"):
            if filename.endswith(".md"):
                with open(os.path.join("knowledge", filename), "r", encoding="utf-8") as f:
                    knowledge_text += f"\n--- {filename} ---\n" + f.read()
    return knowledge_text

def get_ai_response(user_message):
    try:
        context = read_knowledge_base()
        
        # ???-?? ??????? ????? ????? ?????? ????? ???? ???
        prompt = f"""You are a helpful E-commerce Customer Support AI for 'ShopEasy'. 
Use the following company knowledge base to answer the user's question accurately. 
If the answer is not in the knowledge base, politely say you don't know.
Keep your answers concise and friendly. You can reply in English or Bengali based on the user's language.

KNOWLEDGE BASE:
{context}

USER QUESTION: {user_message}
"""
        # ???? ?? ???
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite', # ????? ?????? ??? (gemini-3.5-flash-lite ?? flash-lite)
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
