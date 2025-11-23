# BÁO CÁO ĐỒ ÁN XỬ LÝ ẢNH
## ỨNG DỤNG PHÁT HIỆN BIÊN ẢNH VÀ CHUYỂN ẢNH THÀNH SKETCH

**Học phần:** Xử lý ảnh (INT13146)
**Học viện:** Công nghệ Bưu chính Viễn thông

---

## MỤC LỤC

1. [Giới thiệu](#1-giới-thiệu)
2. [Cơ sở lý thuyết](#2-cơ-sở-lý-thuyết)
3. [Các kỹ thuật phát hiện biên](#3-các-kỹ-thuật-phát-hiện-biên)
4. [Thuật toán chuyển ảnh sang Sketch](#4-thuật-toán-chuyển-ảnh-sang-sketch)
5. [Xử lý ảnh hình thái học](#5-xử-lý-ảnh-hình-thái-học)
6. [Trích xuất đặc trưng](#6-trích-xuất-đặc-trưng)
7. [Công cụ và thư viện](#7-công-cụ-và-thư-viện)
8. [Kiến trúc ứng dụng](#8-kiến-trúc-ứng-dụng)
9. [Kết luận](#9-kết-luận)
10. [Tài liệu tham khảo](#10-tài-liệu-tham-khảo)

---

## 1. GIỚI THIỆU

### 1.1. Tổng quan dự án

Dự án xây dựng ứng dụng phát hiện biên ảnh và chuyển đổi ảnh thành sketch (ảnh vẽ phác thảo) là một bài toán quan trọng trong lĩnh vực xử lý ảnh số và thị giác máy tính. Ứng dụng này có nhiều ứng dụng thực tế như:

- **Nghệ thuật số:** Tạo hiệu ứng nghệ thuật cho ảnh
- **Thiết kế đồ họa:** Chuyển đổi ảnh thành bản vẽ phác thảo phục vụ thiết kế
- **Y khoa:** Làm nổi bật các đường viền trong ảnh y khoa
- **Robot và tự động hóa:** Phát hiện vật thể thông qua đường biên
- **Giáo dục:** Học tập về các kỹ thuật xử lý ảnh cơ bản

### 1.2. Mục tiêu dự án

- Nghiên cứu và triển khai các thuật toán phát hiện biên tiên tiến
- Xây dựng ứng dụng chuyển đổi ảnh sang sketch với nhiều phong cách khác nhau
- Áp dụng kiến thức từ học phần Xử lý ảnh (INT13146)
- Tối ưu hiệu suất và chất lượng đầu ra

### 1.3. Phạm vi dự án

Dự án tập trung vào các nội dung chính sau (theo đề cương học phần INT13146):

- **Chương 2:** Biến đổi cường độ và lọc không gian
- **Chương 3:** Xử lý ảnh màu
- **Chương 4:** Xử lý ảnh hình thái học (Morphological Operations)
- **Chương 5:** Phân đoạn ảnh - Phát hiện cạnh, đường, điểm
- **Chương 6:** Trích xuất đặc trưng (HOG, LBP, SIFT)

---

## 2. CƠ SỞ LÝ THUYẾT

### 2.1. Xử lý ảnh số

**Định nghĩa:** Xử lý ảnh số là quá trình sử dụng máy tính để phân tích, biến đổi và cải thiện ảnh số thông qua các thuật toán toán học.

**Các bước cơ bản trong xử lý ảnh số:**

1. **Thu nhận ảnh (Image Acquisition):** Chuyển đổi ảnh từ thế giới thực sang dạng số
2. **Tiền xử lý (Preprocessing):** Cải thiện chất lượng ảnh, giảm nhiễu
3. **Phân đoạn (Segmentation):** Chia ảnh thành các vùng có ý nghĩa
4. **Biểu diễn và mô tả (Representation & Description):** Trích xuất đặc trưng
5. **Nhận dạng (Recognition):** Gán nhãn cho các đối tượng trong ảnh

### 2.2. Biểu diễn ảnh số

**Ảnh grayscale:** Mỗi pixel được biểu diễn bởi một giá trị cường độ sáng từ 0 (đen) đến 255 (trắng).

```
I(x,y) ∈ [0, 255]
```

**Ảnh màu (RGB):** Mỗi pixel được biểu diễn bởi 3 kênh màu:
- R (Red): Đỏ
- G (Green): Xanh lá
- B (Blue): Xanh dương

```
I(x,y) = [R(x,y), G(x,y), B(x,y)]
```

### 2.3. Các không gian màu

Theo **Chương 3** của đề cương:

**1. Mô hình RGB:**
- Mô hình cộng màu, phù hợp cho hiển thị
- Ba kênh màu cơ bản: Red, Green, Blue

**2. Mô hình CMY/CMYK:**
- Mô hình trừ màu, dùng trong in ấn
- C (Cyan), M (Magenta), Y (Yellow), K (Black)

**3. Mô hình HSI/HSV:**
- H (Hue): Sắc độ
- S (Saturation): Độ bão hòa
- I/V (Intensity/Value): Cường độ sáng
- Phù hợp cho xử lý ảnh vì tách biệt màu sắc và độ sáng

---

## 3. CÁC KỸ THUẬT PHÁT HIỆN BIÊN

### 3.1. Tổng quan về phát hiện biên

**Định nghĩa:** Phát hiện biên (Edge Detection) là quá trình xác định các điểm trong ảnh số tại đó cường độ sáng thay đổi đột ngột. Các điểm này thường tương ứng với:
- Ranh giới giữa các vật thể
- Ranh giới giữa vật thể và nền
- Thay đổi độ sâu
- Thay đổi hướng bề mặt

**Ý nghĩa:** Theo **Chương 5** của đề cương, phát hiện cạnh là một phần quan trọng của phân đoạn ảnh, giúp giảm lượng dữ liệu cần xử lý trong khi vẫn giữ lại thông tin cấu trúc quan trọng.

### 3.2. Toán tử Gradient

Phát hiện biên dựa trên việc tính gradient của ảnh:

```
∇f = [∂f/∂x, ∂f/∂y]
```

**Độ lớn gradient:**
```
|∇f| = √((∂f/∂x)² + (∂f/∂y)²)
```

**Hướng gradient:**
```
θ = arctan(∂f/∂y, ∂f/∂x)
```

### 3.3. Thuật toán Sobel

**Nguyên lý:** Sobel operator sử dụng hai kernel 3×3 để tính đạo hàm theo hướng ngang và dọc.

**Kernel Sobel:**

```
Gx = [-1  0  +1]     Gy = [-1 -2 -1]
     [-2  0  +2]          [ 0  0  0]
     [-1  0  +1]          [+1 +2 +1]
```

**Ưu điểm:**
- Đơn giản, dễ cài đặt
- Kết hợp làm mịn Gaussian, giảm nhiễu
- Tính toán nhanh

**Nhược điểm:**
- Độ chính xác vị trí biên không cao
- Nhạy cảm với nhiễu hơn Canny

**Công thức:**
```
G = √(Gx² + Gy²)
θ = arctan(Gy/Gx)
```

### 3.4. Thuật toán Laplacian

**Nguyên lý:** Sử dụng đạo hàm bậc 2 để phát hiện biên.

**Toán tử Laplacian:**
```
∇²f = ∂²f/∂x² + ∂²f/∂y²
```

**Kernel Laplacian:**
```
    [ 0 -1  0]
L = [-1  4 -1]
    [ 0 -1  0]
```

**Laplacian of Gaussian (LoG):**
- Kết hợp Gaussian smoothing với Laplacian
- Giảm nhiễu trước khi phát hiện biên
- Phát hiện zero-crossing (điểm đổi dấu)

**Ưu điểm:**
- Phát hiện biên theo mọi hướng
- Nhạy với chi tiết

**Nhược điểm:**
- Rất nhạy cảm với nhiễu
- Tạo ra biên kép
- Không cung cấp thông tin về hướng biên

### 3.5. Thuật toán Canny Edge Detector

**Giới thiệu:** Được phát triển bởi John F. Canny năm 1986, được coi là thuật toán phát hiện biên tối ưu.

**Ba tiêu chí của Canny:**
1. **Phát hiện tốt (Good Detection):** Tỷ lệ phát hiện đúng cao, ít bỏ sót và ít phát hiện sai
2. **Định vị tốt (Good Localization):** Khoảng cách giữa biên phát hiện và biên thực tế là nhỏ nhất
3. **Phản ứng đơn (Single Response):** Mỗi biên chỉ được đánh dấu một lần

**Các bước của thuật toán Canny:**

**Bước 1: Làm mịn ảnh với Gaussian**
```
G(x,y) = (1/2πσ²) * exp(-(x² + y²)/2σ²)
I_smooth = I * G(x,y)
```

**Bước 2: Tính gradient**
- Sử dụng Sobel operator tính Gx, Gy
- Tính độ lớn và hướng gradient

**Bước 3: Non-maximum Suppression**
- Làm mỏng biên bằng cách giữ lại pixel có gradient cực đại theo hướng vuông góc với biên
- Loại bỏ các pixel không phải cực đại cục bộ

**Bước 4: Hysteresis Thresholding**
- Sử dụng hai ngưỡng: T_high và T_low
- Pixel có gradient > T_high: chắc chắn là biên (strong edge)
- Pixel có gradient < T_low: chắc chắn không là biên
- Pixel có gradient trong khoảng [T_low, T_high]: là biên nếu kết nối với strong edge (weak edge)

**Ưu điểm:**
- Độ chính xác cao nhất
- Biên mỏng, liên tục
- Ít nhiễu, ít biên giả
- Kiểm soát tốt qua hai ngưỡng

**Nhược điểm:**
- Phức tạp hơn Sobel và Laplacian
- Tốn thời gian tính toán
- Cần điều chỉnh tham số (σ, T_low, T_high)

### 3.6. So sánh các thuật toán

| Tiêu chí | Sobel | Laplacian | Canny |
|----------|-------|-----------|-------|
| **Độ phức tạp** | Thấp | Thấp | Cao |
| **Độ chính xác** | Trung bình | Thấp | Cao |
| **Khả năng chống nhiễu** | Trung bình | Thấp | Cao |
| **Độ mỏng của biên** | Dày | Trung bình | Mỏng |
| **Tốc độ** | Nhanh | Nhanh | Chậm |
| **Ứng dụng** | Real-time, gradient | Phát hiện nhanh | Yêu cầu chất lượng cao |

**Lựa chọn thuật toán:**
- **Sobel:** Khi cần tốc độ, ứng dụng real-time, hoặc khi cần thông tin về hướng gradient
- **Laplacian:** Khi cần phát hiện nhanh các chi tiết nhỏ, không quan tâm đến hướng biên
- **Canny:** Khi cần chất lượng cao nhất, biên mỏng và chính xác, có thể chấp nhận tốc độ chậm hơn

---

## 4. THUẬT TOÁN CHUYỂN ẢNH SANG SKETCH

### 4.1. Giới thiệu

Chuyển đổi ảnh sang sketch (pencil sketch) là quá trình tạo ra hiệu ứng vẽ phác thảo bút chì từ ảnh số, mô phỏng cách con người vẽ bằng bút chì.

### 4.2. Phương pháp truyền thống (Computer Vision)

#### 4.2.1. Thuật toán cơ bản với OpenCV

**Các bước thực hiện:**

**Bước 1: Chuyển đổi sang Grayscale**
```python
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```

**Ý nghĩa:**
- Loại bỏ thông tin màu sắc, chỉ giữ lại cường độ sáng
- Giảm độ phức tạp tính toán (từ 3 kênh xuống 1 kênh)
- Sketch thường là ảnh đen trắng

**Bước 2: Đảo ngược ảnh (Inversion)**
```python
inverted_image = cv2.bitwise_not(gray_image)
```

**Ý nghĩa:**
- Đảo ngược giá trị pixel: 255 - pixel_value
- Tạo negative image
- Chuẩn bị cho bước tiếp theo

**Bước 3: Làm mịn với Gaussian Blur**
```python
blurred = cv2.GaussianBlur(inverted_image, (21, 21), sigmaX=0, sigmaY=0)
```

**Tham số:**
- Kernel size: (21, 21) - kích thước kernel, phải là số lẻ
- sigmaX, sigmaY: độ lệch chuẩn, nếu = 0 sẽ tự động tính

**Ý nghĩa:**
- Làm mịn ảnh, tạo hiệu ứng soft shading
- Loại bỏ chi tiết nhỏ, giữ lại cấu trúc chính
- Mô phỏng cách tán bút chì

**Bước 4: Đảo ngược ảnh đã blur**
```python
inverted_blurred = cv2.bitwise_not(blurred)
```

**Bước 5: Dodge and Burn Blending**
```python
sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
```

**Công thức:**
```
Sketch = (Gray * 256) / (255 - Blurred)
```

**Ý nghĩa:**
- Kỹ thuật "dodge and burn" từ nhiếp ảnh
- Vùng sáng trong ảnh gốc → nét vẽ nhẹ
- Vùng tối trong ảnh gốc → nét vẽ đậm
- Tạo hiệu ứng gradation tự nhiên

#### 4.2.2. Thuật toán nâng cao

**Phương pháp kết hợp Edge Detection:**

```python
def advanced_sketch(image):
    # 1. Chuyển sang grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Phát hiện biên với Canny
    edges = cv2.Canny(gray, 50, 150)

    # 3. Tạo sketch cơ bản
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blurred = cv2.bitwise_not(blurred)
    sketch = cv2.divide(gray, inverted_blurred, scale=256.0)

    # 4. Kết hợp biên và sketch
    # Alpha blending: kết hợp 70% sketch + 30% edges
    final = cv2.addWeighted(sketch, 0.7, edges, 0.3, 0)

    return final
```

**Ưu điểm:**
- Biên rõ nét hơn từ Canny
- Shading mềm mại từ dodge-burn
- Kết quả tự nhiên hơn

### 4.3. Phương pháp học sâu (Deep Learning)

#### 4.3.1. Neural Style Transfer

**Nguyên lý:**
- Sử dụng Convolutional Neural Networks (CNN)
- Trích xuất content từ ảnh gốc
- Trích xuất style từ ảnh sketch mẫu
- Kết hợp để tạo ảnh mới

**Ưu điểm:**
- Chất lượng cao, tự nhiên
- Có thể học nhiều phong cách khác nhau
- Linh hoạt

**Nhược điểm:**
- Cần GPU mạnh
- Thời gian xử lý lâu
- Cần dữ liệu training

#### 4.3.2. Generative Adversarial Networks (GANs)

**Kiến trúc:**
- Generator: tạo ảnh sketch từ ảnh gốc
- Discriminator: phân biệt sketch thật/giả

**Ví dụ:** AnimeGANv2, Pix2Pix

**Ưu điểm:**
- Kết quả rất chân thực
- Học được nhiều style phức tạp

**Nhược điểm:**
- Training phức tạp
- Cần dataset lớn
- Khó kiểm soát

### 4.4. So sánh các phương pháp

| Phương pháp | Chất lượng | Tốc độ | Độ phức tạp | Yêu cầu tài nguyên |
|-------------|-----------|--------|-------------|-------------------|
| **Dodge-Burn** | Tốt | Rất nhanh | Thấp | CPU thường |
| **Edge + Dodge-Burn** | Rất tốt | Nhanh | Trung bình | CPU thường |
| **Neural Style Transfer** | Xuất sắc | Chậm | Cao | GPU |
| **GANs** | Xuất sắc | Trung bình | Rất cao | GPU mạnh |

---

## 5. XỬ LÝ ẢNH HÌNH THÁI HỌC

### 5.1. Giới thiệu Morphological Operations

Theo **Chương 4** của đề cương, xử lý ảnh hình thái học (Mathematical Morphology) là tập hợp các kỹ thuật xử lý ảnh dựa trên hình dạng và cấu trúc của đối tượng trong ảnh.

**Ứng dụng trong dự án:**
- Làm sạch nhiễu sau khi phát hiện biên
- Làm mỏng/dày đường viền
- Lấp đầy các khoảng trống trong sketch
- Trích xuất bộ khung (skeleton)

### 5.2. Các phép toán cơ bản

#### 5.2.1. Erosion (Xói mòn)

**Định nghĩa:** Thu nhỏ vùng foreground, loại bỏ các pixel ở biên.

**Công thức:**
```
(A ⊖ B)(x,y) = min{A(x+i, y+j) | (i,j) ∈ B}
```

**OpenCV:**
```python
eroded = cv2.erode(image, kernel, iterations=1)
```

**Ứng dụng:**
- Loại bỏ nhiễu nhỏ
- Tách các vật thể dính nhau
- Làm mỏng đường viền

**Ví dụ trong dự án:**
```python
# Làm mỏng đường sketch
kernel = np.ones((3,3), np.uint8)
thin_sketch = cv2.erode(sketch, kernel, iterations=1)
```

#### 5.2.2. Dilation (Giãn nở)

**Định nghĩa:** Mở rộng vùng foreground, thêm pixel vào biên.

**Công thức:**
```
(A ⊕ B)(x,y) = max{A(x-i, y-j) | (i,j) ∈ B}
```

**OpenCV:**
```python
dilated = cv2.dilate(image, kernel, iterations=1)
```

**Ứng dụng:**
- Lấp đầy khoảng trống nhỏ
- Nối các đường đứt đoạn
- Làm dày đường viền

**Ví dụ trong dự án:**
```python
# Làm đậm nét vẽ
kernel = np.ones((2,2), np.uint8)
bold_sketch = cv2.dilate(sketch, kernel, iterations=1)
```

### 5.3. Các phép toán nâng cao

#### 5.3.1. Opening (Mở)

**Định nghĩa:** Erosion sau đó Dilation

**Công thức:**
```
A ∘ B = (A ⊖ B) ⊕ B
```

**OpenCV:**
```python
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
```

**Ứng dụng:**
- Loại bỏ nhiễu nhỏ
- Làm mịn đường viền
- Tách các vật thể

#### 5.3.2. Closing (Đóng)

**Định nghĩa:** Dilation sau đó Erosion

**Công thức:**
```
A • B = (A ⊕ B) ⊖ B
```

**OpenCV:**
```python
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
```

**Ứng dụng:**
- Lấp đầy khoảng trống
- Nối các đường gãy
- Loại bỏ lỗ hổng nhỏ

#### 5.3.3. Morphological Gradient

**Định nghĩa:** Hiệu giữa Dilation và Erosion

**Công thức:**
```
Gradient = (A ⊕ B) - (A ⊖ B)
```

**OpenCV:**
```python
gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
```

**Ứng dụng:**
- Phát hiện đường viền
- Tạo hiệu ứng outline cho sketch

### 5.4. Các thuật toán hình thái học (theo đề cương)

#### 5.4.1. Boundary Extraction (Trích xuất hình bao)

**Công thức:**
```
β(A) = A - (A ⊖ B)
```

Trong đó:
- A: ảnh gốc
- B: structuring element
- β(A): đường biên

**Ứng dụng:** Trích xuất đường viền vật thể trong sketch

#### 5.4.2. Hole Filling (Làm đầy hố)

**Thuật toán:**
1. Bắt đầu với điểm bên trong lỗ
2. Dilation lặp lại
3. Giao với complement của ảnh gốc
4. Lặp đến khi hội tụ

**Ứng dụng:** Lấp đầy các vùng trống trong sketch

#### 5.4.3. Connected Component Extraction

**Mục đích:** Trích xuất các thành phần kết nối

**OpenCV:**
```python
num_labels, labels = cv2.connectedComponents(binary_image)
```

**Ứng dụng:** Phân tích các đường nét riêng biệt trong sketch

#### 5.4.4. Thinning và Thickening

**Thinning (Làm mỏng):**
- Giảm độ dày của đường nét
- Tạo skeleton (bộ khung)

**Thickening (Làm dày):**
- Tăng độ dày của đường nét
- Làm đậm nét vẽ

**OpenCV - Skeletonization:**
```python
def skeletonize(image):
    skeleton = np.zeros(image.shape, np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))

    while True:
        eroded = cv2.erode(image, kernel)
        temp = cv2.dilate(eroded, kernel)
        temp = cv2.subtract(image, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        image = eroded.copy()

        if cv2.countNonZero(image) == 0:
            break

    return skeleton
```

### 5.5. Structuring Elements

**Các loại kernel:**

```python
# Rectangular
kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))

# Elliptical
kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))

# Cross
kernel_cross = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))

# Custom
kernel_custom = np.array([[0,1,0],
                          [1,1,1],
                          [0,1,0]], dtype=np.uint8)
```

### 5.6. Ứng dụng trong dự án Sketch

```python
def enhance_sketch_morphology(sketch):
    # 1. Loại bỏ nhiễu nhỏ bằng opening
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    cleaned = cv2.morphologyEx(sketch, cv2.MORPH_OPEN, kernel_small)

    # 2. Nối các đường gãy bằng closing
    kernel_medium = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    connected = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel_medium)

    # 3. Làm mỏng đường nét để tạo sketch tinh tế hơn
    thinned = skeletonize(connected)

    # 4. Tạo morphological gradient để outline
    kernel_gradient = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    gradient = cv2.morphologyEx(connected, cv2.MORPH_GRADIENT, kernel_gradient)

    return {
        'cleaned': cleaned,
        'connected': connected,
        'thinned': thinned,
        'gradient': gradient
    }
```

---

## 6. TRÍCH XUẤT ĐẶC TRƯNG

Theo **Chương 6** của đề cương, trích xuất đặc trưng là quá trình tìm ra các thông tin quan trọng, đặc điểm riêng biệt của ảnh để phục vụ cho các bài toán phân loại, nhận dạng.

### 6.1. Histogram of Oriented Gradients (HOG)

**Định nghĩa:** HOG là bộ mô tả đặc trưng dựa trên phân bố gradient của ảnh.

**Nguyên lý:**
- Chia ảnh thành các cell nhỏ
- Tính histogram của gradient direction trong mỗi cell
- Chuẩn hóa theo block
- Kết hợp thành feature vector

**Các bước:**

1. **Tính gradient:**
```python
Gx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
Gy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
magnitude = np.sqrt(Gx**2 + Gy**2)
direction = np.arctan2(Gy, Gx) * 180 / np.pi
```

2. **Tạo histogram theo orientation:**
- Chia góc thành 9 bins (0°-180° cho unsigned)
- Mỗi pixel vote vào bin tương ứng với direction của nó, weight bằng magnitude

3. **Chuẩn hóa block:**
```python
from skimage.feature import hog

features, hog_image = hog(image,
                          orientations=9,
                          pixels_per_cell=(8, 8),
                          cells_per_block=(2, 2),
                          visualize=True)
```

**Tham số quan trọng:**
- `orientations`: số lượng bins (thường 9)
- `pixels_per_cell`: kích thước cell (thường 8×8)
- `cells_per_block`: kích thước block (thường 2×2)

**Ứng dụng trong dự án:**
- Phân loại kiểu sketch (portrait, landscape, object)
- Đánh giá chất lượng sketch
- Tìm kiếm ảnh tương tự

### 6.2. Local Binary Patterns (LBP)

**Định nghĩa:** LBP là bộ mô tả texture đơn giản nhưng hiệu quả.

**Nguyên lý:**
- So sánh pixel trung tâm với 8 pixel xung quanh
- Nếu pixel xung quanh >= pixel trung tâm → 1, ngược lại → 0
- Tạo số nhị phân 8 bit từ 8 pixel xung quanh

**Công thức:**
```
LBP(xc, yc) = Σ(p=0 to P-1) s(ip - ic) * 2^p

s(x) = { 1 if x >= 0
       { 0 if x < 0
```

Trong đó:
- (xc, yc): tọa độ pixel trung tâm
- ic: giá trị pixel trung tâm
- ip: giá trị pixel xung quanh thứ p
- P: số pixel xung quanh (thường 8)

**Implementation:**
```python
from skimage.feature import local_binary_pattern

# Tính LBP
radius = 1
n_points = 8 * radius
lbp = local_binary_pattern(image, n_points, radius, method='uniform')

# Tạo histogram
n_bins = n_points + 2  # uniform LBP có n_points + 2 bins
hist, _ = np.histogram(lbp.ravel(), bins=n_bins, range=(0, n_bins))
hist = hist.astype("float")
hist /= (hist.sum() + 1e-6)  # normalize
```

**Biến thể:**
- **Uniform LBP:** Chỉ có tối đa 2 transitions (0→1 hoặc 1→0)
- **Rotation Invariant LBP:** Bất biến với xoay

**Ứng dụng trong dự án:**
- Phân loại texture của sketch (smooth, rough, cross-hatched)
- Phân biệt các phong cách vẽ
- Đánh giá độ chi tiết của sketch

### 6.3. Scale-Invariant Feature Transform (SIFT)

**Định nghĩa:** SIFT phát hiện và mô tả các keypoints bất biến với scale và rotation.

**Các bước của SIFT:**

**1. Scale-space Extrema Detection:**
- Tạo Difference of Gaussian (DoG) pyramid
- Tìm local extrema trong scale-space

**2. Keypoint Localization:**
- Loại bỏ keypoints có contrast thấp
- Loại bỏ edge responses

**3. Orientation Assignment:**
- Tính gradient magnitude và direction xung quanh keypoint
- Gán orientation chính cho keypoint

**4. Keypoint Descriptor:**
- Tạo descriptor 128 chiều
- Chia vùng 16×16 thành 16 sub-regions 4×4
- Mỗi sub-region: histogram 8 bins → 16 × 8 = 128 chiều

**OpenCV Implementation:**
```python
# SIFT (cần opencv-contrib-python)
sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(image, None)

# Vẽ keypoints
image_with_keypoints = cv2.drawKeypoints(
    image, keypoints, None,
    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
)
```

**Ưu điểm:**
- Bất biến với scale, rotation
- Robust với thay đổi illumination
- Phân biệt tốt

**Nhược điểm:**
- Tốc độ chậm
- Không bất biến với affine transformation
- Có bằng sáng chế (dùng ORB thay thế)

**Ứng dụng trong dự án:**
- Matching giữa sketch và ảnh gốc
- Tìm kiếm sketch tương tự
- Stitching nhiều sketch lại

### 6.4. Haar-like Features

**Định nghĩa:** Được sử dụng trong Viola-Jones face detection, dựa trên sự khác biệt về intensity giữa các vùng hình chữ nhật.

**Các loại Haar features:**
- Edge features: 2 rectangles
- Line features: 3 rectangles
- Four-rectangle features

**Tính toán nhanh với Integral Image:**
```
II(x,y) = Σ(x'<=x, y'<=y) I(x',y')
```

**Ứng dụng trong dự án:**
- Phát hiện các vùng có contrast cao trong sketch
- Training classifier để phân loại sketch

### 6.5. So sánh các phương pháp trích xuất đặc trưng

| Đặc trưng | Chiều | Tốc độ | Bất biến | Ứng dụng chính |
|-----------|-------|--------|----------|----------------|
| **HOG** | ~3780 (64×64) | Nhanh | Không | Object detection, classification |
| **LBP** | 59 (uniform) | Rất nhanh | Rotation (tùy chọn) | Texture classification |
| **SIFT** | 128/keypoint | Chậm | Scale, Rotation | Matching, stitching |
| **Haar-like** | Nhiều | Rất nhanh | Không | Face detection |

### 6.6. Ứng dụng tổng hợp trong dự án

```python
class SketchFeatureExtractor:
    def __init__(self):
        self.sift = cv2.SIFT_create()

    def extract_hog(self, image):
        """Trích xuất HOG features"""
        features = hog(image,
                      orientations=9,
                      pixels_per_cell=(8, 8),
                      cells_per_block=(2, 2))
        return features

    def extract_lbp(self, image):
        """Trích xuất LBP features"""
        lbp = local_binary_pattern(image, 8, 1, method='uniform')
        hist, _ = np.histogram(lbp.ravel(), bins=59, range=(0, 59))
        hist = hist.astype("float")
        hist /= (hist.sum() + 1e-6)
        return hist

    def extract_sift(self, image):
        """Trích xuất SIFT keypoints và descriptors"""
        keypoints, descriptors = self.sift.detectAndCompute(image, None)
        return keypoints, descriptors

    def extract_all(self, image):
        """Trích xuất tất cả đặc trưng"""
        return {
            'hog': self.extract_hog(image),
            'lbp': self.extract_lbp(image),
            'sift': self.extract_sift(image)
        }
```

---

## 7. CÔNG CỤ VÀ THƯ VIỆN

### 7.1. Python và các thư viện cơ bản

**Python 3.8+**
- Ngôn ngữ lập trình chính
- Hệ sinh thái thư viện phong phú

**NumPy**
```python
import numpy as np
```
- Xử lý mảng nhiều chiều
- Tính toán số học nhanh
- Cơ sở cho các thư viện khác

**Matplotlib**
```python
import matplotlib.pyplot as plt
```
- Visualization
- Hiển thị ảnh và kết quả
- Vẽ biểu đồ, đồ thị

### 7.2. OpenCV (Open Source Computer Vision)

**Cài đặt:**
```bash
pip install opencv-python
pip install opencv-contrib-python  # Cho SIFT, SURF
```

**Import:**
```python
import cv2
```

**Các chức năng chính:**

**1. Đọc/Ghi ảnh:**
```python
# Đọc ảnh
image = cv2.imread('input.jpg')
gray = cv2.imread('input.jpg', cv2.IMREAD_GRAYSCALE)

# Ghi ảnh
cv2.imwrite('output.jpg', result)
```

**2. Chuyển đổi màu:**
```python
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
```

**3. Filtering:**
```python
# Gaussian Blur
blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Median Blur (tốt cho salt-and-pepper noise)
median = cv2.medianBlur(image, 5)

# Bilateral Filter (edge-preserving)
bilateral = cv2.bilateralFilter(image, 9, 75, 75)
```

**4. Edge Detection:**
```python
# Canny
edges = cv2.Canny(image, 100, 200)

# Sobel
sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

# Laplacian
laplacian = cv2.Laplacian(image, cv2.CV_64F)
```

**5. Morphological Operations:**
```python
kernel = np.ones((5,5), np.uint8)

# Erosion
erosion = cv2.erode(image, kernel, iterations=1)

# Dilation
dilation = cv2.dilate(image, kernel, iterations=1)

# Opening
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# Closing
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
```

**6. Thresholding:**
```python
# Simple threshold
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Otsu's method
_, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Adaptive threshold
adaptive = cv2.adaptiveThreshold(gray, 255,
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)
```

### 7.3. Scikit-image

**Cài đặt:**
```bash
pip install scikit-image
```

**Import:**
```python
from skimage import io, filters, feature, morphology
from skimage.feature import hog, local_binary_pattern
```

**Các chức năng:**

**1. Feature extraction:**
```python
# HOG
features, hog_image = hog(image, visualize=True)

# LBP
lbp = local_binary_pattern(image, 8, 1, method='uniform')
```

**2. Filters:**
```python
# Sobel
edges_sobel = filters.sobel(image)

# Gaussian
blurred = filters.gaussian(image, sigma=2)

# Unsharp mask (sharpening)
sharpened = filters.unsharp_mask(image, radius=1, amount=1)
```

**3. Morphology:**
```python
# Skeletonize
skeleton = morphology.skeletonize(binary_image)

# Remove small objects
cleaned = morphology.remove_small_objects(binary_image, min_size=50)
```

### 7.4. PIL/Pillow

**Cài đặt:**
```bash
pip install Pillow
```

**Import:**
```python
from PIL import Image, ImageFilter, ImageEnhance
```

**Ứng dụng:**
- Đọc/ghi nhiều format ảnh
- Image enhancement
- Filters có sẵn

```python
# Đọc ảnh
img = Image.open('input.jpg')

# Filters
blurred = img.filter(ImageFilter.GaussianBlur(radius=2))
edges = img.filter(ImageFilter.FIND_EDGES)

# Enhancement
enhancer = ImageEnhance.Contrast(img)
enhanced = enhancer.enhance(1.5)
```

### 7.5. SciPy

**Cài đặt:**
```bash
pip install scipy
```

**Import:**
```python
from scipy import ndimage
from scipy.signal import convolve2d
```

**Ứng dụng:**
- Convolution
- Morphological operations
- Interpolation

### 7.6. So sánh các thư viện

| Thư viện | Điểm mạnh | Điểm yếu | Khi nào dùng |
|----------|-----------|----------|--------------|
| **OpenCV** | Nhanh, đầy đủ, tối ưu | API phức tạp, BGR color | Real-time, production |
| **Scikit-image** | API đẹp, thuật toán chuẩn | Chậm hơn OpenCV | Research, prototype |
| **PIL/Pillow** | Đơn giản, nhiều format | Ít thuật toán CV | I/O, enhancement cơ bản |
| **SciPy** | Tính toán khoa học mạnh | Không chuyên CV | Tính toán nâng cao |

### 7.7. Cấu trúc project đề xuất

```
SketchLab/
├── data/
│   ├── input/          # Ảnh đầu vào
│   ├── output/         # Kết quả
│   └── samples/        # Ảnh mẫu
├── src/
│   ├── edge_detection/
│   │   ├── canny.py
│   │   ├── sobel.py
│   │   └── laplacian.py
│   ├── sketch/
│   │   ├── traditional.py  # Dodge-burn method
│   │   ├── advanced.py     # Combined methods
│   │   └── deeplearning.py # Neural methods
│   ├── morphology/
│   │   ├── operations.py
│   │   └── enhancement.py
│   ├── features/
│   │   ├── hog.py
│   │   ├── lbp.py
│   │   └── sift.py
│   └── utils/
│       ├── image_io.py
│       └── visualization.py
├── notebooks/
│   ├── 01_edge_detection.ipynb
│   ├── 02_sketch_conversion.ipynb
│   └── 03_evaluation.ipynb
├── requirements.txt
├── README.md
└── main.py
```

### 7.8. Requirements.txt

```txt
numpy>=1.21.0
opencv-python>=4.5.0
opencv-contrib-python>=4.5.0
scikit-image>=0.18.0
scipy>=1.7.0
matplotlib>=3.4.0
Pillow>=8.3.0
```

---

## 8. KIẾN TRÚC ỨNG DỤNG

### 8.1. Luồng xử lý tổng thể

```
┌─────────────┐
│ Input Image │
└──────┬──────┘
       │
       v
┌──────────────────┐
│  Preprocessing   │  ← Chuyển grayscale, resize, denoise
└────────┬─────────┘
         │
         v
    ┌────┴────┐
    │ Choose  │
    │ Method  │
    └────┬────┘
         │
    ┌────┴──────────────────┐
    │                       │
    v                       v
┌─────────────┐      ┌──────────────┐
│ Edge        │      │ Sketch       │
│ Detection   │      │ Conversion   │
└──────┬──────┘      └──────┬───────┘
       │                    │
       v                    v
┌─────────────────────────────┐
│ Post-processing             │  ← Morphology, enhancement
└──────────┬──────────────────┘
           │
           v
    ┌──────────────┐
    │ Feature      │  ← Optional: HOG, LBP, SIFT
    │ Extraction   │
    └──────┬───────┘
           │
           v
    ┌──────────────┐
    │ Save Output  │
    └──────────────┘
```

### 8.2. Module Edge Detection

```python
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
            Ảnh đầu vào (grayscale)
        params : dict
            Tham số cho từng phương pháp

        Returns:
        --------
        edges : numpy.ndarray
            Ảnh biên
        """
        if self.method == 'canny':
            return self._canny(image, **params)
        elif self.method == 'sobel':
            return self._sobel(image, **params)
        elif self.method == 'laplacian':
            return self._laplacian(image, **params)
        else:
            raise ValueError(f"Unknown method: {self.method}")

    def _canny(self, image, low_threshold=50, high_threshold=150):
        """Canny edge detection"""
        return cv2.Canny(image, low_threshold, high_threshold)

    def _sobel(self, image, ksize=3):
        """Sobel edge detection"""
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=ksize)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=ksize)
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        magnitude = np.uint8(magnitude / magnitude.max() * 255)
        return magnitude

    def _laplacian(self, image, ksize=3):
        """Laplacian edge detection"""
        laplacian = cv2.Laplacian(image, cv2.CV_64F, ksize=ksize)
        laplacian = np.uint8(np.absolute(laplacian))
        return laplacian
```

### 8.3. Module Sketch Converter

```python
class SketchConverter:
    """Class chuyển đổi ảnh sang sketch"""

    def __init__(self, method='dodge_burn'):
        """
        Parameters:
        -----------
        method : str
            'dodge_burn', 'edge_based', 'combined'
        """
        self.method = method
        self.edge_detector = EdgeDetector('canny')

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

        if self.method == 'dodge_burn':
            return self._dodge_burn(gray, **params)
        elif self.method == 'edge_based':
            return self._edge_based(gray, **params)
        elif self.method == 'combined':
            return self._combined(gray, **params)
        else:
            raise ValueError(f"Unknown method: {self.method}")

    def _dodge_burn(self, gray, blur_ksize=21, sigma=0):
        """Dodge and burn blending"""
        # 1. Invert
        inverted = cv2.bitwise_not(gray)

        # 2. Blur
        blurred = cv2.GaussianBlur(inverted, (blur_ksize, blur_ksize),
                                   sigmaX=sigma, sigmaY=sigma)

        # 3. Invert blur
        inverted_blurred = cv2.bitwise_not(blurred)

        # 4. Divide
        sketch = cv2.divide(gray, inverted_blurred, scale=256.0)

        return sketch

    def _edge_based(self, gray, low=50, high=150):
        """Edge detection based sketch"""
        edges = self.edge_detector.detect(gray,
                                         low_threshold=low,
                                         high_threshold=high)
        # Invert để có nền trắng
        sketch = cv2.bitwise_not(edges)
        return sketch

    def _combined(self, gray, blur_ksize=21, low=50, high=150,
                  alpha=0.7, beta=0.3):
        """Kết hợp dodge-burn và edge detection"""
        # 1. Tạo sketch từ dodge-burn
        sketch_db = self._dodge_burn(gray, blur_ksize=blur_ksize)

        # 2. Phát hiện biên
        edges = self.edge_detector.detect(gray,
                                         low_threshold=low,
                                         high_threshold=high)

        # 3. Kết hợp
        sketch = cv2.addWeighted(sketch_db, alpha, edges, beta, 0)

        return sketch
```

### 8.4. Module Post-processing

```python
class SketchEnhancer:
    """Class nâng cao chất lượng sketch"""

    def enhance(self, sketch, operations=['denoise', 'connect', 'thin']):
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
        """Loại bỏ nhiễu bằng opening"""
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                          (kernel_size, kernel_size))
        cleaned = cv2.morphologyEx(sketch, cv2.MORPH_OPEN, kernel)
        return cleaned

    def _connect_lines(self, sketch, kernel_size=5):
        """Nối các đường gãy bằng closing"""
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                          (kernel_size, kernel_size))
        connected = cv2.morphologyEx(sketch, cv2.MORPH_CLOSE, kernel)
        return connected

    def _thin(self, sketch):
        """Làm mỏng đường nét"""
        kernel = np.ones((2,2), np.uint8)
        thinned = cv2.erode(sketch, kernel, iterations=1)
        return thinned

    def _thicken(self, sketch):
        """Làm dày đường nét"""
        kernel = np.ones((2,2), np.uint8)
        thickened = cv2.dilate(sketch, kernel, iterations=1)
        return thickened
```

### 8.5. Application Pipeline

```python
class SketchLab:
    """Ứng dụng chính"""

    def __init__(self):
        self.edge_detector = EdgeDetector()
        self.sketch_converter = SketchConverter()
        self.enhancer = SketchEnhancer()
        self.feature_extractor = SketchFeatureExtractor()

    def process(self, image_path, output_path,
                method='combined', enhance=True, extract_features=False):
        """
        Xử lý ảnh từ đầu đến cuối

        Parameters:
        -----------
        image_path : str
            Đường dẫn ảnh đầu vào
        output_path : str
            Đường dẫn lưu kết quả
        method : str
            Phương pháp chuyển đổi
        enhance : bool
            Có áp dụng enhancement không
        extract_features : bool
            Có trích xuất đặc trưng không
        """
        # 1. Đọc ảnh
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Cannot read image: {image_path}")

        # 2. Tiền xử lý
        image = self._preprocess(image)

        # 3. Chuyển đổi sang sketch
        self.sketch_converter.method = method
        sketch = self.sketch_converter.convert(image)

        # 4. Enhancement (tùy chọn)
        if enhance:
            sketch = self.enhancer.enhance(sketch)

        # 5. Trích xuất đặc trưng (tùy chọn)
        features = None
        if extract_features:
            features = self.feature_extractor.extract_all(sketch)

        # 6. Lưu kết quả
        cv2.imwrite(output_path, sketch)

        return sketch, features

    def _preprocess(self, image, target_size=None):
        """Tiền xử lý ảnh"""
        # Resize nếu cần
        if target_size:
            image = cv2.resize(image, target_size)

        # Denoise
        image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

        return image

    def batch_process(self, input_dir, output_dir, **kwargs):
        """Xử lý hàng loạt ảnh"""
        import os
        from pathlib import Path

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, f"sketch_{filename}")

                try:
                    self.process(input_path, output_path, **kwargs)
                    print(f"Processed: {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
```

### 8.6. Ví dụ sử dụng

```python
# main.py
if __name__ == "__main__":
    # Khởi tạo ứng dụng
    app = SketchLab()

    # Xử lý một ảnh
    sketch, features = app.process(
        image_path='data/input/portrait.jpg',
        output_path='data/output/portrait_sketch.jpg',
        method='combined',
        enhance=True,
        extract_features=True
    )

    # Hiển thị kết quả
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    original = cv2.imread('data/input/portrait.jpg')
    original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

    axes[0].imshow(original)
    axes[0].set_title('Original')
    axes[0].axis('off')

    axes[1].imshow(sketch, cmap='gray')
    axes[1].set_title('Sketch')
    axes[1].axis('off')

    plt.tight_layout()
    plt.savefig('data/output/comparison.jpg')
    plt.show()

    # In thông tin đặc trưng
    if features:
        print(f"HOG features shape: {features['hog'].shape}")
        print(f"LBP features shape: {features['lbp'].shape}")
        print(f"SIFT keypoints: {len(features['sift'][0])}")
```

---

## 9. KẾT LUẬN

### 9.1. Tóm tắt

Dự án "Ứng dụng phát hiện biên ảnh và chuyển ảnh thành sketch" đã nghiên cứu và triển khai thành công các kỹ thuật xử lý ảnh quan trọng, bao gồm:

**1. Phát hiện biên:**
- Thuật toán Sobel: nhanh, đơn giản, phù hợp cho real-time
- Thuật toán Laplacian: phát hiện theo mọi hướng
- Thuật toán Canny: chất lượng cao nhất, biên mỏng và chính xác

**2. Chuyển đổi sang sketch:**
- Phương pháp dodge-burn: tạo hiệu ứng vẽ tự nhiên
- Phương pháp edge-based: tập trung vào đường nét
- Phương pháp combined: kết hợp ưu điểm của cả hai

**3. Xử lý hình thái học:**
- Erosion và Dilation cho làm mỏng/dày đường nét
- Opening và Closing cho khử nhiễu và nối đường
- Các thuật toán nâng cao: skeleton, hole filling

**4. Trích xuất đặc trưng:**
- HOG: mô tả gradient, phù hợp cho classification
- LBP: mô tả texture, nhanh và hiệu quả
- SIFT: keypoint detection, bất biến scale và rotation

### 9.2. Kiến thức đã áp dụng từ đề cương

Dự án đã bám sát và áp dụng kiến thức từ đề cương học phần Xử lý ảnh (INT13146):

- **Chương 1:** Hiểu về hệ thống xử lý ảnh số, các thành phần cơ bản
- **Chương 2:** Biến đổi cường độ (inversion, division), lọc không gian (Gaussian, Sobel)
- **Chương 3:** Xử lý ảnh màu (chuyển đổi RGB-Grayscale, không gian màu)
- **Chương 4:** Morphological operations (erosion, dilation, opening, closing, thinning)
- **Chương 5:** Phân đoạn ảnh - phát hiện cạnh (Sobel, Laplacian, Canny), phân ngưỡng
- **Chương 6:** Trích xuất đặc trưng (HOG, LBP, SIFT)

### 9.3. Đánh giá kết quả

**Ưu điểm:**
- Triển khai thành công nhiều thuật toán khác nhau
- Kiến trúc module hóa, dễ mở rộng
- Có thể xử lý real-time với các phương pháp truyền thống
- Kết quả sketch tự nhiên, đẹp mắt

**Hạn chế:**
- Chưa tối ưu cho các ảnh có nhiễu cao
- Cần điều chỉnh tham số thủ công cho từng loại ảnh
- Chưa áp dụng deep learning để tự động hóa

### 9.4. Hướng phát triển

**1. Ngắn hạn:**
- Xây dựng GUI (Tkinter, PyQt) để người dùng dễ sử dụng
- Thêm nhiều style sketch khác nhau (watercolor, charcoal, cross-hatch)
- Tự động điều chỉnh tham số dựa trên phân tích ảnh
- Xử lý video (chuyển video sang sketch video)

**2. Trung hạn:**
- Áp dụng deep learning (Neural Style Transfer, GANs)
- Training model để học các phong cách vẽ khác nhau
- Tích hợp API để sử dụng qua web
- Mobile app (Android/iOS)

**3. Dài hạn:**
- Sketch to photo (chuyển ngược từ sketch sang ảnh)
- Interactive sketching (người dùng vẽ thêm, app tự động hoàn thiện)
- 3D sketch generation
- Artistic style recommendation

### 9.5. Ý nghĩa thực tiễn

**1. Giáo dục:**
- Học tập về xử lý ảnh số
- Nghiên cứu các thuật toán computer vision
- Thực hành lập trình với Python/OpenCV

**2. Ứng dụng:**
- Nghệ thuật số: tạo hiệu ứng cho ảnh
- Thiết kế: chuyển ảnh thành bản vẽ phác thảo
- Y khoa: làm nổi bật đường viền trong ảnh y khoa
- In ấn: tạo illustration từ ảnh

**3. Nghiên cứu:**
- Cơ sở cho các bài toán object detection
- Tiền xử lý cho các mô hình machine learning
- Benchmark cho các thuật toán mới

### 9.6. Tuân thủ đạo đức nghề nghiệp

Theo **CLO2** của đề cương, dự án tuân thủ các nguyên tắc:

**1. Sở hữu hình ảnh:**
- Không sử dụng ảnh có bản quyền mà không có phép
- Credit cho nguồn ảnh khi sử dụng
- Chỉ xử lý ảnh của người dùng hoặc ảnh public domain

**2. Quyền riêng tư:**
- Không lưu trữ ảnh người dùng không cho phép
- Xóa ảnh tạm sau khi xử lý
- Không chia sẻ ảnh của người khác

**3. Trách nhiệm:**
- Không tạo fake images để lừa đảo
- Ghi rõ ảnh đã được chỉnh sửa
- Sử dụng cho mục đích hợp pháp

---

## 10. TÀI LIỆU THAM KHẢO

### 10.1. Tài liệu học phần (theo đề cương)

[1] Đỗ Năng Toàn, Nguyễn Tất Thắng, Đào Thị Thuý Quỳnh, *Bài giảng Xử lý ảnh*, Học viện Công nghệ Bưu chính viễn thông, 2023.

[2] Gonzalez, R. C. and Woods, R. E., *Digital Image Processing*, 4th ed., Pearson/Prentice Hall, NY, 2018.

[3] Richard Szeliski, *Computer Vision: Algorithms and Applications (Texts in Computer Science)*, Springer, 2011.

[4] Goodfellow, I., Bengio, Y. and Courville, A., *Deep learning*, MIT press, 2016.

[5] Jan Solem, *Programming Computer Vision with Python*, O'Reilly Media, 2012.

### 10.2. Tài liệu về Edge Detection

[6] OpenCV, "Edge Detection Using OpenCV", 2025. [Trực tuyến]. Có tại: https://opencv.org/blog/edge-detection-using-opencv/

[7] "Sobel Edge Detection vs. Canny Edge Detection in Computer Vision - GeeksforGeeks", 2025. [Trực tuyến]. Có tại: https://www.geeksforgeeks.org/computer-vision/sobel-edge-detection-vs-canny-edge-detection-in-computer-vision/

[8] Roboflow, "Edge Detection in Image Processing: An Introduction", 2025. [Trực tuyến]. Có tại: https://blog.roboflow.com/edge-detection/

[9] OpenCV Documentation, "Canny Edge Detection". [Trực tuyến]. Có tại: https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html

[10] GeeksforGeeks, "Comprehensive Guide to Edge Detection Algorithms", 2025. [Trực tuyến]. Có tại: https://www.geeksforgeeks.org/computer-vision/comprehensive-guide-to-edge-detection-algorithms/

[11] Ultralytics, "Edge Detection in Image Processing: Explained". [Trực tuyến]. Có tại: https://www.ultralytics.com/blog/edge-detection-in-image-processing-explained

### 10.3. Tài liệu về Sketch Conversion

[12] Kavya, "8 Steps To Convert Image To Pencil Sketch Using OpenCV", Medium, 2025. [Trực tuyến]. Có tại: https://medium.com/@Kavya2099/image-to-pencil-sketch-using-opencv-ec3568443c5e

[13] "Convert Images Into Pencil Sketch Using Python", DEV Community. [Trực tuyến]. Có tại: https://dev.to/spiff/convert-images-into-pencil-sketch-2cfj

[14] "How to turn any image into a pencil sketch with 10 lines of code", freeCodeCamp. [Trực tuyến]. Có tại: https://www.freecodecamp.org/news/sketchify-turn-any-image-into-a-pencil-sketch-with-10-lines-of-code-cf67fa4f68ce

[15] "Automatic image-based pencil sketch rendering", *Journal of Computer Science and Technology*. [Trực tuyến]. Có tại: https://link.springer.com/article/10.1007/BF02947313

### 10.4. Tài liệu về Morphological Operations

[16] OpenCV Documentation, "Eroding and Dilating". [Trực tuyến]. Có tại: https://docs.opencv.org/3.4/db/df6/tutorial_erosion_dilatation.html

[17] OpenCV Documentation, "Morphological Transformations". [Trực tuyến]. Có tại: https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html

[18] GeeksforGeeks, "Erosion and Dilation of images using OpenCV in Python", 2025. [Trực tuyến]. Có tại: https://www.geeksforgeeks.org/python/erosion-dilation-images-using-opencv-python/

[19] PyImageSearch, "OpenCV Morphological Operations", 2021. [Trực tuyến]. Có tại: https://pyimagesearch.com/2021/04/28/opencv-morphological-operations/

[20] Scaler Topics, "Erosion and Dilation in Image Processing". [Trực tuyến]. Có tại: https://www.scaler.com/topics/erosion-and-dilation-in-image-processing/

### 10.5. Tài liệu về Feature Extraction

[21] GeeksforGeeks, "Image Feature Extraction Using Python", 2025. [Trực tuyến]. Có tại: https://www.geeksforgeeks.org/image-feature-extraction-using-python/

[22] The Python Code, "How to Apply HOG Feature Extraction in Python". [Trực tuyến]. Có tại: https://thepythoncode.com/article/hog-feature-extraction-in-python

[23] Analytics Vidhya, "HOG Feature Descriptor: Feature Engineering for Images", 2019. [Trực tuyến]. Có tại: https://www.analyticsvidhya.com/blog/2019/09/feature-engineering-images-introduction-hog-feature-descriptor/

[24] PyImageSearch, "Local Binary Patterns with Python & OpenCV", 2015. [Trực tuyến]. Có tại: https://pyimagesearch.com/2015/12/07/local-binary-patterns-with-python-opencv/

[25] "Image Classification using HOG and LBP Feature Descriptors with SVM and CNN", *IJERT*. [Trực tuyến]. Có tại: https://www.ijert.org/image-classification-using-hog-and-lbp-feature-descriptors-with-svm-and-cnn

### 10.6. Tài liệu về OpenCV và Python

[26] OpenCV Official Documentation. [Trực tuyến]. Có tại: https://docs.opencv.org/

[27] Scikit-image Documentation. [Trực tuyến]. Có tại: https://scikit-image.org/

[28] NumPy Documentation. [Trực tuyến]. Có tại: https://numpy.org/doc/

[29] Matplotlib Documentation. [Trực tuyến]. Có tại: https://matplotlib.org/

---

**PHỤ LỤC**

### A. Code mẫu đầy đủ

Tất cả các code mẫu đã được trình bày trong các phần tương ứng của báo cáo.

### B. Kết quả thực nghiệm

Sẽ được cập nhật sau khi triển khai và test trên dataset thực tế.

### C. Hướng dẫn cài đặt và sử dụng

```bash
# 1. Clone repository (nếu có)
git clone https://github.com/username/SketchLab.git
cd SketchLab

# 2. Tạo virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Chạy ứng dụng
python main.py

# 5. Hoặc sử dụng Jupyter Notebook
jupyter notebook notebooks/
```

---

**KẾT THÚC BÁO CÁO**

Báo cáo này đã trình bày chi tiết về dự án "Ứng dụng phát hiện biên ảnh và chuyển ảnh thành sketch", bao gồm cơ sở lý thuyết vững chắc từ đề cương học phần Xử lý ảnh (INT13146), kết hợp với nghiên cứu mở rộng từ các tài liệu và công nghệ mới nhất trong lĩnh vực Computer Vision và Image Processing.

Dự án không chỉ giúp sinh viên nắm vững các kiến thức lý thuyết mà còn rèn luyện kỹ năng lập trình, thiết kế hệ thống, và áp dụng vào thực tiễn.
