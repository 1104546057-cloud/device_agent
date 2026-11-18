
from rag.retriever import Retriever
from rag.query_rewriter import QueryRewriter

def print_results(title, results):

    print("\n"+"="*50)

    print(title)

    for item in results:
        print(f"排名: {item['rank']}")
        print(f"chunk_id: {item['chunk_id']}")
        print("距离:" ,round(item['distance'],4))
        print("内容:",item['text'][:80])
        print("-"*50)

def main():
    retriever = Retriever()
    rewriter = QueryRewriter()

    queries = [
        "我的车又不知道自己在哪儿了，咋整？",
        "车子导航总是失败，怎么处理？"
    ]
    
    for query in queries:

        original_results = retriever.retrieve(
            query = query,
            top_k = 3
            )

        rewritten_query = rewriter.rewrite(query)

        rewritten_results = retriever.retrieve(
            query = rewritten_query,
            top_k = 3
            )

        print("\n原始问题:",query)
        print("改写后问题:",rewritten_query)

        print_results("原始查询结果:",original_results)
        print_results("改写后查询结果:",rewritten_results)

if __name__ == "__main__":
    main()