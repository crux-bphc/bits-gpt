import json
import time
from src.chains import model, retriever, prompt

with open("tests/test_cases.json", "r") as f:
    test_data = json.load(f)

category = input("Enter category: ")
category_data = test_data[category]
dataset = {
    "question": [],
    "ground_truths": [],
    "answer": [],
    "contexts": [],
}

c = 0
for obj in category_data:
    question, expected_answer = obj["question"], obj["expected_answer"]

    dataset["question"].append(question)
    dataset["ground_truths"].append([expected_answer])

    docs = retriever.get_relevant_documents(question)

    dataset["contexts"].append([repr(doc) for doc in docs])
    context = repr(docs)

    fin_prompt = prompt.format(context=docs, question=question)
    result = model.invoke(fin_prompt)
    dataset["answer"].append(result.content)

    c += 1
    print(f"Generating dataset for {category} | {c/len(category_data)*100:0.2f}%", end="\r")
    time.sleep(3)

print("\Starting evaluation...\n")
with open(f"tests/dataset-{category}.json", "w") as f:
    json.dump(dataset, f, indent=2)

EVALUATION_PROMPT = """
You are given a question, an answer and an expected answer. Your task is to determine if the answer is good or not.
You must ONLY REPLY With a single number: a rating of (0,1,2,3); where 0 is a completely unrelated answer, 1 a bad answer, 2 is a decent answer and 3 is the most acurate answer.
Question: {question}
Answer: {answer}
Expected answer: {expected_answer}
"""

total_score = 0
results = {"average_score":0, "cases": []}
for case in range(len(dataset["question"])):
    print(f"Test Case {case+1}:")
    print(f"Question: {dataset['question'][case]}")
    print(f"Expected answer: {dataset['ground_truths'][case][0]}")
    print(f"Actual answer: {dataset['answer'][case]}")
    print("\n\n")
    time.sleep(2)
    result = model.invoke(EVALUATION_PROMPT.format(question=dataset['question'][case], answer=dataset['answer'][case], expected_answer=dataset['ground_truths'][case][0]))
    print("Rated Score:", result.content, "\n\n")
    try:
        score = int(result.content)
    except ValueError:
        print("Invalid score, asume score=1")
        score = 1

    total_score += score
    case = {
        "question": dataset["question"][case],
        "expected_answer": dataset["ground_truths"][case][0],
        "actual_answer": dataset["answer"][case],
        "score": score,
    }
    results["cases"].append(case)
    time.sleep(1)

results["average_score"] = total_score/len(dataset["question"])

with open(f"tests/results-{category}.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Total score: {total_score}/{len(dataset['question']) * 3}")
print(f"Average score (out of 3): {results['average_score']:0.2f}")