import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your API key from the .env file
load_dotenv()

class CaptionGenerator:
    def __init__(self, api_key=None):
        # If no key is provided, it tries to grab it from the environment
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate(self, topic):
        """
        Sends a prompt to Gemini and returns the generated caption.
        """
        try:
            prompt = f"Write a catchy social media caption and 3 relevant hashtags for: {topic}"
            
            response = self.model.generate_content(prompt)
            
            return response.text.strip()

        except Exception as e:
            # Simple error handling to prevent the app from crashing
            return f"Error: Could not generate caption. Details: {e}"