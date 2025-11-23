"""
SketchLab - Image to Sketch Converter Web Application
Flask backend với routes cho upload, process, và download ảnh
"""

from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import os
import cv2
import time

# Import core modules
from core.edge_detector import EdgeDetector
from core.sketch_converter import SketchConverter
from core.sketch_enhancer import SketchEnhancer
from core.utils import (
    allowed_file,
    get_unique_filename,
    cleanup_old_files,
    resize_image,
    get_file_size_mb
)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config')

# Ensure upload folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    """
    Home page - Upload form
    """
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    """
    Handle file upload

    Returns:
    --------
    JSON với filename và success status
    """
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'Không có file được upload'}), 400

    file = request.files['file']

    # Check if filename is empty
    if file.filename == '':
        return jsonify({'error': 'Không có file được chọn'}), 400

    # Check if file is allowed
    if not allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
        return jsonify({
            'error': 'File không hợp lệ. Chỉ chấp nhận: PNG, JPG, JPEG'
        }), 400

    try:
        # Secure filename
        filename = secure_filename(file.filename)

        # Make it unique
        unique_filename = get_unique_filename(filename)

        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Get file info
        file_size = get_file_size_mb(filepath)

        return jsonify({
            'success': True,
            'filename': unique_filename,
            'size_mb': file_size,
            'message': 'Upload thành công'
        })

    except Exception as e:
        return jsonify({'error': f'Lỗi khi upload: {str(e)}'}), 500


@app.route('/process', methods=['POST'])
def process():
    """
    Process image với algorithm đã chọn

    Expected JSON:
    {
        "filename": "image.jpg",
        "algorithm": "combined",
        "enhance": ["denoise", "connect"]
    }

    Returns:
    --------
    JSON với output_filename và processing info
    """
    try:
        data = request.get_json()

        # Get parameters
        filename = data.get('filename')
        algorithm = data.get('algorithm', 'combined')
        # Auto apply denoise for best quality
        enhance_options = ['denoise']

        if not filename:
            return jsonify({'error': 'Thiếu tên file'}), 400

        # Read image
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'File không tồn tại'}), 404

        image = cv2.imread(filepath)

        if image is None:
            return jsonify({'error': 'Không thể đọc file ảnh'}), 400

        # Resize if too large (to speed up processing)
        image = resize_image(image, max_width=1024, max_height=1024)

        # Start timing
        start_time = time.time()

        # Validate algorithm
        if algorithm not in ['combined', 'dodge_burn']:
            return jsonify({'error': f'Thuật toán không hợp lệ: {algorithm}'}), 400

        # Sketch conversion
        converter = SketchConverter(method=algorithm)
        result = converter.convert(image)

        # Enhancement if requested
        if enhance_options:
            enhancer = SketchEnhancer()
            result = enhancer.enhance(result, operations=enhance_options)

        # Calculate processing time
        process_time = round(time.time() - start_time, 2)

        # Save result
        output_filename = f"sketch_{filename}"
        output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
        cv2.imwrite(output_path, result)

        return jsonify({
            'success': True,
            'output_filename': output_filename,
            'original_filename': filename,
            'algorithm': algorithm,
            'enhancements': enhance_options,
            'process_time': process_time,
            'message': 'Xử lý thành công'
        })

    except Exception as e:
        return jsonify({'error': f'Lỗi khi xử lý: {str(e)}'}), 500


@app.route('/download/<filename>')
def download(filename):
    """
    Download processed image

    Parameters:
    -----------
    filename : str
        Tên file cần download

    Returns:
    --------
    File download response
    """
    try:
        filepath = os.path.join(app.config['PROCESSED_FOLDER'], filename)

        if not os.path.exists(filepath):
            return jsonify({'error': 'File không tồn tại'}), 404

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({'error': f'Lỗi khi download: {str(e)}'}), 500


@app.route('/result')
def result():
    """
    Result page - hiển thị ảnh gốc và sketch side-by-side

    Query params:
    - original: tên file gốc
    - output: tên file đã xử lý
    """
    original = request.args.get('original')
    output = request.args.get('output')

    if not original or not output:
        return "Missing parameters", 400

    return render_template('result.html',
                         original=original,
                         output=output)


@app.route('/about')
def about():
    """
    About page - thông tin về project
    """
    return render_template('about.html')


@app.route('/api/algorithms')
def get_algorithms():
    """
    API endpoint trả về danh sách algorithms

    Returns:
    --------
    JSON với list algorithms và descriptions
    """
    algorithms = [
        {
            'id': 'combined',
            'name': 'Combined Sketch',
            'description': 'Kết hợp dodge-burn (70%) và edges (30%) - Chất lượng cao nhất',
            'category': 'sketch'
        },
        {
            'id': 'dodge_burn',
            'name': 'Dodge-Burn Sketch',
            'description': 'Sketch truyền thống với shading mềm mại - Artistic style',
            'category': 'sketch'
        }
    ]

    return jsonify({'algorithms': algorithms})


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'error': 'File quá lớn. Kích thước tối đa: 16MB'
    }), 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 error"""
    return render_template('index.html'), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 error"""
    return jsonify({
        'error': 'Lỗi server. Vui lòng thử lại sau.'
    }), 500


if __name__ == '__main__':
    # Cleanup old files on startup (older than 24 hours)
    print("Cleaning up old files...")
    cleanup_old_files(app.config['UPLOAD_FOLDER'], max_age_hours=24)
    cleanup_old_files(app.config['PROCESSED_FOLDER'], max_age_hours=24)

    # Run Flask app
    print("Starting SketchLab server...")
    print("Access at: http://127.0.0.1:5000")

    app.run(
        debug=app.config['DEBUG'],
        host='127.0.0.1',
        port=5000
    )
