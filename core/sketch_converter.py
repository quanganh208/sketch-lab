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
        1. Preprocessing với CLAHE để cân bằng vùng sáng
        2. Invert ảnh gốc
        3. Blur ảnh đã invert
        4. Invert ảnh đã blur
        5. Divide với clipping để tránh đốm trắng

        Tạo hiệu ứng vẽ bút chì tự nhiên với shading mềm mại
        """
        # 0. Apply CLAHE để cải thiện contrast vùng sáng
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # 1. Invert
        inverted = cv2.bitwise_not(enhanced)

        # 2. Gaussian Blur
        # Ensure kernel size is odd
        if blur_ksize % 2 == 0:
            blur_ksize += 1

        blurred = cv2.GaussianBlur(inverted, (blur_ksize, blur_ksize),
                                   sigmaX=sigma, sigmaY=sigma)

        # 3. Invert blur
        inverted_blurred = cv2.bitwise_not(blurred)

        # 4. Prevent division by very small numbers (avoid white spots)
        # Add minimum threshold to avoid saturation
        inverted_blurred = np.where(inverted_blurred < 10, 10, inverted_blurred)

        # 5. Divide to create sketch effect
        # Công thức: Sketch = (Gray * 256) / (255 - Blurred)
        sketch = cv2.divide(enhanced, inverted_blurred, scale=256.0)

        # 6. Clip values to prevent over-saturation
        sketch = np.clip(sketch, 0, 255).astype(np.uint8)

        # 7. Post-processing: Rất nhẹ để giảm pixel nhưng giữ sắc nét
        sketch = cv2.GaussianBlur(sketch, (3, 3), 0.3)

        return sketch

    def _edge_based(self, gray, low=50, high=150):
        """
        Edge detection based sketch với edge smoothing

        Sử dụng Canny edge detection để tạo sketch
        Kết quả tập trung vào đường nét, rõ ràng nhưng ít shading
        Thêm smoothing để đường nét mượt mà hơn
        """
        edges = self.edge_detector.detect(gray,
                                         low_threshold=low,
                                         high_threshold=high)

        # Invert để có nền trắng, nét đen
        sketch = cv2.bitwise_not(edges)

        # Apply Gaussian blur rất nhẹ để anti-aliasing
        sketch = cv2.GaussianBlur(sketch, (3, 3), 0.3)

        return sketch

    def _combined(self, gray, blur_ksize=21, low=None, high=None,
                  alpha=0.7, beta=0.3):
        """
        Kết hợp dodge-burn và edge detection với xử lý vùng sáng

        Tạo sketch với:
        - Shading mềm mại từ dodge-burn (70%) - đã cải thiện với CLAHE
        - Biên rõ nét từ Canny (30%) - adaptive thresholding
        - Xử lý đặc biệt cho vùng sáng

        Kết quả cân bằng giữa artistic và clarity
        """
        # 1. Tạo sketch từ dodge-burn (đã có CLAHE và clipping)
        sketch_db = self._dodge_burn(gray, blur_ksize=blur_ksize)

        # 2. Phát hiện biên với adaptive thresholding
        # Truyền None để dùng adaptive, hoặc giá trị cụ thể nếu có
        edges = self.edge_detector.detect(gray,
                                         low_threshold=low,
                                         high_threshold=high)

        # 3. Kết hợp với alpha blending
        # alpha * sketch + beta * edges
        sketch = cv2.addWeighted(sketch_db, alpha, edges, beta, 0)

        # 4. Áp dụng post-processing - cân bằng giữa mượt và sắc nét
        # a) Bilateral filter nhẹ để giảm đốm trắng, giữ edges
        sketch = cv2.bilateralFilter(sketch, 5, 50, 50)

        # b) Unsharp masking mạnh để tăng độ sắc nét
        # Tạo version mờ
        gaussian = cv2.GaussianBlur(sketch, (5, 5), 1.5)
        # Sharp = Original×2.0 - Blurred×1.0 (tăng cường độ sharp)
        sketch = cv2.addWeighted(sketch, 2.0, gaussian, -1.0, 0)

        # c) Morphological gradient để tăng cường edges
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        gradient = cv2.morphologyEx(sketch, cv2.MORPH_GRADIENT, kernel)
        # Blend gradient vào để làm rõ edges
        sketch = cv2.addWeighted(sketch, 0.9, gradient, 0.1, 0)

        # Ensure values are in valid range
        sketch = np.clip(sketch, 0, 255).astype(np.uint8)

        return sketch
