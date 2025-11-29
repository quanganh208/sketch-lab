"""
Sobel Operator Implementation
"""

import numpy as np
from .convolution import Convolution2D


class SobelOperator:
    """
    Class thực hiện toán tử Sobel từ đầu

    Sobel operator tính xấp xỉ đạo hàm (gradient) của ảnh:
    - Gradient theo x: phát hiện biên dọc
    - Gradient theo y: phát hiện biên ngang
    - Magnitude: cường độ biên tổng hợp
    - Direction: hướng của biên

    Kernel Sobel 3x3:
    Gx = [[-1, 0, 1],      Gy = [[-1, -2, -1],
          [-2, 0, 2],            [ 0,  0,  0],
          [-1, 0, 1]]            [ 1,  2,  1]]

    Sobel là nền tảng cho:
    - Canny edge detection
    - Corner detection
    - Optical flow
    - Feature extraction
    """

    def __init__(self):
        """Khởi tạo với kernels và convolution engine"""
        self.conv = Convolution2D(padding_mode="reflect")

        # Kernel Sobel 3x3 chuẩn
        self.kernel_x_3 = np.array(
            [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64
        )

        self.kernel_y_3 = np.array(
            [[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64
        )

        # Kernel Sobel 5x5 (cho độ chính xác cao hơn)
        self.kernel_x_5 = np.array(
            [
                [-1, -2, 0, 2, 1],
                [-4, -8, 0, 8, 4],
                [-6, -12, 0, 12, 6],
                [-4, -8, 0, 8, 4],
                [-1, -2, 0, 2, 1],
            ],
            dtype=np.float64,
        )

        self.kernel_y_5 = np.array(
            [
                [-1, -4, -6, -4, -1],
                [-2, -8, -12, -8, -2],
                [0, 0, 0, 0, 0],
                [2, 8, 12, 8, 2],
                [1, 4, 6, 4, 1],
            ],
            dtype=np.float64,
        )

    def _get_kernels(self, ksize):
        """
        Lấy kernel theo kích thước

        Parameters:
        -----------
        ksize : int
            Kích thước kernel (3 hoặc 5)

        Returns:
        --------
        tuple : (kernel_x, kernel_y)
        """
        if ksize == 5:
            return self.kernel_x_5, self.kernel_y_5
        else:
            return self.kernel_x_3, self.kernel_y_3

    def compute_all(self, image, ksize=3):
        """
        Tính tất cả: gradient x, y, magnitude, direction

        Công thức:
        - Gx: tích chập với kernel Sobel x
        - Gy: tích chập với kernel Sobel y
        - Magnitude: M = sqrt(Gx² + Gy²)
        - Direction: θ = arctan2(Gy, Gx)

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh grayscale
        ksize : int
            Kích thước kernel (3 hoặc 5)

        Returns:
        --------
        dict : {'gx': gradient_x, 'gy': gradient_y,
                'magnitude': magnitude, 'direction': direction}
        """
        kernel_x, kernel_y = self._get_kernels(ksize)

        # Tính gradient x và y
        gx = self.conv.convolve_fast(image.astype(np.float64), kernel_x)
        gy = self.conv.convolve_fast(image.astype(np.float64), kernel_y)

        # Tính magnitude và direction
        mag = np.sqrt(gx**2 + gy**2)
        direction = np.arctan2(gy, gx)

        return {"gx": gx, "gy": gy, "magnitude": mag, "direction": direction}
