from agent import Agent

def main():
    agent = Agent(max_steps=5)

    user_input = input("请输入你的请求：")

    result = agent.run(user_input)
    print("\n=== 最终结果 ===")

    if result["answer"]:
        print("回答:", result["answer"])

    if not result["success"]:
        print("错误:", result["error"])

if __name__ == "__main__":
    main()