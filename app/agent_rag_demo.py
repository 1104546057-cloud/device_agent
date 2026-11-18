
from agent import Agent


def main():

    # 创建 Agent
    agent = Agent(max_steps=5)

    # 用户问题
    query = "请查询设备 AGV001 当前的运行状态和电量。"

    print("用户问题：", query)

    # 启动 Agent
    result = agent.run(query)

    print("\n========== 最终结果 ==========")

    print("执行成功：", result["success"])
    print("最终回答：", result["answer"])
    print("执行步数：", result["steps"])

    print("\n========== 工具调用历史 ==========")

    for record in result["history"]:
        print("工具名称：", record["tool"])
        print("工具参数：", record["arguments"])

    # 检查 Agent 是否真正调用 RAG
    used_rag = any(
        record["tool"] == "search_manual"
        for record in result["history"]
    )

    print("\n是否调用过 RAG 工具：", used_rag)

    used_status = any(
        record["tool"] == "get_device_status"
        for record in result["history"]
    )

    used_rag = any(
        record["tool"] == "search_manual"
        for record in result["history"]
    )

    print("是否调用设备状态工具：", used_status)
    print("是否错误调用 RAG 工具：", used_rag)




if __name__ == "__main__":
    main()
