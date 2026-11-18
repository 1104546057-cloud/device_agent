from tools import get_device_status, restart_device, search_manual


tool_functions = {
    "get_device_status": get_device_status,
    "restart_device": restart_device,
    "search_manual": search_manual
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
    },    {
        "type": "function",
        "function": {
            "name": "search_manual",
            "description": (
                "查询AGV无人车维护手册。"
                "当用户询问故障代码、定位异常、导航失败、"
                "维修方法或设备维护知识时使用此工具。"
                "返回相关文档内容及Chunk ID。"
                "这不是查询设备实时状态的工具。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "需要查询维护手册的问题"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "返回文档数量，1到5，默认3"
                    }
                },
                "required": ["query"]
            }
        }
    }
    
]