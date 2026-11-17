from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-base-zh-v1.5",
    device = "cpu"
)

text = "无人车发生定位异常，需要检查激光雷达。"
embedding = model.encode(text)

print("原始文本:", text)

print("向量类型：", type(embedding))

print("向量维度：", embedding.shape)

print("前十个数值：", embedding[:10])
