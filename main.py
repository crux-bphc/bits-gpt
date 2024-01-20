from query_db import query_chroma
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import dotenv

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question normally without saying anything about the context: {question}
"""

def ask_question_open_ai(question: str):
    results = query_chroma(question, k=2)
    # print(results)
    
    if len(results) == 0:
        print(f"Unable to find matching results.")
        return
    
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=question)

    model = ChatOpenAI(model="gpt-3.5-turbo")
    response_text = model.invoke(prompt)

    sources = set(doc.metadata.get("source", None) for doc, _score in results)
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)

def main():
    dotenv.load_dotenv()

    while True:
        question = input("Enter question: ")
        ask_question_open_ai(question)

if __name__ == "__main__":
    main()