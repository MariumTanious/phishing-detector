import requests

res = requests.post("http://127.0.0.1:5000/predict", json={
    "url": "http://secure-bank-login.com"
})

print(res.json())