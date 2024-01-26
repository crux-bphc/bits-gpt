import json

'''
{
  "simple-facts": [],
  "complex-facts": [],
  "advice": [],
  "opinion": []
}
'''

def add_data(category, question, answer):
    with open("tests/test_cases.json", "r") as handle:
        data = json.load(handle)

    if category not in data:
        print("Category invalid")
        return
    
    data[category].append({"question":question, "expected_answer":answer})
    with open("tests/test_cases.json", "w") as output:
        json.dump(data, output, indent=2)

def main():
    while True:
        print("type 'exit' to quit\n\n")
        category = input("Enter category: ")
        question = input("Enter question: ")
        answer = input("Enter answer: ")

        if category == 'exit' or question == 'exit' or answer == 'exit':
            break

        add_data(category, question, answer)


if __name__ == "__main__":
    main()