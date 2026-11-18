
from llm_client import LLMClient


REWRITE_PROMPT = """
你是一个 AGV 无人车知识库查询改写助手。

你的任务是把用户的自然语言问题改写成适合知识库语义检索的查询。

规则：
1. 保留原始问题的真实含义。
2. 可以将口语化表达转换为专业术语。
3. 不得编造用户没有提供的故障代码、设备参数或事实。
4. 不要回答用户的问题。
5. 只输出一条改写后的中文查询，不要解释。
"""

class QueryRewriter:
    def __init__(self):
        self.llm = LLMClient()

    def rewrite(self,query:str)->str:
        if not query.strip():
            raise ValueError("查询不能为空不能为空")

        messages =[
            {
                "role": "system",
                "content": REWRITE_PROMPT
            },
            {
                "role": "user",
                "content": query
            }
        ]

        rewritten_query = self.llm.chat(messages)

        if not rewritten_query or not rewritten_query.strip():
            return query
        
        return rewritten_query.strip()
