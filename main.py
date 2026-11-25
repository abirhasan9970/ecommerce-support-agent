from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm_helper import get_ai_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/frontend/index.html")

class ChatRequest(BaseModel):
    message: str

@app.post('/chat')
async def chat_with_bot(request: ChatRequest):
    try:
        bot_reply = get_ai_response(request.message)
        return {'reply': bot_reply}
    except Exception as e:
        return {'reply': f'Server Error: {str(e)}'}
