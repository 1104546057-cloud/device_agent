
from rag.retriever import Retriever

def get_device_status(device_id: str):
    return {
        "device_id": device_id,
        "status": "running",
        "temperature": 105,
        "battery": 65
    }

def restart_device(device_id: str):
    return {
        "device_id":device_id,
        "action":"restart",
        "success":True
    }

def search_manual(query: str , top_k: int =3)-> dict:
    
    if not query.strip():
        raise ValueError("检索问题不能为空")

    if not isinstance(top_k, int) or not 1 <= top_k <= 5:
        raise ValueError("top_k 必须是 1 到 5 的整数")

    # 1. 创建检索器
    retriever = Retriever()

    # 2. 查询 ChromaDB
    chunks = retriever.retrieve(
        query=query,
        top_k=top_k
    )

    # 3. 整理返回结果
    results = []

    for chunk in chunks:
        results.append({
            "chunk_id": chunk["chunk_id"],
            "source": chunk["source"],
            "text": chunk["text"]
        })

    # 4. 返回给 Agent
    return {
        "query": query,
        "results": results
    }
