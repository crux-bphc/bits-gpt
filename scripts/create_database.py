import os
import shutil
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import (
    DirectoryLoader,
    WebBaseLoader,
    SitemapLoader,
)
from langchain.vectorstores.chroma import Chroma
from src.embeddings import get_embeddings

CHROMA_PATH = "chroma"
DATA_PATH = "data"
embeddings = get_embeddings()


def load_documents(extension="txt") -> list[Document]:
    print(f"Loading {extension} documents...")
    loader = DirectoryLoader(DATA_PATH, glob=f"**/*.{extension}")
    documents = loader.load()
    return documents


def load_web_documents() -> list[Document]:
    # Sitemap Loader is taking forever and failing because of TooManyRedirects
    # loader = SitemapLoader("https://www.bits-pilani.ac.in/sitemap_index.xml")

    loader = WebBaseLoader("https://www.bits-pilani.ac.in/hyderabad/")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=300,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    return chunks


def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")


def generate_data_store():
    print(f"Loading documents in {DATA_PATH}...")

    documents = load_documents("md")
    chunks = split_text(documents)

    documents = load_documents("pdf")
    chunks.extend(split_text(documents))

    print("Loading web documents...")
    web_documents = load_web_documents()
    web_chunks = split_text(web_documents)

    chunks.extend(web_chunks)
    print("Saving to Chroma...")
    save_to_chroma(chunks)


def main():
    generate_data_store()


if __name__ == "__main__":
    main()
