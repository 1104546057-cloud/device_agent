def get_device_status(device_id: str):
    return {
        "device_id": device_id,
        "status": "running",
        "temperature": 105,
        "battery": 65
    }

def restart_device(device_id: str):
    return {
        "device_id":device_id,
        "action":"restart",
        "success":True
    }