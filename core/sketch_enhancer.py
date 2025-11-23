"""
Sketch Enhancement Module
Implements denoise operation to enhance sketch quality
"""

import cv2
import numpy as np


class SketchEnhancer:
    """Class nâng cao chất lượng sketch bằng morphological denoising"""

    def enhance(self, sketch, operations=['denoise']):
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
            if op == 'denoise':
                result = self._denoise(result)

        return result

    def _denoise(self, sketch, kernel_size=3):
        """
        Loại bỏ nhiễu bằng morphological opening

        Opening = Erosion + Dilation
        Loại bỏ các điểm nhiễu nhỏ trong khi giữ nguyên cấu trúc chính
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                          (kernel_size, kernel_size))
        cleaned = cv2.morphologyEx(sketch, cv2.MORPH_OPEN, kernel)

        return cleaned
