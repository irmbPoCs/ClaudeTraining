from rag_types import *
from embedding import *
from dotenv import load_dotenv

load_dotenv()

#with open("./claude_api/05-RAG/src/report.md", "r") as f:
with open("./report.md", "r") as f:
    text = f.read()

# chunks = chunk_by_sentence(text)
# chunks = chunk_by_char(text, 500, 150)
chunks = chunk_by_section(text)
# [print(chunk + "\n----\n") for chunk in chunks]

print(generate_embedding(chunks[0]))