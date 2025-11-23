"""
Edge Detection Module
Implements Canny, Sobel, and Laplacian edge detection algorithms
Based on SketchLab Report - Chapter 3 & 5
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
            Phương pháp: 'canny', 'sobel', 'laplacian'
        """
        self.method = method

    def detect(self, image, **params):
        """
        Phát hiện biên trong ảnh

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh đầu vào (grayscale hoặc color)
        params : dict
            Tham số cho từng phương pháp

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
        elif self.method == 'sobel':
            return self._sobel(gray, **params)
        elif self.method == 'laplacian':
            return self._laplacian(gray, **params)
        else:
            raise ValueError(f"Unknown method: {self.method}")

    def _canny(self, image, low_threshold=50, high_threshold=150):
        """
        Canny edge detection

        Thuật toán tốt nhất với 4 bước:
        1. Gaussian smoothing
        2. Gradient calculation
        3. Non-maximum suppression
        4. Hysteresis thresholding
        """
        edges = cv2.Canny(image, low_threshold, high_threshold)
        return edges

    def _sobel(self, image, ksize=3):
        """
        Sobel edge detection

        Sử dụng Sobel operator để tính gradient theo x và y
        Sau đó tính magnitude để có biên
        """
        # Calculate gradients
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)

        # Calculate magnitude
        magnitude = np.sqrt(sobelx**2 + sobely**2)

        # Normalize to 0-255
        magnitude = np.uint8(magnitude / magnitude.max() * 255)

        return magnitude

    def _laplacian(self, image, ksize=3):
        """
        Laplacian edge detection

        Sử dụng đạo hàm bậc 2 (Laplacian operator)
        Nhạy cảm với nhiễu nhưng phát hiện theo mọi hướng
        """
        laplacian = cv2.Laplacian(image, cv2.CV_64F, ksize=ksize)

        # Take absolute value and normalize
        laplacian = np.uint8(np.absolute(laplacian))

        return laplacian
