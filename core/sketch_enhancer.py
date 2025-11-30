"""
Sketch Enhancement Module
Implements denoise operation to enhance sketch quality
Sử dụng morphological operations tự implement
"""

import numpy as np
from .algorithms import MorphologicalOperations


class SketchEnhancer:
    """
    Class nâng cao chất lượng sketch bằng morphological denoising
    """

    def __init__(self):
        """Khởi tạo với morphological operations engine"""
        self.morph = MorphologicalOperations()

    def enhance(self, sketch, operations=["denoise"]):
        """
        Nâng cao chất lượng sketch bằng denoise

        Parameters:
        -----------
        sketch : numpy.ndarray
            Ảnh sketch đầu vào
        operations : list
            Danh sách các phép toán: chỉ hỗ trợ 'denoise'

        Returns:
        --------
        enhanced : numpy.ndarray
            Ảnh sketch đã được nâng cao
        """
        result = sketch.copy()

        for op in operations:
            if op == "denoise":
                result = self._denoise(result)

        return result

    def _denoise(self, sketch, kernel_size=3):
        """
        Loại bỏ nhiễu bằng morphological opening - TỰ IMPLEMENT

        Opening = Erosion + Dilation
        Loại bỏ các điểm nhiễu nhỏ trong khi giữ nguyên cấu trúc chính

        Thuật toán:
        1. Erosion: co vùng sáng, loại bỏ điểm nhỏ
        2. Dilation: giãn lại để khôi phục kích thước ban đầu
        """
        kernel = self.morph.create_kernel("ellipse", kernel_size)

        # Áp dụng opening (erosion + dilation) - TỰ IMPLEMENT
        cleaned = self.morph.opening(sketch, kernel)

        return cleaned
