from llm_helper import ask_gemini

print("=== Testing Gemini LLM Integration ===")

# Test 1: Ask a valid question from the knowledge base
print("\nTest 1: Asking a known question (Delivery charge)")
q1 = "What is the delivery charge for Dhaka?"
print(f"User: {q1}")
res1 = ask_gemini(q1)
if res1["success"]:
    print(f"AI: {res1['reply']}")
else:
    print(f"Error: {res1['error']}")

# Test 2: Ask something outside the knowledge base (Hallucination test)
print("\nTest 2: Asking an unknown question (Do you deliver to USA?)")
q2 = "Do you deliver to USA?"
print(f"User: {q2}")
res2 = ask_gemini(q2)
if res2["success"]:
    print(f"AI: {res2['reply']}")
    if "I'm sorry" in res2['reply'] or "don't have that information" in res2['reply']:
        print("[OK] AI correctly refused to answer outside its knowledge.")
    else:
        print("[WARNING] AI might have hallucinated.")
else:
    print(f"Error: {res2['error']}")

print("\n=== LLM Test Complete ===")
