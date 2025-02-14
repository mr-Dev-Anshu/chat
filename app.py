from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Replace with your OpenAI API key
openai.api_key = 'your-openai-api-key'

# Product and service information
PRODUCTS = {
    "Battery Management Systems": "Advanced systems ensuring optimal battery performance.",
    "Lithium-ion Batteries": "High-quality battery packs for the Indian 2W and 3W market.",
    "Charging Stations": "Charging infrastructure deployed across India.",
    "Battery Recycling": "Services including sorting, repurposing, and recycling of old cells.",
    "Battery Leasing": "Batteries available for rent.",
    "Battery Fire Safety Products": "Products to prevent and extinguish lithium-ion battery fires."
}

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "I'm sorry, I didn't understand that."})

    # Construct the prompt for OpenAI
    prompt = f"""
    You are a sales assistant for VoltQ Energy, a company specializing in:
    - Battery Management Systems: {PRODUCTS['Battery Management Systems']}
    - Lithium-ion Batteries: {PRODUCTS['Lithium-ion Batteries']}
    - Charging Stations: {PRODUCTS['Charging Stations']}
    - Battery Recycling: {PRODUCTS['Battery Recycling']}
    - Battery Leasing: {PRODUCTS['Battery Leasing']}
    - Battery Fire Safety Products: {PRODUCTS['Battery Fire Safety Products']}

    Your task is to assist customers by understanding their requirements, providing information, negotiating prices, and closing deals.

    Customer: {user_message}
    Sales Assistant:
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        bot_reply = response.choices[0].text.strip()
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": "I'm sorry, there was an error processing your request."})

if __name__ == '__main__':
    app.run(debug=True)