from pathlib import Path
from sentence_transformers import SentenceTransformer

from rag.loader import load_text, clean_text
from rag.splitter import splitter_text

def main():

    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "manuals" / "agv_manual.txt"

    content = load_text(file_path)
    cleaned_content = clean_text(content)

    chunks = splitter_text(
        text = cleaned_content,
        chunk_size = 100,
        overlap = 20,
        source = file_path.name
    )

    print("chunk 数量:", len(chunks))

    model = SentenceTransformer(
        "BAAI/bge-base-zh-v1.5",
        device = "cpu"
    )

    passages = [chunk["text"] for chunk in chunks]

    passage_vectors = model.encode(
        passages,
        normalize_embeddings=True
    )

    query = "机器人找不到自己的位置怎么办？"

    instruction = "为这个句子生成表示以用于检索相关文章："

    query_vector = model.encode(
        instruction + " " + query,
        normalize_embeddings=True
    )

    scores = passage_vectors @ query_vector

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )

    # 打印排名前 3 的文章
    top_k = 3

    print("\n用户问题：", query)

    print("\n===top_k 检索结果===")

    for rank , index in enumerate(ranked_indices[:top_k],start = 1):
        chunk = chunks[index]

        print("\n" + "=" * 40)
        print("排名：", rank)
        print("Chunk ID：", chunk["chunk_id"])
        print("相似度：", round(float(scores[index]), 4)) #round() 是 Python 的内置函数，用于数值舍入。
        print("来源：", chunk["source"])
        print("文本内容：")
        print(chunk["text"])

if __name__ == "__main__":
    main()
