from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS মিডলওয়্যার (ব্রাউজার থেকে রিকোয়েস্ট পাঠানোর জন্য অত্যন্ত জরুরি)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# স্ট্যাটিক ফাইল (CSS, JS, ছবি) সার্ভ করার জন্য
app.mount("/static", StaticFiles(directory="static"), name="static")

# মূল পেজে index.html দেখানোর জন্য
@app.get("/")
async def read_index():
    return FileResponse("static/frontend/index.html")

# ---------------------------------------------------------
# এখানে তোমার চ্যাট API এন্ডপয়েন্টটি থাকবে। 
# ধরো তোমার script.js এ fetch('/chat') বলা আছে, তাহলে নিচের মতো হবে:

# @app.post("/chat")
# async def chat_endpoint(user_message: dict):
#     # এখানে তোমার Gemini API কল করার লজিক থাকবে
#     return {"response": "This is a dummy response"}

# ---------------------------------------------------------