import requests

url = "https://sandbox.openfinance.celcoin.dev/vehicledebtsapi/v1/debts"

payload = {
    "state": "DF",
    "licensePlate": "DIS9865",
    "renavam": "01203988813",
    "cpfCnpj": "81183207077",
    "clientRequestId": "f6c44940-7010-11ed-9eba-91c4cd147db9"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)