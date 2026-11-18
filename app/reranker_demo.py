
from rag.retriever import Retriever
from rag.reranker import Reranker


def print_results(title, results):

    print("\n" + "=" * 50)
    print(title)

    for chunk in results:

        print("当前排名：", chunk["rank"])
        print("Chunk ID：", chunk["chunk_id"])
        print("原始距离：", round(chunk["distance"], 4))

        if "rerank_score" in chunk:
            print(
                "Rerank 分数：",
                round(chunk["rerank_score"], 4)
            )
            print(
                "原始排名：",
                chunk["retrieval_rank"]
            )

        print("内容：", chunk["text"][:100])
        print("-" * 30)


def main():

    retriever = Retriever()
    reranker = Reranker()

    queries = [
        "我的车又不知道自己在哪儿了，咋整？",
        "AGV 无人车定位异常的处理方法是什么？",
        "车子导航总是失败，怎么处理？"
    ]

    candidate_k = 5
    final_k = 3

    for query in queries:

        print("\n用户问题：", query)

        # 1. 先召回 5 个候选
        candidates = retriever.retrieve(
            query=query,
            top_k=candidate_k
        )

        # 2. 原始检索 Top-3
        original_results = candidates[:final_k]

        # 3. 对同一批候选进行 Rerank
        reranked_results = reranker.rerank(
            query=query,
            chunks=candidates,
            top_k=final_k
        )

        print_results(
            "原始 Retriever Top-3",
            original_results
        )

        print_results(
            "Rerank 后的 Top-3",
            reranked_results
        )


if __name__ == "__main__":
    main()
