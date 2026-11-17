
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


def main():

    project_root = Path(__file__).resolve().parent.parent
    db_path = project_root / "vector_db"

    client = chromadb.PersistentClient(
        path=str(db_path)
    )

    collection = client.get_collection(
        name="agv_manual_v1",
        embedding_function=None
    )

    print("数据库记录数量：", collection.count())
    data = collection.get(
    include=["documents", "metadatas"]
    )

    print("数据库中的全部 ID：")
    print(data["ids"])

    model = SentenceTransformer(
        "BAAI/bge-base-zh-v1.5",
        device = "cpu"
    )

    query = "机器人找不到自己的位置怎么办？"
    instruction = "为这个句子生成表示以用于检索相关文章："

    query_vector = model.encode(
        instruction + " " + query,
        normalize_embeddings=True
    )

    results = collection.query(
        query_embeddings=[query_vector.tolist()],
        n_results=3,
        include = ["documents","metadatas","distances"]
    )

    # 8. 输出检索结果
    print("\n用户问题：", query)
    print("\n=== ChromaDB Top-3 检索结果 ===")

    for rank, (chunk_id, document, metadata, distance) in enumerate(
        zip( #将多个可迭代对象中对应位置的元素组合起来。
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ),
        start=1
    ):
        print("\n" + "=" * 40)
        print("排名：", rank)
        print("Chunk ID：", chunk_id)
        print("距离：", round(float(distance), 4))
        print("来源：", metadata["source"])
        print("文本内容：")
        print(document)


if __name__ == "__main__":
    main()