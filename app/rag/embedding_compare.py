from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-base-zh-v1.5",
    device = "cpu"
)

query = "机器人找不到自己的位置怎么办？"

passages = [
    "故障代码 E102：定位异常，需要检查激光雷达连接。",
    "故障代码 E103：导航规划失败，需要检查地图。",
    "设备电量不足时，需要连接充电器。"
]

instruction = "为这个句子生成表示以用于检索相关文章："

query_vector = model.encode(
    instruction + " " + query,
    normalize_embeddings=True
    )

passage_vectors = model.encode(
    passages,
    normalize_embeddings=True
)

print("query向量形状：", query_vector.shape)
print("passage向量形状：", passage_vectors.shape)

scores = passage_vectors @ query_vector

for i, score in enumerate(scores):
    print(f"chunk {i} 相似度：{float(score):.4f}")
    print(f"chunk {i} 内容：{passages[i]}")
