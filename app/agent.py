import json

from llm_client import LLMClient
from registry import tools, tool_functions

SYSTEM_PROMPT = """
你是一个设备管理Agent。

你必须遵守以下规则：

1. 当用户要求查询设备状态、重启设备等操作时，优先使用提供的工具获取真实结果。
2. 必须根据工具返回的数据回答，不得编造工具没有提供的信息。
3. 如果工具没有提供单位、正常范围或安全阈值，不要自行推断。
4. 如果工具调用失败，应根据错误信息决定是否重试或向用户说明失败原因。
5. 不要声称某个操作成功，除非工具结果明确表示成功。
6. 完成用户要求的全部任务后，再给出最终回答。
7. 如果多个操作存在先后依赖关系，必须按照依赖顺序执行，不要同时调用相互依赖的工具。
8. 如果用户要求“重启设备并获取状态”，必须先完成重启，再查询设备状态，确保返回的是重启后的最新状态。
"""


class Agent:
    def __init__(self, max_steps: int = 5, system_prompt: str = SYSTEM_PROMPT):
        self.max_steps = max_steps
        self.llm = LLMClient()
        self.system_prompt = system_prompt

    def run(self, user_input: str):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        step = 0
        execution_history = []
        tool_failed = False

        while True:

            if step >= self.max_steps:
                agent_result = {
                    "success": False,
                    "answer": None,
                    "steps": step,
                    "history": execution_history,
                    "error": f"超过最大步骤数 {self.max_steps}，未能完成任务。"
                }

                for record in execution_history:
                    print(
                        
                        f"工具: {record['tool']}, "
                        f"参数: {record['arguments']}, "
                        f"结果: {record['result']}"
                    )
                
                break
            step += 1

            print(f"\n=== 第{step}步 ===")


            try:
                response = self.llm.client.chat.completions.create(
                    model = self.llm.model,
                    messages = messages,
                    tools = tools,
                    tool_choice = "auto",
                    extra_body = {
                        "thinking":{
                            "type":"disabled"  
                        }
                    }
                )
            except Exception as e:
                agent_result ={
                    "success": False,
                    "answer": None,
                    "steps": step,
                    "history": execution_history,
                    "error": f"调用LLM接口失败: {str(e)}"
                }
                break
            message = response.choices[0].message

            print("原始回答：")
            print(message.content)

            print("\n工具调用结果：")
            print(message.tool_calls)
            
            if not message.tool_calls:
                agent_result = {
                    "success": not tool_failed,
                    "answer": message.content,
                    "steps": step,
                    "history": execution_history,
                    "error": "工具执行错误："if tool_failed else None
                }
                break

            messages.append(message)

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                arguments = tool_call.function.arguments
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError as e:
                    result = {
                        "error": "参数格式不正确",
                        "details": str(e)
                    }
                    tool_failed = True

                    execution_history.append(
                        {
                            "tool":function_name,
                            "arguments":tool_call.function.arguments,
                            "result":result
                        }
                    )


                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result, ensure_ascii=False)
                        }
                    )
                    continue

                print("\n函数名称:",tool_call.function.name)
                print("函数参数:",arguments)

                tool_function = tool_functions.get(function_name)
                if tool_function:
                    try:
                        result = tool_function(**arguments)
                    except Exception as e:
                        result = {
                            "error": str(e)
                        }
                        tool_failed = True
                    execution_history.append(
                        {
                            "tool":function_name,
                            "arguments":arguments,
                            "result":result
                        }
                    )
                else:
                    tool_failed = True
                    result = {
                        "error": f"未知工具: {tool_call.function.name}"
                    }
                    execution_history.append(
                        {
                            "tool":function_name,
                            "arguments":arguments,
                            "result":result
                        }
                    )
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    }
                )
        return agent_result