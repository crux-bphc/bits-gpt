import uuid
import os
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

raw_data_path = "data\\Handouts\\tt_processed"
summaries_path = "data\\Handouts\\Summary"

table_summaries = []
text_summaries = []
raw_tables = []
raw_texts = []

raw_filelist = os.listdir(raw_data_path)
summaries_filelist = os.listdir(summaries_path)
print("Loading documents and summaries from disk..")

for raw_file in raw_filelist:
    with open(os.path.join(raw_data_path, raw_file), "r", encoding="utf-8") as handle:
        if "rawtext" in raw_file:
            raw_texts.append(handle.read())
        if "rawtable" in raw_file:
            raw_tables.append(handle.read())

for summary_file in summaries_filelist:
    with open(
        os.path.join(summaries_path, summary_file), "r", encoding="utf-8"
    ) as handle:
        if "cookedtext" in summary_file:
            text_summaries.append(handle.read())
        if "cookedtable" in summary_file:
            table_summaries.append(handle.read())

# print lenght of each list along with which list it is
print(len(raw_texts), "raw_texts")
print(len(raw_tables), "raw_tables")
print(len(text_summaries), "text_summaries")
print(len(table_summaries), "table_summaries")


# The vectorstore to use to index the child chunks
vectorstore = Chroma(
    collection_name="summaries",
    embedding_function=HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    ),
)

store = InMemoryStore()
id_key = "doc_id"

# The retriever (empty to start)
MV_retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    docstore=store,
    id_key=id_key,
)

print("Building retriever..", MV_retriever.search_type)

# Add texts
doc_ids = [str(uuid.uuid4()) for _ in text_summaries]
summary_texts = [
    Document(page_content=s, metadata={id_key: doc_ids[i]})
    for i, s in enumerate(text_summaries)
]
if summary_texts:
    MV_retriever.vectorstore.add_documents(summary_texts)
    MV_retriever.docstore.mset(
        list(zip(doc_ids, raw_texts))
    )  # figure out how to efficiently get the raw data

# Add tables
table_ids = [str(uuid.uuid4()) for _ in table_summaries]
summary_tables = [
    Document(page_content=s, metadata={id_key: table_ids[i]})
    for i, s in enumerate(table_summaries)
]
MV_retriever.vectorstore.add_documents(summary_tables)
MV_retriever.docstore.mset(list(zip(table_ids, raw_tables)))
