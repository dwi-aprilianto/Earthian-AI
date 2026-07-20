import os
from dotenv import load_dotenv
from google import genai

# 1. Load variabel environment
load_dotenv()

# 2. Inisialisasi Client (Syntax Baru)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Model yang tersedia untuk API Key kamu:")

# 3. Mengambil daftar model dari client
for model in client.models.list():
    print(model.name)