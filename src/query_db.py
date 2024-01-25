from langchain.vectorstores.chroma import Chroma
from src.embeddings import get_embeddings

CHROMA_PATH = "chroma"
embeddings = get_embeddings()


def query_chroma(query: str, k=5):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    results = db.similarity_search_with_relevance_scores(query, k=k)
    return results


def get_retriever(**kwargs):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = db.as_retriever(**kwargs)
    return retriever


def main():
    while True:
        query = input("Enter query: ")
        results = query_chroma(query)
        print(results)


if __name__ == "__main__":
    main()
