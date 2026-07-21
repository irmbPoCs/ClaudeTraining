import voyageai
from dotenv import load_dotenv

load_dotenv()

client  = voyageai.Client()

# Embedding Generation
def generate_embedding(text, model="voyage-3-large", input_type="query"):
    result = client.embed([text], model=model, input_type=input_type)

    return result.embeddings[0]