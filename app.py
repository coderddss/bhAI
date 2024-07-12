from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = 'YOUR_OPENAI_API_KEY'

def generate_response(prompt, user_data):
    user_data_text = f"User likes: {user_data.get('likes', '')}. User dislikes: {user_data.get('dislikes', '')}. User interests: {user_data.get('interests', '')}."
    full_prompt = f"{user_data_text} {prompt}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.9,
    )
    return response.choices[0].text.strip()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    user_data = data.get('user_data', {})
    context = data.get('context', '')

    prompt = f"You are a friendly and fun chatbot named ChatBuddy. {context} User: {user_message}\nChatBuddy:"
    response = generate_response(prompt, user_data)

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)
