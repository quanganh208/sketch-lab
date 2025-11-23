"""
Utility Functions
Helper functions for file handling, image processing, and cleanup
"""

import os
import time
from datetime import datetime
from werkzeug.utils import secure_filename
import cv2
import numpy as np


def allowed_file(filename, allowed_extensions={'png', 'jpg', 'jpeg'}):
    """
    Kiểm tra file có extension hợp lệ không

    Parameters:
    -----------
    filename : str
        Tên file cần kiểm tra
    allowed_extensions : set
        Set các extension được phép

    Returns:
    --------
    bool : True nếu file hợp lệ
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_unique_filename(filename):
    """
    Tạo filename unique bằng cách thêm timestamp

    Parameters:
    -----------
    filename : str
        Tên file gốc

    Returns:
    --------
    str : Filename unique với timestamp
    """
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{name}_{timestamp}{ext}"


def cleanup_old_files(folder, max_age_hours=24):
    """
    Xóa các file cũ hơn max_age_hours

    Parameters:
    -----------
    folder : str
        Đường dẫn thư mục cần cleanup
    max_age_hours : int
        Tuổi tối đa của file (giờ)
    """
    if not os.path.exists(folder):
        return

    current_time = time.time()
    max_age_seconds = max_age_hours * 3600

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)

        # Skip directories
        if os.path.isdir(filepath):
            continue

        # Check file age
        file_age = current_time - os.path.getmtime(filepath)

        if file_age > max_age_seconds:
            try:
                os.remove(filepath)
                print(f"Cleaned up old file: {filename}")
            except Exception as e:
                print(f"Error cleaning up {filename}: {e}")


def resize_image(image, max_width=1024, max_height=1024):
    """
    Resize ảnh nếu quá lớn để tăng tốc xử lý

    Parameters:
    -----------
    image : numpy.ndarray
        Ảnh cần resize
    max_width : int
        Chiều rộng tối đa
    max_height : int
        Chiều cao tối đa

    Returns:
    --------
    numpy.ndarray : Ảnh đã resize
    """
    height, width = image.shape[:2]

    # No need to resize if already small enough
    if width <= max_width and height <= max_height:
        return image

    # Calculate scaling factor
    scale = min(max_width / width, max_height / height)

    # Calculate new dimensions
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Resize
    resized = cv2.resize(image, (new_width, new_height),
                        interpolation=cv2.INTER_AREA)

    return resized


def image_to_base64(image):
    """
    Convert image to base64 string for JSON response

    Parameters:
    -----------
    image : numpy.ndarray
        Ảnh cần convert

    Returns:
    --------
    str : Base64 encoded string
    """
    import base64

    # Encode image to bytes
    success, buffer = cv2.imencode('.png', image)

    if not success:
        raise ValueError("Failed to encode image")

    # Convert to base64
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"


def get_file_size_mb(filepath):
    """
    Get file size in megabytes

    Parameters:
    -----------
    filepath : str
        Đường dẫn file

    Returns:
    --------
    float : File size in MB
    """
    size_bytes = os.path.getsize(filepath)
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)
