from rag.query_rewriter import QueryRewriter


def main():

    rewriter = QueryRewriter()

    queries =[
        "我的车又不知道自己在哪儿了，咋整？",
        "车子导航总是失败，怎么处理？",
        "这款无人车的保修期是多少年？"
    ]

    for query in queries:
        rewritten_query = rewriter.rewrite(query)
        print(f"原始查询: {query}")
        print(f"重写后查询: {rewritten_query}")
        print("\n"+"="*50)

if __name__ == "__main__":
    main()
