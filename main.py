from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

# Configure GenAI
genai.configure(api_key=os.environ['GEMINI'])

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 4096,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
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
        response = generate_content("Translate this text to use gen-alpha keywords (rizz, rizzy, sigma, baddie, ohio, skibidi, gang, fr, ong, no cap, fanum tax, kai cenat and other related terms), make sure to only use gen alpha slang, dont ramble, and the translation should adapt/maintain input's original meaning, only output the translated text with no introduction: " + prompt)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)})

def generate_content(prompt):
    try:
        convo = model.start_chat(history=[])
        convo.send_message(prompt)
        response = convo.last.text
        # Truncate the response if it exceeds 2000 characters
        if len(response) > 2000:
            response = response[:2000]
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
