from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import traceback

# আপনার llm_helper ফাইল থেকে ফাংশনটি ইম্পোর্ট করুন
from llm_helper import get_ai_response 

app = FastAPI()

# ১. CORS মিডলওয়্যার (এরর সমাধানের জন্য অত্যন্ত জরুরি)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ২. স্ট্যাটিক ফাইল সার্ভ করা
app.mount("/static", StaticFiles(directory="static"), name="static")

# ৩. মূল UI পেজ রেন্ডার করা
@app.get("/")
async def read_index():
    return FileResponse("static/frontend/index.html")

# ৪. চ্যাট রিকোয়েস্টের ডেটা ফরম্যাট (Pydantic Model)
class ChatRequest(BaseModel):
    message: str

# ৫. চ্যাট API এন্ডপয়েন্ট (কমেন্ট আউট করা ছিল, এটি এখন সচল)
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # llm_helper.py থেকে AI উত্তর জেনারেট করা
        ai_reply = get_ai_response(request.message)
        return {"reply": ai_reply}
    except Exception as e:
        # কোনো এরর হলে টার্মিনালে প্রিন্ট হবে এবং ক্লায়েন্টকে জানানো হবে
        print(f"Error in chat endpoint: {e}")
        traceback.print_exc()
        return {"reply": f"Server Error: {str(e)}"}