import os

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LLM_API_KEY")

print("DeviceAgent started.")
print(f"API Key:" , api_key is not None)

