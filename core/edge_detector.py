"""
Edge Detection Module
Implements Canny edge detection algorithm
Used for sketch conversion in Combined and Edge-Based methods
"""

import cv2
import numpy as np


class EdgeDetector:
    """Class xử lý phát hiện biên"""

    def __init__(self, method='canny'):
        """
        Parameters:
        -----------
        method : str
            Phương pháp: 'canny' (only supported method)
        """
        self.method = method

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

        if self.method == 'canny':
            return self._canny(gray, **params)
        else:
            raise ValueError(f"Unknown method: {self.method}. Only 'canny' is supported.")

    def _canny(self, image, low_threshold=None, high_threshold=None):
        """
        Canny edge detection with adaptive thresholding

        Thuật toán tốt nhất với 4 bước:
        1. CLAHE preprocessing để cải thiện vùng sáng
        2. Gaussian smoothing
        3. Gradient calculation
        4. Non-maximum suppression
        5. Adaptive hysteresis thresholding

        Nếu không cung cấp threshold, sẽ tự động tính dựa trên median
        """
        # Apply CLAHE để cải thiện contrast vùng sáng
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)

        # Apply bilateral filter để giảm nhiễu nhưng giữ edges
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

        edges = cv2.Canny(denoised, low_threshold, high_threshold)

        # Apply very light Gaussian blur for anti-aliasing only
        # Chỉ làm mượt nhẹ để giảm pixel, không làm mờ
        edges_smooth = cv2.GaussianBlur(edges, (3, 3), 0.3)

        return edges_smooth
