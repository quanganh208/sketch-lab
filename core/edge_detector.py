"""
Edge Detection Module
Implements Canny edge detection algorithm from scratch
Used for sketch conversion in Combined and Edge-Based methods
"""

import cv2
import numpy as np
from .algorithms import CannyEdgeDetector, GaussianBlur


class EdgeDetector:
    """
    Class xử lý phát hiện biên
    """

    def __init__(self, method="canny"):
        """
        Parameters:
        -----------
        method : str
            Phương pháp: 'canny' (only supported method)
        """
        self.method = method
        # Sử dụng Canny detector tự implement
        self.canny_detector = CannyEdgeDetector()
        self.gaussian = GaussianBlur()

    def detect(self, image, **params):
        """
        Phát hiện biên trong ảnh bằng Canny algorithm

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh đầu vào (grayscale hoặc color)
        params : dict
            Tham số cho Canny

        Returns:
        --------
        edges : numpy.ndarray
            Ảnh biên
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        if self.method == "canny":
            return self._canny(gray, **params)
        else:
            raise ValueError(
                f"Unknown method: {self.method}. Only 'canny' is supported."
            )

    def _canny(self, image, low_threshold=None, high_threshold=None):
        """
        Canny edge detection with adaptive thresholding

        Thuật toán Canny tự implement gồm 5 bước:
        1. Gaussian smoothing - giảm nhiễu
        2. Gradient calculation (Sobel) - tính đạo hàm
        3. Non-maximum suppression - làm mỏng biên
        4. Double thresholding - phân loại biên
        5. Hysteresis - nối các biên

        vì đây là các thuật toán phức tạp không phải trọng tâm
        """
        # Preprocessing: CLAHE để cải thiện contrast vùng sáng
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)

        # Bilateral filter để giảm nhiễu nhưng giữ edges
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

        # Adaptive thresholding based on image statistics
        if low_threshold is None or high_threshold is None:
            # Tính threshold tự động từ median
            median = np.median(denoised)
            sigma = 0.33  # Recommended sigma value

            low_threshold = int(max(0, (1.0 - sigma) * median))
            high_threshold = int(min(255, (1.0 + sigma) * median))

            # Ensure reasonable thresholds
            low_threshold = max(30, low_threshold)
            high_threshold = min(200, high_threshold)

        edges = self.canny_detector.detect(
            denoised,
            low_threshold=low_threshold,
            high_threshold=high_threshold,
            blur_ksize=5,
            blur_sigma=1.4,
            sobel_ksize=3,
        )

        # Post-processing: Gaussian blur nhẹ để anti-aliasing
        edges_smooth = self.gaussian.blur(edges, ksize=3, sigma=0.3)

        return edges_smooth
