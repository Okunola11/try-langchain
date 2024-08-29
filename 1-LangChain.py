from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from settings import OPEN_API_KEY

LLM_CONFIG = {
    "api_key": OPEN_API_KEY,
    "model": "gpt-4o"
}
model = ChatOpenAI(**LLM_CONFIG)

system_prompt = "Translate the following into {language}"

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input_text}")
])

messages = [
    SystemMessage(content="Translate from English to Spanish"),
    HumanMessage(content="hi!")
]

# result = model.invoke(messages)
# print(f"Model result is -->: {result}")

parser = StrOutputParser()
# parser.invoke(result)

chain = model | parser
# result = chain.invoke(messages)
# print(f"Chained result is -->: {result}")

chain = prompt_template | model | parser
# result = chain.invoke({"language": "Arabic", "input_text": "How are you doing today my friend?"})
# print(results)