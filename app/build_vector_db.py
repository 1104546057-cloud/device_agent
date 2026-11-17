from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from rag.loader import load_text, clean_text
from rag.splitter import splitter_text

def main():
    # 项目根目录
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "manuals" / "agv_manual.txt"
    db_path = project_root / "vector_db"

    # 加载文本内容
    content = load_text(file_path)
    cleaned_content = clean_text(content)

    # 分块  
    chunks = splitter_text(
        text = cleaned_content,
        chunk_size = 100,
        overlap = 20,
        source = file_path.name
    )

    # 检查分块是否成功
    if not chunks:
        raise ValueError("分块失败")

    # 提取文本内容
    passages = [chunk["text"] for chunk in chunks]
    
    # 加载模型
    model = SentenceTransformer(
        "BAAI/bge-base-zh-v1.5",
        device = "cpu"
    )

    # 生成向量
    vectors = model.encode(
        passages,
        normalize_embeddings=True
    )

    # 创建数据库
    client = chromadb.PersistentClient(
        path=str(db_path)
    )

    # 创建集合

    collection = client.get_or_create_collection( #如果这个 Collection 已经存在，就获取它。如果不存在，就创建它。
        name="agv_manual_v1",
        embedding_function=None
    )

    # 生成 ID
    ids = [
        f"{file_path.stem}_{chunk['chunk_id']}"
        for chunk in chunks
    ]

    # 生成元数据
    metadatas = [
        {
            "source": file_path.name,
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"]
        }
        for chunk in chunks
    ]

    # 插入数据
    collection.upsert( #不存在就新增，存在则更新。
        ids=ids,
        documents=passages,
        embeddings=vectors.tolist(), #表示将 NumPy 数组转换成 Python 列表，方便传入 ChromaDB。
        metadatas=metadatas
    )

    print("数据库地址：", str(db_path))
    print("collection:", collection.name)
    print("向量维度:", vectors.shape)
    print("数据库记录数量：", collection.count())


if __name__ == "__main__":
    main()




    
