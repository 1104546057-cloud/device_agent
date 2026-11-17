
from rag.retriever import Retriever


def print_results(title, results):

    print("\n" + "=" * 50)
    print(title)
    print("返回数量：", len(results))

    if not results:
        print("没有找到符合条件的文档")
        return

    for item in results:
        print("\n排名：", item["rank"])
        print("Chunk ID：", item["chunk_id"])
        print("距离：", round(item["distance"], 4))
        print("来源：", item["source"])
        print("内容：")
        print(item["text"])

def main():

    retriever = Retriever()
    query = "机器人找不到自己的位置怎么办？"

    results_1 = retriever.retrieve(
        query = query,
        top_k = 3
    )

    print_results("Top-3 检索结果", results_1)

        # 实验 2：只检索 Top-1
    results_2 = retriever.retrieve(
        query=query,
        top_k=1
    )

    print_results("实验 2：普通 Top-1 检索", results_2)

    # 实验 3：按照 Chunk ID 过滤
    results_3 = retriever.retrieve(
        query=query,
        top_k=3,
        metadata_filter={"chunk_id": 2}
    )

    print_results("实验 3：Metadata 过滤", results_3)

    # 实验 4：使用不存在的来源进行过滤
    results_4 = retriever.retrieve(
        query=query,
        top_k=3,
        metadata_filter={"source": "other_manual.txt"}
    )

    print_results("实验 4：无匹配来源", results_4)


if __name__ == "__main__":
    main()