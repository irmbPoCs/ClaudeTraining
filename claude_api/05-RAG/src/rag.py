from rag_types import *
from embedding import *
from vector_store import VectorStore
from dotenv import load_dotenv

load_dotenv()

#with open("./claude_api/05-RAG/src/report.md", "r") as f:
with open("./report.md", "r") as f:
    text = f.read()

# chunks = chunk_by_sentence(text)
# chunks = chunk_by_char(text, 500, 150)
chunks = chunk_by_section(text)
# [print(chunk + "\n----\n") for chunk in chunks]

store = VectorStore()

# The collection persists to ./chroma_db, so only embed on the first run.
if store.is_empty():
    # input_type="document" is what Voyage expects for indexing; queries use "query".
    embeddings = generate_embedding(chunks, input_type="document")
    store.add(chunks, embeddings)
    print(f"Indexed {len(chunks)} chunks into {store.persist_dir}")
else:
    print(f"Reusing {len(store)} chunks already in {store.persist_dir}")

query = "What are the top 3 goals of Development department?"
query_embedding = generate_embedding(query, input_type="query")

for result in store.search(query_embedding, k=2):
    print(f"\n--- distance: {result['distance']:.4f} ---")
    print(result["content"][:300])
