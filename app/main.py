import os
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LLM_API_KEY")

device = {
    "device_id": "robot_001",
    "battery": 82,
    "temperature": 36.5,
    "online": True
}

json_data = json.dumps(
    device,
    ensure_ascii=False,   #保留中文显示原样
    indent=2              #缩进为2个空格
    )

def get_device_status(device_id:str):
    if device["device_id"] != device_id:
        raise ValueError("Device not found.")

    return {
        "device_id": device_id,
        "battery": 82,
        "temperature": 36.5,
        "online": True
    }

try:
    result = get_device_status("robot_001")
    print(result)
except ValueError as e:
    print(f"Error: {e}")


print("DeviceAgent started.")
print(f"API Key: {api_key is not None}")

print("\nDevice:")
print(json_data)

print(type(device))
print(type(json_data))

new_device = json.loads(json_data)

print("\nNew Device:")
print(new_device)
print(type(new_device))