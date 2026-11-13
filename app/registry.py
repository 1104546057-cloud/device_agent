from tools import get_device_status, restart_device


tool_functions = {
    "get_device_status": get_device_status,
    "restart_device": restart_device
}


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_device_status",
            "description": "获取设备状态",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "设备ID"
                    }
                },
                "required": ["device_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "restart_device",
            "description": "重启设备",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_id": {
                        "type": "string",
                        "description": "需要重启的设备ID"
                    }
                },
                "required": ["device_id"]
            }
        }
    }
]