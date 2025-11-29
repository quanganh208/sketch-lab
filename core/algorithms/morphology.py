"""
Morphological Operations Implementation
"""

import numpy as np


class MorphologicalOperations:
    """
    Class thực hiện các phép toán hình thái học từ đầu

    Morphological operations làm việc trên cấu trúc hình học của ảnh:
    - Dựa trên lý thuyết tập hợp
    - Sử dụng structuring element (kernel) để thăm dò ảnh
    - Thường dùng cho ảnh nhị phân nhưng cũng áp dụng được cho grayscale

    Các phép toán cơ bản:
    1. Erosion (co): Thu nhỏ vùng sáng, mở rộng vùng tối
    2. Dilation (giãn): Mở rộng vùng sáng, thu nhỏ vùng tối
    3. Opening: Erosion + Dilation (loại bỏ nhiễu nhỏ)
    4. Closing: Dilation + Erosion (lấp đầy lỗ nhỏ)

    Ứng dụng trong sketch:
    - Loại bỏ nhiễu (noise removal)
    - Làm mỏng nét vẽ (thinning)
    - Nối các đường đứt (gap filling)
    """

    def __init__(self):
        """Khởi tạo với các kernel mặc định"""
        pass

    def create_kernel(self, shape, size):
        """
        Tạo structuring element (kernel)

        Parameters:
        -----------
        shape : str
            Hình dạng: 'rect', 'ellipse', 'cross'
        size : int hoặc tuple
            Kích thước kernel

        Returns:
        --------
        numpy.ndarray : Kernel (binary, 0 hoặc 1)
        """
        if isinstance(size, int):
            size = (size, size)

        h, w = size

        if shape == "rect":
            # Kernel hình chữ nhật (tất cả 1)
            return np.ones((h, w), dtype=np.uint8)

        elif shape == "ellipse":
            # Kernel hình ellipse
            kernel = np.zeros((h, w), dtype=np.uint8)
            center_y, center_x = h // 2, w // 2
            radius_y, radius_x = h / 2, w / 2

            for i in range(h):
                for j in range(w):
                    # Phương trình ellipse: (x/a)² + (y/b)² <= 1
                    dy = (i - center_y) / radius_y if radius_y > 0 else 0
                    dx = (j - center_x) / radius_x if radius_x > 0 else 0
                    if dx**2 + dy**2 <= 1:
                        kernel[i, j] = 1

            return kernel

        elif shape == "cross":
            # Kernel hình chữ thập
            kernel = np.zeros((h, w), dtype=np.uint8)
            center_y, center_x = h // 2, w // 2

            # Đường ngang
            kernel[center_y, :] = 1
            # Đường dọc
            kernel[:, center_x] = 1

            return kernel

        else:
            # Mặc định là rect
            return np.ones((h, w), dtype=np.uint8)

    def erode_fast(self, image, kernel):
        """
        Erosion tối ưu bằng vectorization

        Sử dụng sliding window và numpy operations

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh đầu vào
        kernel : numpy.ndarray
            Structuring element

        Returns:
        --------
        numpy.ndarray : Ảnh sau erosion
        """
        img_h, img_w = image.shape
        ker_h, ker_w = kernel.shape

        pad_h, pad_w = ker_h // 2, ker_w // 2
        padded = np.pad(
            image,
            ((pad_h, pad_h), (pad_w, pad_w)),
            mode="constant",
            constant_values=255,
        )

        # Tạo view của tất cả các windows
        shape = (img_h, img_w, ker_h, ker_w)
        strides = padded.strides * 2
        windows = np.lib.stride_tricks.as_strided(padded, shape=shape, strides=strides)

        # Áp dụng kernel mask và tìm min
        # Đặt vị trí kernel=0 thành 255 để không ảnh hưởng đến min
        kernel_mask = kernel.astype(bool)
        output = np.min(np.where(kernel_mask, windows, 255), axis=(2, 3))

        return output.astype(np.uint8)

    def dilate_fast(self, image, kernel):
        """
        Dilation tối ưu bằng vectorization

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh đầu vào
        kernel : numpy.ndarray
            Structuring element

        Returns:
        --------
        numpy.ndarray : Ảnh sau dilation
        """
        img_h, img_w = image.shape
        ker_h, ker_w = kernel.shape

        pad_h, pad_w = ker_h // 2, ker_w // 2
        padded = np.pad(
            image, ((pad_h, pad_h), (pad_w, pad_w)), mode="constant", constant_values=0
        )

        shape = (img_h, img_w, ker_h, ker_w)
        strides = padded.strides * 2
        windows = np.lib.stride_tricks.as_strided(padded, shape=shape, strides=strides)

        kernel_mask = kernel.astype(bool)
        output = np.max(np.where(kernel_mask, windows, 0), axis=(2, 3))

        return output.astype(np.uint8)

    def opening(self, image, kernel):
        """
        Phép opening = Erosion rồi Dilation

        Tác dụng:
        - Loại bỏ nhiễu nhỏ (điểm sáng nhỏ)
        - Giữ nguyên cấu trúc lớn
        - Làm mịn biên từ bên ngoài

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh đầu vào
        kernel : numpy.ndarray
            Structuring element

        Returns:
        --------
        numpy.ndarray : Ảnh sau opening
        """
        eroded = self.erode_fast(image, kernel)
        opened = self.dilate_fast(eroded, kernel)
        return opened
