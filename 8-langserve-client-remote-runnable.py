import asyncio
from langserve import RemoteRunnable
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

chain_endpoint = 'http://localhost:8100/chain'

chain = RemoteRunnable(chain_endpoint)

# result = chain.invoke("Tell me about New York")
# print(result)

# It supports asyn-await
# put in a async function
# async for chunk in chain.astream("What do you know about Isaale eko"): 
#     print(chunk)

prompt = PromptTemplate.from_template("Tell me about {topic}")

def format_prompt(inputs):
    prompt_value = prompt.format_prompt(**inputs)
    return prompt_value.to_string()

new_chain = RunnablePassthrough() | format_prompt | chain

new_chain_result = new_chain.invoke({"topic": "Third mainland bridge"})
print(new_chain_result)