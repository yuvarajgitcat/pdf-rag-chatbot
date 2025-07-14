from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from rag_pipeline import ingest_pdf, answer_question

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "RAG Chatbot backend is running!"})

@app.route("/upload", methods=["POST"])
def upload():
    try:
        # ✅ Correct key name check
        if 'file' not in request.files:
            return jsonify({"error": "No PDF file found in request."}), 400

        file = request.files['file']  # ✅ Match this with frontend

        if file.filename == '':
            return jsonify({"error": "No selected file."}), 400

        if not file.filename.endswith('.pdf'):
            return jsonify({"error": "Only PDF files are supported."}), 400

        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)

        ingest_pdf(save_path)

        return jsonify({"message": "PDF uploaded and processed successfully."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()
        if not question:
            return jsonify({"error": "No question provided."}), 400

        answer = answer_question(question)
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
