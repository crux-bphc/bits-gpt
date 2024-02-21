import os
from fastapi import FastAPI
from langserve import add_routes
from src.chains import talk_chain
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="BitsGPT LangChain Server",
    version="1.0",
    description="A simple api server for BitsGPT using Langchain's Runnable interfaces",
)


add_routes(
    app,
    talk_chain,
    path="/talk",
)

if os.getenv("COHERE_API_KEY") is not None:
    from src.chains import cohere_talk_chain

    add_routes(
        app,
        cohere_talk_chain,
        path="/cohere",
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
