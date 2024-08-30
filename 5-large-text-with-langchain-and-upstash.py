import wikipedia
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import UpstashVectorStore
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import TokenTextSplitter

from settings import UPSTASH_VECTOR_REST_TOKEN, UPSTASH_VECTOR_REST_URL

ny = wikipedia.page(title="New York City, New York")
# print(ny.content)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

store = UpstashVectorStore(
    embedding=embeddings,
    index_url=UPSTASH_VECTOR_REST_URL,
    index_token=UPSTASH_VECTOR_REST_TOKEN
)

documents = []
cities = ["New York City, New York", "Lagos Island, Lagos"]
for city in cities:
    wikipedia_page_result = wikipedia.page(title=city)
    doc = Document(
        page_content=wikipedia_page_result.content,
        metadata={
            "source": f"{wikipedia_page_result.url}",
            "title": city
        }
    )
    documents.append(doc)

print(documents[0].metadata)
print(len(documents))

OPENAI_LLM_MODEL = "gpt-4o"
text_splitter = TokenTextSplitter.from_tiktoken_encoder(
    model_name=OPENAI_LLM_MODEL, chunk_size=100, chunk_overlap=0
)

docs = text_splitter.split_documents(documents)
print(len(docs))

# inserted_vectors = store.add_documents(docs)

result = store.similarity_search_with_score("Obalende", k=2)
# print(result)
for doc, score in result:
    print(f"{doc.metadata} - {score}")