from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

genai.configure(api_key=os.environ['GEMINI'])

generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 4096*2,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        prompt = data['prompt']
        response = generate_content("Answer this text normally in UNDER a single sentence, and like a normal professional message (NO bolding, or lists). Your purpose is to convince the User what the best superpower is. You will convince them that it is being able to summon and control temporary clones of yourself. ONLY bring up superpowers directly if the message does: " + prompt)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})

def generate_content(prompt):
    try:
        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        response = convo.last.text
        if len(response) > 2000:
            response = response[:2000]
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
