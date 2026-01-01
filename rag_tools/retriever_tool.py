from langchain.tools import tool
from Chroma_database.chroma_client import collection
from langchain.embeddings import init_embeddings


# vector_store = VectorStore()

embed_model = init_embeddings(
    model="text-embedding-all-minilm-l6-v2-embedding",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

@tool
def retrieve_context(query: str) -> str:
    """
    Docstring for web_scraping
    -This retrieve_context_tool function retrieves the relevent documents.
    -It retrieves the documents form chromadb(vector_database) with semantic similarity with the embeddings of given user query.
    
    :param query: str - user question
    """

    query_embed = embed_model.embed_query(query)

    docs = collection.query(
        query_embeddings=[query_embed],
        n_results=12
    )
    
    documents = docs.get("documents", [])

    if not documents or not documents[0]:
        return "No relevant documents found."

    flat_docs = documents[0]  # flatten

    text = ""
    # Optional: debug print
    for i, doc in enumerate(flat_docs, 1):
        text += doc
        text += "\n"
    return text

 
