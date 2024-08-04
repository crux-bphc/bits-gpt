from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from src.query_db import get_retriever
from src.multivector import MV_retriever
from langchain.retrievers import EnsembleRetriever
import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv("GROQ_API_KEY") is not None:
    model_name = os.getenv("GROQ_MODEL_NAME") or "llama3-70b-8192"
    print(f"Using GROQ: {model_name} model")
    model = ChatGroq(temperature=0, model_name=model_name)

elif os.getenv("OPENAI_API_KEY") is not None:
    model_name = os.getenv("OPENAI_MODEL_NAME") or "gpt-3.5-turbo"
    print(f"Using OpenAI: {model_name} model")
    model = ChatOpenAI(model=model_name)

else:
    raise ValueError("No API key found for GROQ or OpenAI in environment variables")

vectorstore_retriever = get_retriever()


PROMPT_TEMPLATE = """
You are BitsGPT, a friendly chatbot for helping college students with their college life created by CruX.
Your responses are quirky and fun, try to joke around but provide useful advice as well.
Don't create up advice on your own. Instead, use the following context to answer the question.


{context}

---
If any CSV data is present, ONLY consider the CSV data for the context.
Answer the question without using the word context: {question}

Also at the end link the source(s) of your answer, if they are related to the question.
"""

ensemble_retriever = EnsembleRetriever(
    retrievers=[vectorstore_retriever, MV_retriever], weights=[0.6, 0.4]
)

prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
setup_and_retrieval = RunnableParallel(
    {"context": ensemble_retriever, "question": RunnablePassthrough()}
)
output_parser = StrOutputParser()

talk_chain = setup_and_retrieval | prompt | model | output_parser

if os.getenv("COHERE_API_KEY") is not None:
    from langchain.retrievers import ContextualCompressionRetriever
    from langchain.retrievers.document_compressors import CohereRerank

    extra_retriever = get_retriever(search_kwargs={"k": 50})
    compressor = CohereRerank()
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=extra_retriever
    )

    cohere_setup_and_retrieval = RunnableParallel(
        {"context": compression_retriever, "question": RunnablePassthrough()}
    )
    cohere_talk_chain = cohere_setup_and_retrieval | prompt | model | output_parser
