import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import UpstashVectorStore

from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from settings import OPEN_API_KEY, UPSTASH_VECTOR_REST_TOKEN, UPSTASH_VECTOR_REST_URL

os.environ['OPENAI_API_KEY'] = OPEN_API_KEY

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

store = UpstashVectorStore(
    embedding=embeddings,
    index_url=UPSTASH_VECTOR_REST_URL,
    index_token=UPSTASH_VECTOR_REST_TOKEN
)

retriever = store.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 2}
)

# test_search = retriever.invoke("Which city is surrounded by water")
# print(test_search)

LLM_CONFIG = {
    "model": "gpt-4o-mini",
    "api_key": OPEN_API_KEY
}
llm = ChatOpenAI(**LLM_CONFIG)

message = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

prompt = ChatPromptTemplate.from_messages(["human", message])

parser = StrOutputParser()

chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm | parser

# result = chain.invoke("Where is lagos island located")
# result = chain.invoke("what is the best food in New York")
# print(result)