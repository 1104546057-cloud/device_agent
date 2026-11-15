from pathlib import Path

from rag.loader import load_text, clean_text
from rag.splitter import splitter_text

def main():
    # 指定文本文件路径
    project_root = Path(__file__).parent.parent

    # 获取维护手册完整路径
    file_path = project_root / "manuals" / "agv_manual.txt"

    #读取文档
    content = load_text(file_path)

    print("原始文档长度：\n", len(content))

    # 清理文档
    cleaned_content = clean_text(content)
    print("\n=== 清理后的文档长度 ===\n", len(cleaned_content))

    # 分割文档
    chunks = splitter_text(
        text = cleaned_content,
        chunk_size = 50,
        overlap = 10,
        source = file_path.name
    )

    print("\n=== 分割后的文档数量 ===\n", len(chunks))

    # 打印每个分割块的内容
    for chunk in chunks:
        print("\n"+"="*20)
        print("分割块ID:", chunk["chunk_id"])
        print("分割块来源:", chunk["source"])
        print("分割块起始索引:", chunk["start_index"])
        print("分割块结束索引:", chunk["end_index"])
        print("分割块内容:\n", chunk["text"])


if __name__ == "__main__":
    main()