import math

def cosine_similarity(a: list[float], b: list[float]) -> float:

    if len(a) != len(b):
        raise ValueError("两个向量纬度必须一致")

    dot_product = sum(
        x * y for x, y in zip(a, b)
    )

    norm_a = math.sqrt(sum(x**2 for x in a))
    norm_b = math.sqrt(sum(y**2 for y in b))

    if norm_a == 0 or norm_b == 0:
        raise ValueError("不能计算余弦相似度，因为有一个向量的模为0。")
        
    similarity = dot_product / (norm_a * norm_b)
    return similarity

if __name__ == "__main__":
    query = [0.9, 0.1, 0.0]

    chunk_a = [1.0, 0.0, 0.0]
    chunk_b = [0.0, 1.0, 0.0]
    chunk_c = [0.0, 0.0, 1.0]

    print(
        "consine 与 chunk_a 的相似度为：",
        cosine_similarity(query, chunk_a)
    )
    print(
        "consine 与 chunk_b 的相似度为：",
        cosine_similarity(query, chunk_b)
    )
    print(
        "consine 与 chunk_c 的相似度为：",
        cosine_similarity(query, chunk_c)
    )

    
