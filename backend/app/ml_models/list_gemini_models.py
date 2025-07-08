# Purpose: List all available Gemini models and their supported generation methods.
# Usage: Running this script will show the available models and their capabilities that the API key supports..





import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

models = genai.list_models()
for model in models:
    print(f"{model.name} | supported generation methods: {model.supported_generation_methods}")
