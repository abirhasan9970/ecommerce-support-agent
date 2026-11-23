from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_helper import get_ai_response

app = FastAPI()

# CORS সেটআপ
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# স্ট্যাটিক ফোল্ডার মাউন্ট করা
app.mount("/static", StaticFiles(directory="static"), name="static")

# রুট (/) এ গেলে index.html দেখানোর জন্য
@app.get("/")
async def read_index():
    return FileResponse("static/frontend/index.html")

class ChatRequest(BaseModel):
    message: str

# চ্যাট এন্ডপয়েন্ট (একটিই থাকবে)
@app.post('/chat')
async def chat_with_bot(request: ChatRequest):
    try:
        bot_reply = get_ai_response(request.message)
        return {'reply': bot_reply}
    except Exception as e:
        return {'reply': f'Server Error: {str(e)}'}
