from langchain_community.embeddings import HuggingFaceEmbeddings


def get_hf_embeddings():
    model_id = "sentence-transformers/all-MiniLM-L6-v2"
    model_kwargs = {"device": "cpu"}
    hf_embedding = HuggingFaceEmbeddings(model_name=model_id, model_kwargs=model_kwargs)
    return hf_embedding


def get_embeddings():
    return get_hf_embeddings()