"""
Canny Edge Detection Implementation
"""

import numpy as np
from .gaussian_blur import GaussianBlur
from .sobel import SobelOperator


class CannyEdgeDetector:
    """
    Class thực hiện Canny Edge Detection từ đầu

    Thuật toán Canny gồm 5 bước:
    1. Noise reduction: Làm mờ Gaussian để giảm nhiễu
    2. Gradient calculation: Tính gradient bằng Sobel
    3. Non-maximum suppression: Làm mỏng biên
    4. Double thresholding: Phân loại pixel biên
    5. Edge tracking by hysteresis: Nối các biên yếu với biên mạnh

    Canny được coi là detector tối ưu vì:
    - Good detection: phát hiện đúng biên thật
    - Good localization: vị trí biên chính xác
    - Minimal response: mỗi biên chỉ được đánh dấu 1 lần
    """

    def __init__(self):
        """Khởi tạo các component cần thiết"""
        self.gaussian = GaussianBlur()
        self.sobel = SobelOperator()

    def _non_maximum_suppression(self, magnitude, direction):
        """
        Bước 3: Non-maximum suppression

        Làm mỏng biên bằng cách:
        - Với mỗi pixel, so sánh với 2 pixel láng giềng theo hướng gradient
        - Chỉ giữ pixel nếu nó là maximum cục bộ

        Parameters:
        -----------
        magnitude : numpy.ndarray
            Cường độ gradient
        direction : numpy.ndarray
            Hướng gradient (radians)

        Returns:
        --------
        numpy.ndarray : Ảnh sau NMS (biên mỏng hơn)
        """
        rows, cols = magnitude.shape
        output = np.zeros_like(magnitude)

        # Chuyển direction từ radians sang degrees
        angle = np.degrees(direction)
        # Đưa về khoảng 0-180 (vì biên đối xứng)
        angle[angle < 0] += 180

        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                # Lấy 2 pixel láng giềng theo hướng gradient
                # Có 4 hướng chính: 0°, 45°, 90°, 135°

                q = 255  # Pixel trước (theo hướng gradient)
                r = 255  # Pixel sau (ngược hướng gradient)

                # Hướng 0° (ngang) -> so sánh trái-phải
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    q = magnitude[i, j + 1]
                    r = magnitude[i, j - 1]

                # Hướng 45° -> so sánh chéo
                elif 22.5 <= angle[i, j] < 67.5:
                    q = magnitude[i + 1, j - 1]
                    r = magnitude[i - 1, j + 1]

                # Hướng 90° (dọc) -> so sánh trên-dưới
                elif 67.5 <= angle[i, j] < 112.5:
                    q = magnitude[i + 1, j]
                    r = magnitude[i - 1, j]

                # Hướng 135° -> so sánh chéo ngược
                elif 112.5 <= angle[i, j] < 157.5:
                    q = magnitude[i - 1, j - 1]
                    r = magnitude[i + 1, j + 1]

                # Giữ pixel nếu nó là maximum
                if magnitude[i, j] >= q and magnitude[i, j] >= r:
                    output[i, j] = magnitude[i, j]
                else:
                    output[i, j] = 0

        return output

    def _double_threshold(self, image, low_ratio=0.05, high_ratio=0.15):
        """
        Bước 4: Double thresholding

        Phân loại pixel thành 3 loại:
        - Strong edge: > high_threshold (chắc chắn là biên)
        - Weak edge: giữa low và high (có thể là biên)
        - Non-edge: < low_threshold (không phải biên)

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh sau NMS
        low_ratio : float
            Tỷ lệ cho low threshold (so với max)
        high_ratio : float
            Tỷ lệ cho high threshold

        Returns:
        --------
        tuple : (result, weak_value, strong_value)
        """
        high_threshold = image.max() * high_ratio
        low_threshold = high_threshold * low_ratio

        rows, cols = image.shape
        result = np.zeros_like(image)

        # Định nghĩa giá trị cho weak và strong edge
        weak = 50
        strong = 255

        # Tìm vị trí strong và weak edges
        strong_i, strong_j = np.where(image >= high_threshold)
        weak_i, weak_j = np.where((image >= low_threshold) & (image < high_threshold))

        result[strong_i, strong_j] = strong
        result[weak_i, weak_j] = weak

        return result, weak, strong

    def _hysteresis(self, image, weak, strong):
        """
        Bước 5: Edge tracking by hysteresis

        Kết nối weak edges với strong edges:
        - Weak edge được giữ nếu kết nối với strong edge
        - Weak edge bị loại bỏ nếu không kết nối

        Sử dụng flood-fill approach:
        - Duyệt qua tất cả strong edges
        - Với mỗi strong edge, tìm weak edges lân cận và chuyển thành strong

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh sau double thresholding
        weak : int
            Giá trị của weak edge
        strong : int
            Giá trị của strong edge

        Returns:
        --------
        numpy.ndarray : Ảnh biên cuối cùng
        """
        rows, cols = image.shape
        result = image.copy()

        # Duyệt nhiều lần để đảm bảo tất cả weak edges được kết nối
        for _ in range(3):  # Thường 2-3 lần là đủ
            for i in range(1, rows - 1):
                for j in range(1, cols - 1):
                    if result[i, j] == weak:
                        # Kiểm tra 8 pixel lân cận
                        neighbors = [
                            result[i - 1, j - 1],
                            result[i - 1, j],
                            result[i - 1, j + 1],
                            result[i, j - 1],
                            result[i, j + 1],
                            result[i + 1, j - 1],
                            result[i + 1, j],
                            result[i + 1, j + 1],
                        ]

                        # Nếu có strong edge lân cận, chuyển thành strong
                        if strong in neighbors:
                            result[i, j] = strong
                        else:
                            result[i, j] = 0

        return result

    def detect(
        self,
        image,
        low_threshold=None,
        high_threshold=None,
        blur_ksize=5,
        blur_sigma=1.4,
        sobel_ksize=3,
    ):
        """
        Phát hiện biên bằng thuật toán Canny

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh grayscale đầu vào
        low_threshold : int hoặc None
            Ngưỡng thấp (None = tự động tính)
        high_threshold : int hoặc None
            Ngưỡng cao (None = tự động tính)
        blur_ksize : int
            Kích thước kernel Gaussian blur
        blur_sigma : float
            Sigma cho Gaussian blur
        sobel_ksize : int
            Kích thước kernel Sobel (3 hoặc 5)

        Returns:
        --------
        numpy.ndarray : Ảnh biên (0 hoặc 255)
        """
        # Đảm bảo input là grayscale
        if len(image.shape) == 3:
            # Chuyển sang grayscale thủ công
            # Y = 0.299*R + 0.587*G + 0.114*B
            image = (
                0.299 * image[:, :, 2] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 0]
            ).astype(np.uint8)

        # Bước 1: Gaussian blur để giảm nhiễu
        blurred = self.gaussian.blur(image, blur_ksize, blur_sigma)

        # Bước 2: Tính gradient bằng Sobel
        gradients = self.sobel.compute_all(blurred, sobel_ksize)
        magnitude = gradients["magnitude"]
        direction = gradients["direction"]

        # Chuẩn hóa magnitude về 0-255
        magnitude = (
            (magnitude / magnitude.max() * 255) if magnitude.max() > 0 else magnitude
        )

        # Bước 3: Non-maximum suppression
        nms = self._non_maximum_suppression(magnitude, direction)

        # Bước 4: Double thresholding
        # Nếu threshold được cung cấp, tính ratio từ đó
        if low_threshold is not None and high_threshold is not None:
            # Chuyển threshold tuyệt đối sang ratio
            max_val = nms.max() if nms.max() > 0 else 255
            high_ratio = high_threshold / max_val
            low_ratio = low_threshold / high_threshold
        else:
            # Tự động tính threshold từ thống kê ảnh
            median = np.median(blurred)
            sigma = 0.33
            low_threshold = int(max(0, (1.0 - sigma) * median))
            high_threshold = int(min(255, (1.0 + sigma) * median))

            max_val = nms.max() if nms.max() > 0 else 255
            high_ratio = min(0.25, high_threshold / max_val)
            low_ratio = 0.4  # low = 40% của high

        threshold_result, weak, strong = self._double_threshold(
            nms, low_ratio, high_ratio
        )

        # Bước 5: Hysteresis
        edges = self._hysteresis(threshold_result, weak, strong)

        return edges.astype(np.uint8)
