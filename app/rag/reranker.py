
from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "BAAI/bge-reranker-base",
            device="cpu",
            max_length=512
        )

    def rerank(
        self,
        query: str,
        chunks: list[dict],
        top_k: int = 3
    ) -> list[dict]:

        # 1. 检查输入
        if not query.strip():
            raise ValueError("查询不能为空")

        if top_k <= 0:
            raise ValueError("top_k 必须大于 0")

        if not chunks:
            return []

        # 2. 组成问题和文档配对
        pairs = [
            (query, chunk["text"])
            for chunk in chunks
        ]

        # 3. 使用 CrossEncoder 计算相关性分数
        scores = self.model.predict(
            pairs,
            batch_size=4
        )

        # 4. 将分数和 Chunk 对应起来
        reranked_chunks = []

        for chunk, score in zip(chunks, scores):

            new_chunk = chunk.copy()

            new_chunk["retrieval_rank"] = chunk["rank"]
            new_chunk["rerank_score"] = float(score)

            reranked_chunks.append(new_chunk)

        # 5. 根据 Rerank 分数从高到低排序
        reranked_chunks.sort(
            key=lambda item: item["rerank_score"],
            reverse=True
        )

        # 6. 只保留前 top_k 条
        reranked_chunks = reranked_chunks[:top_k]

        # 7. 重新生成排名
        for rank, chunk in enumerate(
            reranked_chunks,
            start=1
        ):
            chunk["rank"] = rank

        return reranked_chunks
