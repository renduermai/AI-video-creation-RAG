import hashlib
import chromadb
from config import TOP_K, CHROMA_PATH, COLLECTION_NAME
from chromadb import Settings


class VectorStore:

    def __init__(self, persist_path=CHROMA_PATH, space="l2"):
        if persist_path:
            self.client = chromadb.PersistentClient(path=persist_path)
        else:
            self.client = chromadb.Client(Settings(allow_reset=True))

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": space}
        )

    def add_documents(self, documents, vectors, metadatas=None, ids=None):
        if ids is None:
            # 用内容哈希生成唯一 id：同内容重复导入会覆盖，不同内容不会冲突
            ids = [hashlib.md5(doc.encode("utf-8")).hexdigest() for doc in documents]

        if metadatas is None:
            metadatas = [{} for _ in documents]

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=vectors,
            metadatas=metadatas
        )

    def search(self, query_vector, top_k=TOP_K, where=None):
        results = self.collection.query(
            query_embeddings=query_vector,
            n_results=top_k,
            where=where
        )
        return results
