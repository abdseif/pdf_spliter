from flask import Flask, request, send_file, jsonify
from PyPDF2 import PdfReader, PdfWriter
import io
import zipfile

app = Flask(__name__)

@app.route('/split_pdf', methods=['POST'])
def split_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    input_pdf = PdfReader(uploaded_file.stream)
    total_pages = len(input_pdf.pages)

    chunk_size = 2
    chunks = []

    for i in range(0, total_pages, chunk_size):
        writer = PdfWriter()
        for j in range(i, min(i + chunk_size, total_pages)):
            writer.add_page(input_pdf.pages[j])

        chunk_stream = io.BytesIO()
        writer.write(chunk_stream)
        chunk_stream.seek(0)

        chunks.append((f'TS-{i + 1}-{min(i + chunk_size, total_pages)}.pdf', chunk_stream.read()))

    # Package all chunks into a zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zipf:
        for filename, data in chunks:
            zipf.writestr(filename, data)

    zip_buffer.seek(0)
    return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='chunks.zip')
