"""
Gaussian Blur Implementation
"""

import numpy as np
from .convolution import Convolution2D


class GaussianBlur:
    """
    Class thực hiện Gaussian Blur từ đầu

    Gaussian Blur là phép làm mờ dựa trên phân phối Gaussian (chuẩn):
    G(x,y) = (1 / 2πσ²) × e^(-(x² + y²) / 2σ²)

    Đặc điểm:
    - Làm mờ đều theo mọi hướng (isotropic)
    - Giảm nhiễu hiệu quả
    - Giữ được cấu trúc tổng thể của ảnh
    - Là bộ lọc tách được (separable) -> tối ưu tính toán

    Ứng dụng trong sketch conversion:
    - Làm mờ trong dodge-burn technique
    - Tiền xử lý trước edge detection
    - Post-processing để làm mượt kết quả
    """

    def __init__(self):
        """Khởi tạo với Convolution2D engine"""
        self.conv = Convolution2D(padding_mode="reflect")

    def _create_gaussian_kernel_1d(self, size, sigma):
        """
        Tạo kernel Gaussian 1D

        Công thức: G(x) = e^(-x² / 2σ²)

        Parameters:
        -----------
        size : int
            Kích thước kernel (phải là số lẻ)
        sigma : float
            Độ lệch chuẩn (sigma càng lớn càng mờ)

        Returns:
        --------
        numpy.ndarray : Kernel Gaussian 1D đã chuẩn hóa
        """
        # Tạo mảng tọa độ từ -size//2 đến size//2
        x = np.arange(size) - size // 2

        # Tính giá trị Gaussian
        kernel = np.exp(-(x**2) / (2 * sigma**2))

        # Chuẩn hóa để tổng = 1 (bảo toàn độ sáng)
        kernel = kernel / kernel.sum()

        return kernel

    def _create_gaussian_kernel_2d(self, size, sigma):
        """
        Tạo kernel Gaussian 2D

        Công thức: G(x,y) = e^(-(x² + y²) / 2σ²)

        Cách 1: Tính trực tiếp từ công thức
        Cách 2: Nhân outer product của 2 kernel 1D (vì separable)

        Parameters:
        -----------
        size : int
            Kích thước kernel (ksize x ksize)
        sigma : float
            Độ lệch chuẩn

        Returns:
        --------
        numpy.ndarray : Kernel Gaussian 2D đã chuẩn hóa
        """
        # Tạo lưới tọa độ
        center = size // 2
        x = np.arange(size) - center
        y = np.arange(size) - center
        xx, yy = np.meshgrid(x, y)

        # Tính Gaussian 2D
        kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))

        # Chuẩn hóa
        kernel = kernel / kernel.sum()

        return kernel

    def _calculate_sigma(self, ksize, sigma):
        """
        Tính sigma nếu không được cung cấp

        Theo OpenCV: sigma = 0.3 * ((ksize-1)*0.5 - 1) + 0.8

        Parameters:
        -----------
        ksize : int
            Kích thước kernel
        sigma : float
            Sigma được cung cấp (0 = tự tính)

        Returns:
        --------
        float : Sigma đã tính
        """
        if sigma <= 0:
            # Công thức của OpenCV
            sigma = 0.3 * ((ksize - 1) * 0.5 - 1) + 0.8
        return sigma

    def blur(self, image, ksize, sigma=0):
        """
        Áp dụng Gaussian blur lên ảnh

        Sử dụng separable convolution để tối ưu:
        - Thay vì O(n² × k²), chỉ cần O(n² × 2k)
        - Kết quả giống hệt nhưng nhanh hơn nhiều

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh grayscale đầu vào
        ksize : int hoặc tuple
            Kích thước kernel. Nếu int, dùng ksize x ksize
            Nếu tuple, dùng (ksize_x, ksize_y)
        sigma : float
            Độ lệch chuẩn (0 = tự tính từ ksize)

        Returns:
        --------
        numpy.ndarray : Ảnh đã blur
        """
        # Xử lý ksize
        if isinstance(ksize, tuple):
            ksize_x, ksize_y = ksize
        else:
            ksize_x = ksize_y = ksize

        # Đảm bảo ksize là số lẻ
        if ksize_x % 2 == 0:
            ksize_x += 1
        if ksize_y % 2 == 0:
            ksize_y += 1

        # Tính sigma
        sigma_x = self._calculate_sigma(ksize_x, sigma)
        sigma_y = self._calculate_sigma(ksize_y, sigma)

        # Tạo kernel 1D cho mỗi chiều
        kernel_x = self._create_gaussian_kernel_1d(ksize_x, sigma_x)
        kernel_y = self._create_gaussian_kernel_1d(ksize_y, sigma_y)

        # Áp dụng separable convolution
        output = self.conv.separable_convolve(image, kernel_x, kernel_y)

        # Clip và chuyển về uint8
        output = np.clip(output, 0, 255).astype(np.uint8)

        return output
