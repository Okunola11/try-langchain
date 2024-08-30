import requests

endpoint = "http://localhost:8100/chain"
chain_type = "invoke"
url = f"{endpoint}/{chain_type}"

data = {"input": "Tell me about Lagos Island"}

r = requests.post(url, json=data)
print(r.json()['output'])