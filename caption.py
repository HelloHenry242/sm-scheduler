import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class CaptionGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None

    def generate(self, topic):
        if not self.api_key or not self.model:
            return "Error: Gemini API Key is missing. Check your .env file."
        try:
            prompt = f"Write a catchy social media caption and 3 relevant hashtags for: {topic}"
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error: Could not generate caption. Details: {e}"