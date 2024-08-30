from openai import OpenAI
from upstash_vector import Vector, Index

from settings import UPSTASH_VECTOR_REST_URL, UPSTASH_VECTOR_REST_TOKEN, OPEN_API_KEY

client = OpenAI(api_key=OPEN_API_KEY)

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

documents = [
    "The cat jumped over the dog",
    "The dog jumped over the cat",
    "The cow jumped over the moon"
]

embeddings = [get_embedding(x) for x in documents]

dataset = {}
for i, embedding in enumerate(embeddings):
    dataset[i] = embedding

index = Index(url=UPSTASH_VECTOR_REST_URL, token=UPSTASH_VECTOR_REST_TOKEN)

vectors = []
for key, value in dataset.items():
    print(key)
    my_id = key
    embedding = value
    vectors.append(Vector(id=my_id, vector=embedding))

# index.upsert(vectors=vectors)

dataset[3] = get_embedding("The moose sat by the dog in the house")
index.upsert(vectors=[Vector(id=3, vector=dataset[3])])

query_str = "The moose sat by the dog in the house"
query_embedding = get_embedding(query_str)

results = index.query(
  vector=query_embedding,
  top_k=3,
  include_vectors=True,
  include_metadata=True
)

for result in results:
    print(result.id, result.score * 100)