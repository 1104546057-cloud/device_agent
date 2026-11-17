from pathlib import Path

import chromadb 
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self):

        project_root = Path(__file__).resolve().parent.parent.parent
        db_path = project_root / "vector_db"

        client = chromadb.PersistentClient(
            path = db_path
        )

        self.collection = client.get_collection(
            name="agv_manual_v1",
            embedding_function=None
        )

        self.model = SentenceTransformer(
            "BAAI/bge-base-zh-v1.5",
            device = "cpu"
        )

        self.instruction = "为这个句子生成表示以用于检索相关文章："

    def retrieve(
            self, 
            query: str, 
            top_k: int = 3,
            metadata_filter: dict | None = None
        )->list[dict]:
        
        if not query.strip():
            raise ValueError("查询不能为空不能为空")

        if top_k <= 0:
            raise ValueError("top_k 必须大于 0")

        total = self.collection.count()

        if total ==0:
            return []

        query_vector = self.model.encode(
            self.instruction + " " + query,
            normalize_embeddings=True
        )

        result = self.collection.query(
            query_embeddings = [query_vector.tolist()]  ,
            n_results = top_k,
            where = metadata_filter,
            include = ["documents","metadatas","distances"]
        )

        retrieved_chunks = []

        for rank,(chunk_id,document,metadata,distance) in enumerate(
            zip(
                result["ids"][0],
                result["documents"][0],
                result["metadatas"][0],
                result["distances"][0]
            ),
            start = 1
        ):
            metatata = metadata or {}

            chunk={
                "rank":rank,
                "chunk_id":chunk_id,
                "text":document,
                "metadata":metatata,
                "distance":float(distance),
                "source":metatata.get("source","")
            }

            retrieved_chunks.append(chunk)

        return retrieved_chunks


