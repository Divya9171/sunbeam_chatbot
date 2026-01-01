   
import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import init_embeddings
# from langchain_community.vectorstores import Chroma
# from Chroma_database import vectorstore
from Chroma_database.chroma_client import collection

#here first we load the text files giving path of the folder
def ingect():
    # ================= CONFIG =================
    TXT_FOLDER_PATH = "D:\\IIIT-GEN-AI-94359\\final_project\\text_files"
    # CHROMA_DB_PATH = "./chroma_db"
    # COLLECTION_NAME = "scraped_txt_collection"

    # ================= LOAD TXT FILES =================
    documents = []

    for file in os.listdir(TXT_FOLDER_PATH):
        if file.endswith(".txt"):
            file_path = os.path.join(TXT_FOLDER_PATH, file)
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())

    print(f"📄 Loaded {len(documents)} text files")

#Large text cannot be:
#Embedded efficiently
#Retrieved accurately

    # ================= SPLIT INTO CHUNKS =================
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    # splitter = RecursiveCharacterTextSplitter(
    #     chunk_size = 500,
    #     chunk_overlap = 100,
    #     separators=["\n\n", "\n"]
    # )
    # scraper = InternshipScraper()
    # text = scraper.scrape()
    # chunks = splitter.split_text(text)

    chunks = text_splitter.split_documents(documents)
    print(f"✂ Created {len(chunks)} chunks")
#An embedding is a numerical vector representation of text
    # ================= EMBEDDING MODEL =================
    embed_model = init_embeddings(
        model="text-embedding-all-minilm-l6-v2-embedding",
        provider="openai",
        base_url="http://127.0.0.1:1234/v1",
        api_key="not-needed",
        check_embedding_ctx_length=False
    )

    # ================= CREATE CHROMA DB =================
    # vectorstore=
    # vectorstore = Chroma.from_documents(
    #     documents=chunks,
    #     embedding=embedding_model,
    #     persist_directory=CHROMA_DB_PATH,
    #     collection_name=COLLECTION_NAME
    # )

    for i, chunk in enumerate(chunks):
       
        collection.add(
            ids = [f"sunbeam_docs_{i}"],
            documents = [chunk.page_content],
            metadatas = [{
                "page": f"sunbeam_docs"
            }],
            embeddings=embed_model.embed_documents([chunk.page_content])    
        )


    # vectorstore.persist()
    print("✅ ChromaDB created and stored successfully")


