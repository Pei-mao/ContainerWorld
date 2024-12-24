import requests

url = "http://192.168.2.203:11434/api/generate"

data = {
        "model": "tinyllama",
        "prompt": "台灣的總統是誰?",
        "stream": False,
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    print("Response from ollma: \n")
    value = response.json()
    print("The value type of response: ", type(value))
    
    print(value["response"])
else:
    print(f"Error: {response.status_code} - {response.text}")