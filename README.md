# BitsGPT

Your campus buddy chatbot for advice, resources and making student life easier.

## Setup

1. Clone the repository

```bash
git clone https://github.com/crux-bphc/bits-gpt.git
```

2. Create a virtual environment

```bash
python -m venv venv
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Create the vector database

```bash
python create_database.py
```

5. Run the server

```bash
python server.py
```

6. Go to http://localhost:8000/talk/playground/ to open the playground
