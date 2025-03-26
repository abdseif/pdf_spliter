from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import base64
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "PDF Splitter is Live!"

@app.route('/split_pdf', methods=['POST'])
def split_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    chunks = []

    for i in range(0, pdf.page_count, 10):
        chunk = fitz.open()
        chunk.insert_pdf(pdf, from_page=i, to_page=min(i + 9, pdf.page_count - 1))
        stream = io.BytesIO()
        chunk.save(stream)
        encoded = base64.b64encode(stream.getvalue()).decode("utf-8")
        chunks.append(encoded)

    return jsonify({ "chunks": chunks })

if __name__ == "__main__":
    app.run()
