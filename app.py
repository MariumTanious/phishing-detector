from flask import Flask, request, jsonify, render_template
import pickle
import re
import os

app = Flask(__name__)

#  Load model safely
try:
    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    model = pickle.load(open(model_path, "rb"))
    print("Model loaded successfully")
except Exception as e:
    print("ERROR loading model:", e)
    model = None

# feature extraction
def extract_features(url):
    url = url.lower()

    suspicious_words = [
        'bank', 'secure', 'account', 'login',
        'verify', 'update', 'free', 'bonus',
        'paypal', 'signin', 'confirm'
    ]

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
        1 if any(word in url for word in suspicious_words) else 0,
        sum(word in url for word in suspicious_words),
        len(re.findall(r'\d', url)),
        1 if len(url) > 75 else 0
    ]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"result": "Model not loaded ❌"})

    data = request.get_json()
    url = data.get("url", "")

    features = extract_features(url)
    prediction = model.predict([features])[0]

    return jsonify({
        "result": "Phishing ⚠️" if prediction == 1 else "Safe ✅"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
