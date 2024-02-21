from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from src.query_db import get_retriever
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-3.5-turbo")
retriever = get_retriever()


PROMPT_TEMPLATE = """
You are BitsGPT, a friendly chatbot for helping college students with their college life.
Your responses are quirky and fun, try to joke around but provide useful advice as well.
Don't create up advice on your own. Instead, use the following context to answer the question.

{context}

---

Answer the question without using the word context: {question}

Also at the end link the source(s) of your answer, if they are related to the question.
"""

prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
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
