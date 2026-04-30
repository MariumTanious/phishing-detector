import os
import pickle
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# ✅ حماية لو الملف مش موجود
model_path = "model.pkl"

if not os.path.exists(model_path):
    raise Exception("model.pkl not found in deployment")

model = pickle.load(open(model_path, "rb"))

@app.route("/")
def home():
    return "🚀 Phishing Detector Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data["url"]

    features = extract_features(url)
    prediction = model.predict([features])[0]

    return jsonify({
        "result": "Phishing ⚠️" if prediction == 1 else "Safe ✅"
    })


def extract_features(url):
    url = url.lower()
    suspicious_words = ['bank','secure','account','login','verify','update','free','bonus','paypal','signin','confirm']

    return [
        len(url),
        url.count('.'),
        url.count('-'),
        url.count('/'),
        len(url.split('.')),
        1 if '@' in url else 0,
        1 if 'https' in url else 0,
        1 if 'http://' in url else 0,
        1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        1 if any(w in url for w in suspicious_words) else 0,
        sum(w in url for w in suspicious_words),
        len(re.findall(r'\d', url)),
        1 if len(url) > 75 else 0
    ]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
