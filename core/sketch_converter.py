"""
Sketch Conversion Module
Implements dodge-burn and combined sketch conversion methods
"""

import cv2
import numpy as np
from .edge_detector import EdgeDetector
from .algorithms import GaussianBlur


class SketchConverter:
    """
    Class chuyển đổi ảnh sang sketch
    - cvtColor: chuyển đổi không gian màu
    - bitwise_not: invert ảnh (phép NOT đơn giản)
    - CLAHE: thuật toán phức tạp không phải core
    - bilateralFilter: thuật toán phức tạp không phải core
    """

    def __init__(self, method="dodge_burn"):
        """
        Parameters:
        -----------
        method : str
            'dodge_burn', 'edge_based', 'combined'
        """
        self.method = method
        self.edge_detector = EdgeDetector("canny")
        # Sử dụng GaussianBlur tự implement
        self.gaussian = GaussianBlur()

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

        if self.method == "dodge_burn":
            return self._dodge_burn(gray, **params)
        elif self.method == "combined":
            return self._combined(gray, **params)
        else:
            raise ValueError(
                f"Unknown method: {self.method}. Only 'dodge_burn' and 'combined' are supported."
            )

    def _invert(self, image):
        """
        Invert ảnh (đảo ngược giá trị pixel)

        Công thức: output = 255 - input

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh đầu vào

        Returns:
        --------
        numpy.ndarray : Ảnh đã invert
        """
        return (255 - image).astype(np.uint8)

    def _divide_blend(self, base, blend, scale=256.0):
        """
        Công thức: output = (base * scale) / blend

        Đây là kỹ thuật core của dodge-burn

        Parameters:
        -----------
        base : numpy.ndarray
            Ảnh cơ sở
        blend : numpy.ndarray
            Ảnh để chia
        scale : float
            Hệ số scale

        Returns:
        --------
        numpy.ndarray : Kết quả blend
        """
        # Chuyển sang float để tính toán
        base_f = base.astype(np.float64)
        blend_f = blend.astype(np.float64)

        # Tránh chia cho 0
        blend_f = np.where(blend_f < 1, 1, blend_f)

        # Tính divide
        result = (base_f * scale) / blend_f

        # Clip và chuyển về uint8
        return np.clip(result, 0, 255).astype(np.uint8)

    def _alpha_blend(self, img1, img2, alpha, beta, gamma=0):
        """
        Công thức: output = alpha * img1 + beta * img2 + gamma

        Parameters:
        -----------
        img1 : numpy.ndarray
            Ảnh thứ nhất
        img2 : numpy.ndarray
            Ảnh thứ hai
        alpha : float
            Trọng số ảnh 1
        beta : float
            Trọng số ảnh 2
        gamma : float
            Giá trị cộng thêm

        Returns:
        --------
        numpy.ndarray : Kết quả blend
        """
        result = (
            alpha * img1.astype(np.float64) + beta * img2.astype(np.float64) + gamma
        )
        return np.clip(result, 0, 255).astype(np.uint8)

    def _gamma_correction(self, image, gamma):
        """
        Công thức: output = (input/255)^(1/gamma) * 255

        Gamma > 1: làm sáng ảnh
        Gamma < 1: làm tối ảnh

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh đầu vào
        gamma : float
            Giá trị gamma

        Returns:
        --------
        numpy.ndarray : Ảnh sau gamma correction
        """
        # Tạo lookup table
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype(
            np.uint8
        )

        # Áp dụng lookup table
        return table[image]

    def _dodge_burn(self, gray, blur_ksize=21, sigma=0):
        """
        Dodge and burn blending method

        Các bước:
        1. Preprocessing với CLAHE để cân bằng vùng sáng
        2. Invert ảnh gốc (TỰ IMPLEMENT)
        3. Gaussian Blur ảnh đã invert (TỰ IMPLEMENT)
        4. Invert ảnh đã blur (TỰ IMPLEMENT)
        5. Divide blend với clipping (TỰ IMPLEMENT)

        Tạo hiệu ứng vẽ bút chì tự nhiên với shading mềm mại
        """
        # 0. Apply CLAHE để cải thiện contrast vùng sáng
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # 1. Invert - TỰ IMPLEMENT
        inverted = self._invert(enhanced)

        # 2. Gaussian Blur - TỰ IMPLEMENT
        # Ensure kernel size is odd
        if blur_ksize % 2 == 0:
            blur_ksize += 1

        blurred = self.gaussian.blur(inverted, ksize=blur_ksize, sigma=sigma)

        # 3. Invert blur - TỰ IMPLEMENT
        inverted_blurred = self._invert(blurred)

        # 4. Prevent division by very small numbers (avoid white spots)
        inverted_blurred = np.where(inverted_blurred < 10, 10, inverted_blurred)

        # 5. Divide to create sketch effect - TỰ IMPLEMENT
        # Công thức: Sketch = (Gray * 256) / (255 - Blurred)
        sketch = self._divide_blend(enhanced, inverted_blurred, scale=256.0)

        # 6. Clip values to prevent over-saturation
        sketch = np.clip(sketch, 0, 255).astype(np.uint8)

        # 7. Post-processing: Gaussian blur nhẹ - TỰ IMPLEMENT
        sketch = self.gaussian.blur(sketch, ksize=3, sigma=0.3)

        return sketch

    def _combined(self, gray, blur_ksize=21, low=None, high=None, alpha=0.9, beta=0.1):
        """
        Kết hợp dodge-burn và edge detection với xử lý vùng sáng

        Tạo sketch với:
        - Shading mềm mại từ dodge-burn (90%) - đã cải thiện với CLAHE
        - Biên rõ nét từ Canny tự implement (10%) - adaptive thresholding
        - Gamma correction để tăng độ sáng nền (TỰ IMPLEMENT)

        Kết quả cân bằng giữa artistic và clarity với nền sáng tương đương dodge-burn
        """
        # 1. Tạo sketch từ dodge-burn (đã có CLAHE và clipping)
        sketch_db = self._dodge_burn(gray, blur_ksize=blur_ksize)

        # 2. Phát hiện biên với Canny TỰ IMPLEMENT (qua EdgeDetector)
        edges = self.edge_detector.detect(gray, low_threshold=low, high_threshold=high)

        # 3. Alpha blending - TỰ IMPLEMENT
        sketch = self._alpha_blend(sketch_db, edges, alpha, beta, 0)

        # 4. Áp dụng post-processing
        # a) Bilateral filter nhẹ để giảm đốm trắng, giữ edges
        sketch = cv2.bilateralFilter(sketch, 5, 50, 50)

        # b) Unsharp masking nhẹ để tăng độ sắc nét - TỰ IMPLEMENT
        gaussian = self.gaussian.blur(sketch, ksize=5, sigma=1.5)
        # Sharp = Original×1.3 - Blurred×0.3
        sketch = self._alpha_blend(sketch, gaussian, 1.3, -0.3, 0)

        # c) Gamma correction - TỰ IMPLEMENT
        gamma = 1.15
        sketch = np.clip(sketch, 0, 255).astype(np.uint8)
        sketch = self._gamma_correction(sketch, gamma)

        # Ensure values are in valid range
        sketch = np.clip(sketch, 0, 255).astype(np.uint8)

        return sketch
