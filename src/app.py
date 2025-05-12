from flask import Flask, request, jsonify, render_template
from models.ai_model import AIModel

app = Flask(__name__)
ai_model = AIModel()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return an empty response with status code 204 (No Content)

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('question')
    context = request.json.get('context', "This is a sample context for testing.")
    if not user_input:
        return jsonify({'error': 'No question provided'}), 400
    answer = ai_model.predict(user_input, context)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True, port=5001)