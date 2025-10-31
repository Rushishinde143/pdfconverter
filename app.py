from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
import io

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    images = request.files.getlist('images')
    layout = request.form.get('layout', 'portrait')

    if not images:
        return jsonify({'error': 'No images uploaded'}), 400

    image_list = []

    try:
        for img in images:
            try:
                image = Image.open(img).convert('RGB')
                if layout == 'landscape':
                    image = image.rotate(270, expand=True)
                image_list.append(image)
            except UnidentifiedImageError:
                return jsonify({'error': f'Invalid image file: {img.filename}'}), 400

        if not image_list:
            return jsonify({'error': 'No valid images to convert'}), 400

        pdf_bytes = io.BytesIO()
        image_list[0].save(pdf_bytes, format='PDF', save_all=True, append_images=image_list[1:])
        pdf_bytes.seek(0)

        return send_file(pdf_bytes, download_name='converted.pdf', as_attachment=True, mimetype='application/pdf')

    except Exception as e:
        return jsonify({'error': 'Failed to generate PDF', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
