"""
2D Convolution Implementation
Thực hiện phép tích chập 2D - nền tảng cho các thuật toán xử lý ảnh
"""

import numpy as np


class Convolution2D:
    """
    Class thực hiện phép tích chập 2D từ đầu

    Tích chập là phép toán cơ bản trong xử lý ảnh:
    - Làm mờ (blur)
    - Phát hiện biên (edge detection)
    - Làm sắc nét (sharpening)

    Công thức:
    G(x,y) = Σ Σ K(i,j) × I(x+i, y+j)
Chị pChị Em  
    Trong đó:
    - G: ảnh output
    - K: kernel (bộ lọc)
    - I: ảnh input
    """

    def __init__(self, padding_mode='reflect'):
        """
        Parameters:
        -----------
        padding_mode : str
            Cách xử lý biên: 'reflect', 'constant', 'edge'
            - 'reflect': phản chiếu pixel ở biên
            - 'constant': điền giá trị 0
            - 'edge': lặp lại pixel biên
        """
        self.padding_mode = padding_mode

    def _pad_image(self, image, pad_h, pad_w):
        """
        Thêm padding vào ảnh để xử lý biên

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh cần padding
        pad_h : int
            Số pixel padding theo chiều cao
        pad_w : int
            Số pixel padding theo chiều rộng

        Returns:
        --------
        numpy.ndarray : Ảnh đã padding
        """
        if self.padding_mode == 'constant':
            return np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)),
                         mode='constant', constant_values=0)
        elif self.padding_mode == 'edge':
            return np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)),
                         mode='edge')
        else:  # reflect
            return np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)),
                         mode='reflect')

    def convolve_fast(self, image, kernel):
        """
        Tích chập nhanh sử dụng vectorization

        Tối ưu hóa bằng cách:
        1. Tạo ma trận các vùng cục bộ (im2col)
        2. Nhân ma trận thay vì loop

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh grayscale
        kernel : numpy.ndarray
            Kernel

        Returns:
        --------
        numpy.ndarray : Ảnh sau tích chập
        """
        image = image.astype(np.float64)
        kernel = kernel.astype(np.float64)

        img_h, img_w = image.shape
        ker_h, ker_w = kernel.shape

        pad_h = ker_h // 2
        pad_w = ker_w // 2

        padded = self._pad_image(image, pad_h, pad_w)

        # Sử dụng stride tricks để tạo view của các vùng cục bộ
        # Đây là kỹ thuật im2col tối ưu
        shape = (img_h, img_w, ker_h, ker_w)
        strides = padded.strides * 2

        # Tạo view 4D của các patches
        patches = np.lib.stride_tricks.as_strided(
            padded, shape=shape, strides=strides
        )

        # Tích chập = tổng của element-wise multiplication
        kernel_flipped = np.flip(kernel)
        output = np.einsum('ijkl,kl->ij', patches, kernel_flipped)

        return output

    def separable_convolve(self, image, kernel_x, kernel_y):
        """
        Tích chập tách được (separable convolution)

        Nhiều kernel có thể tách thành tích của 2 vector 1D:
        K = kernel_y @ kernel_x.T

        Ưu điểm: O(n*k) thay vì O(n*k²)

        Parameters:
        -----------
        image : numpy.ndarray
            Ảnh grayscale
        kernel_x : numpy.ndarray
            Kernel theo chiều ngang (1D)
        kernel_y : numpy.ndarray
            Kernel theo chiều dọc (1D)

        Returns:
        --------
        numpy.ndarray : Ảnh sau tích chập
        """
        # Tích chập theo chiều ngang trước
        kernel_x_2d = kernel_x.reshape(1, -1)
        temp = self.convolve_fast(image, kernel_x_2d)

        # Sau đó tích chập theo chiều dọc
        kernel_y_2d = kernel_y.reshape(-1, 1)
        output = self.convolve_fast(temp, kernel_y_2d)

        return output
