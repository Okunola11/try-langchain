phrase_1 = 'The dog ate my homework'
phrase_2 = 'The homework ate my dog'

phrase_1_as_list = sorted([x.lower() for x in phrase_1.split(" ")])
phrase_2_as_list = sorted([x.lower() for x in phrase_2.split(" ")])

print(phrase_1_as_list)
print(phrase_2_as_list)

from openai import OpenAI
import numpy as np
from settings import OPEN_API_KEY

client = OpenAI(api_key=OPEN_API_KEY)

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

documents = [
    "The cat jumped over the dog",
    "The dog jumped over the cat",
    "The cow jumped over the moon"
]

embeddings = [get_embedding(x) for x in documents]
# print(embeddings[0])
print(len(embeddings))

print(np.array(embeddings[0]).shape)

def calculate_cosine_metrics(v1, v2):
    dot_product = np.dot(v1, v2)
    magnitude_1 = np.linalg.norm(v1)
    magnitude_2 = np.linalg.norm(v2)
    cosine_similarity = dot_product / (magnitude_1 * magnitude_2)
    cosine_difference = 1 - cosine_similarity
    return int(cosine_similarity * 100), int(cosine_difference * 100)

print(calculate_cosine_metrics(embeddings[0], embeddings[0]))
print(calculate_cosine_metrics(embeddings[0], embeddings[1]))
print(calculate_cosine_metrics(embeddings[0], embeddings[2]))

phrase_1_embedding = get_embedding("The dog ate my homework and then burped it up")
phrase_2_embedding = get_embedding("The green dog ate my homework and then burped it up")
print(calculate_cosine_metrics(phrase_1_embedding, phrase_2_embedding))