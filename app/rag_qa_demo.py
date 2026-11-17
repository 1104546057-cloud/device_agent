from rag.rag_qa import RAGQA

def main():

    rag = RAGQA()
    query = "机器人找不到自己的位置怎么办？"

    print("查询：", query)

    result = rag.ask(
        query = query,
        top_k = 3
    )

    print("回答：", result["answer"])

    for source in result["sources"]:
        print(
            "来源：", source["source"],
            "距离：", round(source["distance"], 4),
            "chunk_id：", source["chunk_id"]
        )

if __name__ == "__main__":
    main()