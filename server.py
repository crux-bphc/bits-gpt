from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langserve import add_routes
from dotenv import load_dotenv
from query_db import get_retriever

load_dotenv()

app = FastAPI(
    title="BitsGPT LangChain Server",
    version="1.0",
    description="A simple api server for BitsGPT using Langchain's Runnable interfaces",
)

model = ChatOpenAI(model="gpt-3.5-turbo")
retriever = get_retriever()

PROMPT_TEMPLATE = """
You are BitsGPT, a friendly chatbot for helping college students with their college life.
Don't create up advice on your own. Instead, use the following context to answer the question.

{context}

---

Answer the question without using the word context: {question}

Also at the end link the source(s) of your answer.
"""

prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)
output_parser = StrOutputParser()

chain = setup_and_retrieval | prompt | model | output_parser

add_routes(
    app,
    chain,
    path="/talk",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
