from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"

def load_knowledge_base():
    knowledge = {}
    if not KNOWLEDGE_DIR.exists():
        return knowledge
    for file_path in KNOWLEDGE_DIR.glob("*.md"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                knowledge[file_path.stem] = file.read()
        except Exception as e:
            print(f"Error reading {file_path.name}: {e}")
    return knowledge

def search_faq(question: str):
    question_lower = question.lower()
    kb = load_knowledge_base()

    if any(word in question_lower for word in ["delivery", "ship", "charge", "time", "ডেলিভারি"]):
        return kb.get("delivery", "Delivery information not found.")
    elif any(word in question_lower for word in ["return", "refund", "money back", "ফেরত", "রিফান্ড"]):
        return kb.get("return_policy", "Return policy not found.")
    elif any(word in question_lower for word in ["payment", "pay", "bkash", "nagad", "card", "পেমেন্ট"]):
        return kb.get("payment", "Payment information not found.")
    elif any(word in question_lower for word in ["warranty", "guarantee", "ওয়ারেন্টি"]):
        return kb.get("warranty", "Warranty information not found.")
    elif any(word in question_lower for word in ["order", "help", "contact", "অর্ডার"]):
        return kb.get("faq", "FAQ not found.")
    return None
