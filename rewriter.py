import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Initialize the client using the new SDK
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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

def rewrite_content(title: str) -> str | None:
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Topic: {title}\n\n{PROMPT}",
            config=types.GenerateContentConfig(
                temperature=0.7,
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating content for {title}: {e}")
        return None
