from langchain_community.document_loaders import UnstructuredPDFLoader

# from langchain_community.document_loaders import PyPDFLoader
import pickle

# loader = PyPDFLoader("data\Bulletin-2023-24.pdf")

loader = UnstructuredPDFLoader("data\Bulletin-2023-24.pdf")
data = loader.load()

with open("bulletin_unstructured.pickle", "wb") as handle:
    pickle.dump(data, handle)

# handle = open("data\\bulletin_dumps\\bulletin_page_split.pickle","rb")
# pages = pickle.load(handle)

# print(pages[23])
