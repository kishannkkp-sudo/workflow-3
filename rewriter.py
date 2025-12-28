import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT = """
Write a completely ORIGINAL job information article.

Rules:
- DO NOT copy content from any website
- DO NOT mention source websites
- Use your own wording
- Adsense safe
- SEO friendly
- Informational tone

Structure:
- SEO Title
- Introduction
- Key Job Details (table)
- Eligibility
- Selection Process
- How to Apply
- Important Dates
- Disclaimer
"""

def rewrite_content(title: str) -> str:
    model = genai.GenerativeModel("gemini-flash-latest")
    res = model.generate_content(f"Topic: {title}\n\n{PROMPT}")
    return res.text.strip()
