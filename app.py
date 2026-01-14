from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

feedback_store = []

POSITIVE_WORDS = ["shiny", "elegant", "premium", "beautiful", "comfortable", "durable", "love", "great"]
NEGATIVE_WORDS = ["tarnish", "dull", "heavy", "broke", "uncomfortable", "fragile", "bad", "poor"]

THEME_KEYWORDS = {
    "Comfort": ["light", "heavy", "fit", "wearable", "comfortable", "uncomfortable"],
    "Durability": ["broke", "strong", "quality", "fragile", "tarnish", "lasting"],
    "Appearance": ["shiny", "dull", "design", "polish", "beautiful", "elegant"]
}

def analyze_sentiment(text, rating):
    text_lower = text.lower()
    pos_count = sum(1 for word in POSITIVE_WORDS if word in text_lower)
    neg_count = sum(1 for word in NEGATIVE_WORDS if word in text_lower)
    
    if rating <= 2: return "Negative"
    if rating >= 4 and neg_count == 0: return "Positive"
    
    if pos_count > neg_count: return "Positive"
    if neg_count > pos_count: return "Negative"
    return "Neutral"

def detect_themes(text):
    text_lower = text.lower()
    return [theme for theme, keys in THEME_KEYWORDS.items() if any(k in text_lower for k in keys)]

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    sentiment = analyze_sentiment(data['review_text'], int(data['rating']))
    themes = detect_themes(data['review_text'])

    entry = {
        "product_id": data['product_id'],
        "rating": int(data['rating']),
        "review_text": data['review_text'],
        "sentiment": sentiment,
        "themes": themes
    }
    feedback_store.append(entry)
    return jsonify(entry), 201

@app.route('/feedback/<product_id>', methods=['GET'])
def get_feedback(product_id):
    return jsonify([f for f in feedback_store if f['product_id'] == product_id]), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
