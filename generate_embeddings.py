import argparse
import os
from uuid import uuid4

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Distance, VectorParams

load_dotenv()


def ingest_documents(folder_path, collection_name):
    # Initialize OpenAI embeddings
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    # Initialize Qdrant client
    qdrant_client = QdrantClient(host="localhost", port=6333)

    try:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
        )
    except UnexpectedResponse:
        pass

    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=collection_name,
        embedding=embeddings,
    )

    # Iterate over all PDF files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            # Load PDF document
            loader = PyPDFLoader(file_path)
            documents = loader.load()

            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
            )
            chunks = text_splitter.split_documents(documents)

            uuids = [str(uuid4()) for _ in range(len(chunks))]
            vector_store.add_documents(documents=documents, ids=uuids)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ingest PDF documents and upload embeddings to Qdrant.",
    )
    parser.add_argument(
        "folder",
        type=str,
        help="Path to the folder containing PDF files.",
    )
    parser.add_argument("collection", type=str, help="Name of the Qdrant collection.")
    args = parser.parse_args()

    ingest_documents(args.folder, args.collection)
