from document_loader import DocumentLoader
from embedding_client import EmbeddingClient
from llm_client import LLMClient
from vector_store import VectorStore


class RAGPipeline:
    def __init__(self):
        self.document_loader = DocumentLoader()
        self.embedding_client = EmbeddingClient()
        self.vector_store = VectorStore()
        self.llm_client = LLMClient()

    def ingest(self, file_path, category="default"):
        # 文件读取
        file_contents = self.document_loader.load(file_path)
        # 切分文档
        results = self.document_loader.text_splitter(file_contents)
        # 向量化
        vector_chunks = self.embedding_client.embed_documents(results)
        # 为每个 chunk 打上分类标签
        metadatas = [{"category": category} for _ in results]
        # 存储
        self.vector_store.add_documents(results, vector_chunks, metadatas=metadatas)

    def ingest_texts(self, texts, category="default"):
        """直接灌入文本列表，带分类"""
        vector_chunks = self.embedding_client.embed_documents(texts)
        metadatas = [{"category": category} for _ in texts]
        self.vector_store.add_documents(texts, vector_chunks, metadatas=metadatas)

    def query(self, query, category=None):
        # 问题向量化
        vector_query = self.embedding_client.embed_query(query)
        # 如果有 category，则按分类过滤
        where = {"category": category} if category else None
        # 搜索 top_k 文档
        top_k_docs = self.vector_store.search(vector_query, where=where)
        documents = top_k_docs.get("documents", [[]])[0]
        # 拼接文档
        context = "\n".join(documents)
        # 问题和文档给 AI 返回答案
        answer = self.llm_client.rag_ask(query, context)
        return answer

    def chat(self):
        print("欢迎进入 AIGC 创作知识库，按 q 退出")

        while True:
            # 接收问题
            question = input("请输入问题：")
            if question.lower() in ['q', 'quit', 'exit']:
                print('再见')
                break
            if not question:
                continue
            try:
                answer = self.query(question)
                # 可替换：只限定在某个txt 文件里面搜索
                # answer = self.query(question, category="script_paradigm")
                print(f'ai回答：{answer}')
            except Exception as e:
                print(e)
