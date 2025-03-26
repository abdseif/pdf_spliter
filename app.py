from flask import Flask, request, jsonify
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/")
def index():
    return "PDF Splitter is live!"

@app.route("/split_pdf", methods=["POST"])
def split_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    input_pdf = PdfReader(file.stream)

    chunks = []
    chunk_size = 10  # Pages per split

    for start in range(0, len(input_pdf.pages), chunk_size):
        writer = PdfWriter()
        for i in range(start, min(start + chunk_size, len(input_pdf.pages))):
            writer.add_page(input_pdf.pages[i])

        buffer = BytesIO()
        writer.write(buffer)
        buffer.seek(0)
        b64_data = base64.b64encode(buffer.read()).decode("utf-8")
        chunks.append(b64_data)

    return jsonify({"chunks": chunks})
