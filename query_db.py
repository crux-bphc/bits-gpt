from langchain.vectorstores.chroma import Chroma
from embeddings import get_hf_embeddings

CHROMA_PATH = "chroma"
hf_embeddings = get_hf_embeddings()


def query_chroma(query: str, k=5):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=hf_embeddings)
    results = db.similarity_search_with_relevance_scores(query, k=k)
    return results


def get_retriever():
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=hf_embeddings)
    retriever = db.as_retriever()
    return retriever


def main():
    while True:
        query = input("Enter query: ")
        results = query_chroma(query)
        print(results)


if __name__ == "__main__":
    main()
