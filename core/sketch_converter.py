"""
Sketch Conversion Module
Implements dodge-burn, edge-based, and combined sketch conversion methods
Based on SketchLab Report - Chapter 4
"""

import cv2
import numpy as np
from .edge_detector import EdgeDetector


class SketchConverter:
    """Class chuyển đổi ảnh sang sketch"""

    def __init__(self, method='dodge_burn'):
        """
        Parameters:
        -----------
        method : str
            'dodge_burn', 'edge_based', 'combined'
        """
        self.method = method
        self.edge_detector = EdgeDetector('canny')

    def convert(self, image, **params):
        """
        Chuyển đổi ảnh sang sketch

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh đầu vào (có thể màu hoặc grayscale)
        params : dict
            Tham số cho từng phương pháp

        Returns:
        --------
        sketch : numpy.ndarray
            Ảnh sketch
        """
        # Chuyển sang grayscale nếu cần
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        if self.method == 'dodge_burn':
            return self._dodge_burn(gray, **params)
        elif self.method == 'edge_based':
            return self._edge_based(gray, **params)
        elif self.method == 'combined':
            return self._combined(gray, **params)
        else:
            raise ValueError(f"Unknown method: {self.method}")

    def _dodge_burn(self, gray, blur_ksize=21, sigma=0):
        """
        Dodge and burn blending method

        Các bước:
        1. Invert ảnh gốc
        2. Blur ảnh đã invert
        3. Invert ảnh đã blur
        4. Divide ảnh gốc với ảnh đã blur để tạo sketch

        Tạo hiệu ứng vẽ bút chì tự nhiên với shading mềm mại
        """
        # 1. Invert
        inverted = cv2.bitwise_not(gray)

        # 2. Gaussian Blur
        # Ensure kernel size is odd
        if blur_ksize % 2 == 0:
            blur_ksize += 1

        blurred = cv2.GaussianBlur(inverted, (blur_ksize, blur_ksize),
                                   sigmaX=sigma, sigmaY=sigma)

        # 3. Invert blur
        inverted_blurred = cv2.bitwise_not(blurred)

        # 4. Divide to create sketch effect
        # Công thức: Sketch = (Gray * 256) / (255 - Blurred)
        sketch = cv2.divide(gray, inverted_blurred, scale=256.0)

        return sketch

    def _edge_based(self, gray, low=50, high=150):
        """
        Edge detection based sketch

        Sử dụng Canny edge detection để tạo sketch
        Kết quả tập trung vào đường nét, rõ ràng nhưng ít shading
        """
        edges = self.edge_detector.detect(gray,
                                         low_threshold=low,
                                         high_threshold=high)

        # Invert để có nền trắng, nét đen
        sketch = cv2.bitwise_not(edges)

        return sketch

    def _combined(self, gray, blur_ksize=21, low=50, high=150,
                  alpha=0.7, beta=0.3):
        """
        Kết hợp dodge-burn và edge detection

        Tạo sketch với:
        - Shading mềm mại từ dodge-burn (70%)
        - Biên rõ nét từ Canny (30%)

        Kết quả cân bằng giữa artistic và clarity
        """
        # 1. Tạo sketch từ dodge-burn
        sketch_db = self._dodge_burn(gray, blur_ksize=blur_ksize)

        # 2. Phát hiện biên
        edges = self.edge_detector.detect(gray,
                                         low_threshold=low,
                                         high_threshold=high)

        # 3. Kết hợp với alpha blending
        # alpha * sketch + beta * edges
        sketch = cv2.addWeighted(sketch_db, alpha, edges, beta, 0)

        return sketch
