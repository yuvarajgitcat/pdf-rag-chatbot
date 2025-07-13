from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from rag_pipeline import ingest_pdf, answer_question



app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "RAG Chatbot backend is running!"


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        save_path = os.path.join("uploads", file.filename)
        file.save(save_path)
        ingest_pdf(save_path)
        return jsonify({"message": "File uploaded and processed."})
    return jsonify({"error": "No file uploaded"}), 400

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400
    answer = answer_question(question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
