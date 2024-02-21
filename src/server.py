import os
from fastapi import FastAPI
from langserve import add_routes
from src.chains import talk_chain
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI(
    title="BitsGPT LangChain Server",
    version="1.0",
    description="A simple api server for BitsGPT using Langchain's Runnable interfaces",
)

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://172.16.142.163",
    "http://172.16.142.163:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
