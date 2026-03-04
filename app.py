from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()  # .env file load pannudu

app = Flask(__name__)
CORS(app)

# 🔑 API Key - environment variable la irukku (safe!)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

client = Groq(api_key=GROQ_API_KEY)

SHOP_CONTEXT = """
You are a friendly chatbot for a mobile phone shop.

Shop info:
- Products: Smartphones (Samsung, Apple, Redmi, Realme, OnePlus, Vivo, Oppo), Feature phones, Tablets
- Services: Mobile repair, Screen replacement, Battery replacement, Software flashing, Accessories
- Accessories: Cases, Chargers, Earphones, Screen guards, Power banks, Bluetooth speakers
- Price range: Budget phones (5k-15k), Mid-range (15k-30k), Premium (30k+)
- Offers: EMI available, Exchange offers, Free screen guard on purchase

Your job:
1. Help customers find the right phone based on budget and needs
2. Answer questions about specs, price, availability
3. Suggest best options based on what they ask
4. After 2-3 questions, ask if they want to visit the shop or get a callback
5. Keep responses SHORT and friendly (2-4 sentences)

IMPORTANT: Reply in the same language the user uses. Tamil la keataal Tamil la sollu. English la keataal English la sollu.
"""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        messages = data.get('messages', [])

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SHOP_CONTEXT},
                *messages
            ],
            max_tokens=300,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("✅ Mobile Shop Chatbot Server Running!")
    print("🌐 Open index.html in browser")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
