import sys
import os
import importlib
from dotenv import load_dotenv

print("=== Checking Environment and Dependencies ===")

# 1. Check Python Version
if sys.version_info >= (3, 10):
    print(f"[OK] Python version is {sys.version.split()[0]} (10 or higher is required)")
else:
    print(f"[ERROR] Python version is too old: {sys.version.split()[0]}. Please upgrade.")

# 2. Check Required Packages
required_packages = ["fastapi", "uvicorn", "google.genai", "dotenv"]
for package in required_packages:
    try:
        # Handle google.genai import mapping
        if package == "google.genai":
            importlib.import_module("google.genai")
        else:
            importlib.import_module(package)
        print(f"[OK] Package installed: {package}")
    except ImportError:
        print(f"[ERROR] Package missing: {package}. Run 'pip install {package}'")

# 3. Check .env and API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[ERROR] GEMINI_API_KEY not found in .env file.")
elif api_key == "your_gemini_api_key_here":
    print("[WARNING] GEMINI_API_KEY is still the placeholder. AI features will not work.")
else:
    print("[OK] GEMINI_API_KEY is configured.")

print("=== Check Complete ===")
