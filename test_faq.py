from faq_helper import search_faq

print("--- Testing FAQ Search ---")
q1 = "What is the delivery charge?"
print(f"Q: {q1}")
print(f"A: {search_faq(q1)}")

q2 = "Can I return a product?"
print(f"Q: {q2}")
print(f"A: {search_faq(q2)}")
