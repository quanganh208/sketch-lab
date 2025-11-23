"""
Sketch Enhancement Module
Implements morphological operations to enhance sketch quality
Based on SketchLab Report - Chapter 5
"""

import cv2
import numpy as np


class SketchEnhancer:
    """Class nâng cao chất lượng sketch bằng morphological operations"""

    def enhance(self, sketch, operations=['denoise', 'connect']):
        """
        Nâng cao chất lượng sketch

        Parameters:
        -----------
        sketch : numpy.ndarray
            Ảnh sketch đầu vào
        operations : list
            Danh sách các phép toán: 'denoise', 'connect', 'thin', 'thicken'

        Returns:
        --------
        enhanced : numpy.ndarray
            Ảnh sketch đã được nâng cao
        """
        result = sketch.copy()

        for op in operations:
            if op == 'denoise':
                result = self._denoise(result)
            elif op == 'connect':
                result = self._connect_lines(result)
            elif op == 'thin':
                result = self._thin(result)
            elif op == 'thicken':
                result = self._thicken(result)

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

    def _connect_lines(self, sketch, kernel_size=5):
        """
        Nối các đường gãy bằng morphological closing

        Closing = Dilation + Erosion
        Lấp đầy các khoảng trống nhỏ và nối các đường đứt gãy
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                          (kernel_size, kernel_size))
        connected = cv2.morphologyEx(sketch, cv2.MORPH_CLOSE, kernel)

        return connected

    def _thin(self, sketch, iterations=1):
        """
        Làm mỏng đường nét bằng erosion

        Giảm độ dày của đường vẽ, tạo nét mảnh hơn
        Phù hợp cho artistic sketch style
        """
        kernel = np.ones((2, 2), np.uint8)
        thinned = cv2.erode(sketch, kernel, iterations=iterations)

        return thinned

    def _thicken(self, sketch, iterations=1):
        """
        Làm dày đường nét bằng dilation

        Tăng độ dày của đường vẽ, tạo nét đậm hơn
        Phù hợp cho bold sketch style
        """
        kernel = np.ones((2, 2), np.uint8)
        thickened = cv2.dilate(sketch, kernel, iterations=iterations)

        return thickened

    def skeletonize(self, image):
        """
        Tạo skeleton (bộ khung) của ảnh

        Làm mỏng dần ảnh cho đến khi chỉ còn lại đường trung tâm
        Tạo hiệu ứng line art tinh tế
        """
        skeleton = np.zeros(image.shape, np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

        while True:
            eroded = cv2.erode(image, kernel)
            temp = cv2.dilate(eroded, kernel)
            temp = cv2.subtract(image, temp)
            skeleton = cv2.bitwise_or(skeleton, temp)
            image = eroded.copy()

            if cv2.countNonZero(image) == 0:
                break

        return skeleton
