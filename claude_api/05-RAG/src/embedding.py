import voyageai
from dotenv import load_dotenv

load_dotenv()

client  = voyageai.Client()

# Embedding Generation
def generate_embedding(chunks, model="voyage-3-large", input_type="query"):
    is_list = isinstance(chunks, list)
    input = chunks if is_list else [chunks]
    result = client.embed(input, model=model, input_type=input_type)
    return result.embeddings if is_list else result.embeddings[0]