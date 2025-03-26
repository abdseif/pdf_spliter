from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import base64
import io

app = Flask(__name__)

@app.route('/split_pdf', methods=['POST'])
def split_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        total_pages = pdf_document.page_count
        chunks = []

        for i in range(0, total_pages, 10):
            pdf_writer = fitz.open()
            for j in range(i, min(i + 10, total_pages)):
                pdf_writer.insert_pdf(pdf_document, from_page=j, to_page=j)
            output_stream = io.BytesIO()
            pdf_writer.save(output_stream)
            output_stream.seek(0)
            encoded_pdf = base64.b64encode(output_stream.read()).decode('utf-8')
            chunks.append(encoded_pdf)

        return jsonify({'chunks': chunks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
