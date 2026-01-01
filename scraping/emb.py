

# embed_model=init_embeddings(
#     model="text-embedding-nomic-embed-text-v1.5-embedding",
#     api_key="not-needed",
#     base_url="http://127.0.0.1:1234/v1",
#     provider="openai",
#     check_embedding_ctx_length=False
# )

# def get_embeddings(text_file):
    
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import init_embeddings
from langchain_community.vectorstores import Chroma

# ================= CONFIG =================
TXT_FOLDER_PATH = "D:\IIIT-GEN-AI-94359\final_project\scraping"  # 👈 your scraped txt folder
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "scraped_txt_collection"

# ================= LOAD TXT FILES =================
documents = []

for file in os.listdir(TXT_FOLDER_PATH):
    if file.endswith(".txt"):
        file_path = os.path.join(TXT_FOLDER_PATH, file)
        loader = TextLoader(file_path, encoding="utf-8")
        documents.extend(loader.load())

print(f"📄 Loaded {len(documents)} text files")

# ================= SPLIT INTO CHUNKS =================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)
print(f"✂ Created {len(chunks)} chunks")

# ================= EMBEDDING MODEL =================
embedding_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5-embedding",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

# ================= CREATE CHROMA DB =================
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory=CHROMA_DB_PATH,
    collection_name=COLLECTION_NAME
)

vectorstore.persist()
print("✅ ChromaDB created and stored successfully")
