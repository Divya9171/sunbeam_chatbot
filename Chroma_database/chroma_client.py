import chromadb

client = chromadb.PersistentClient(path="chroma_db/chroma")

collection = client.get_or_create_collection(
    name="scraper_docs"
)