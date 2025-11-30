# SketchLab - Image to Sketch Converter

Ứng dụng web chuyển đổi ảnh thành sketch sử dụng các thuật toán xử lý ảnh.

## Tổng quan

SketchLab là một ứng dụng web Flask cho phép người dùng chuyển đổi ảnh thành sketch (ảnh vẽ phác thảo) bằng các thuật toán xử lý ảnh cơ bản.

Dự án được xây dựng dựa trên kiến thức từ học phần **Xử lý ảnh (INT13146)** - Học viện Công nghệ Bưu chính Viễn thông.

## Tính năng

- **Upload ảnh**: Drag & drop hoặc click để chọn file (PNG, JPG, JPEG)
- **2 phương pháp chuyển đổi**:
  - **Combined Sketch** (Recommended) - Kết hợp dodge-burn và Canny edges
  - **Dodge-Burn Sketch** - Tạo shading tự nhiên như vẽ bút chì
- **Tự động denoise**: Loại bỏ nhiễu bằng morphological opening
- **Preview**: So sánh side-by-side giữa ảnh gốc và sketch
- **Download**: Tải về ảnh đã xử lý

## Thuật toán xử lý ảnh

Dự án sử dụng các thuật toán xử lý ảnh cơ bản:

### 1. Convolution2D (`core/algorithms/convolution.py`)

Phép tích chập 2D - nền tảng của xử lý ảnh:

```
G(x,y) = ΣΣ K(i,j) × I(x+i, y+j)
```

- Sử dụng stride tricks và einsum để tối ưu
- Hỗ trợ separable convolution: O(n×k) thay vì O(n×k²)

### 2. GaussianBlur (`core/algorithms/gaussian_blur.py`)

Làm mờ Gaussian:

```
G(x,y) = (1/2πσ²) × e^(-(x²+y²)/2σ²)
```

- Tính kernel từ công thức toán học
- Sử dụng separable convolution để tối ưu

### 3. SobelOperator (`core/algorithms/sobel.py`)

Toán tử Sobel tính gradient:

```
Gx = [[-1,0,1], [-2,0,2], [-1,0,1]]
Gy = [[-1,-2,-1], [0,0,0], [1,2,1]]
```

- Tính gradient theo x, y
- Tính magnitude: M = √(Gx² + Gy²)
- Tính direction: θ = arctan2(Gy, Gx)

### 4. CannyEdgeDetector (`core/algorithms/canny.py`)

Thuật toán Canny đầy đủ 5 bước:

1. **Gaussian smoothing** - Giảm nhiễu
2. **Gradient calculation** - Tính đạo hàm bằng Sobel
3. **Non-maximum suppression** - Làm mỏng biên
4. **Double thresholding** - Phân loại strong/weak edges
5. **Hysteresis** - Nối weak edges với strong edges

### 5. MorphologicalOperations (`core/algorithms/morphology.py`)

Các phép toán hình thái học:

- **Erosion**: Thu nhỏ vùng sáng - `output = MIN(region)`
- **Dilation**: Mở rộng vùng sáng - `output = MAX(region)`
- **Opening**: Erosion → Dilation (loại bỏ nhiễu)

## Công nghệ

- **Backend**: Python 3.8+, Flask 3.0
- **Image Processing**: OpenCV (một phần), NumPy
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Local (localhost:5000)

## Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd SketchLab
```

### 2. Tạo virtual environment

```bash
python3 -m venv venv
```

### 3. Activate virtual environment

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
python app.py
```

Ứng dụng sẽ chạy tại: **http://127.0.0.1:5000**

## Hướng dẫn sử dụng

1. Mở trình duyệt và truy cập: `http://127.0.0.1:5000`
2. Upload ảnh bằng cách kéo thả hoặc click chọn file
3. Chọn thuật toán (khuyến nghị: **Combined Sketch**)
4. Click "Xử lý ảnh"
5. Xem kết quả so sánh và tải về

## Cấu trúc dự án

```
SketchLab/
├── app.py                          # Flask application
├── config.py                       # Cấu hình
├── requirements.txt                # Dependencies
├── README.md
│
├── core/                           # Image processing modules
│   ├── __init__.py
│   ├── edge_detector.py            # EdgeDetector class
│   ├── sketch_converter.py         # SketchConverter class
│   ├── sketch_enhancer.py          # SketchEnhancer class
│   ├── utils.py                    # Helper functions
│   │
│   └── algorithms/                 # Thuật toán xử lý ảnh
│       ├── __init__.py
│       ├── convolution.py          # Convolution2D
│       ├── gaussian_blur.py        # GaussianBlur
│       ├── sobel.py                # SobelOperator
│       ├── canny.py                # CannyEdgeDetector
│       └── morphology.py           # MorphologicalOperations
│
├── docs/                           # Tài liệu báo cáo
│   ├── BAO_CAO_SLIDE.md            # Báo cáo slide
│   ├── generate_images.py          # Script tạo hình minh họa
│   └── images/                     # Hình ảnh minh họa
│
├── templates/                      # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   └── about.html
│
└── static/
    ├── css/style.css
    ├── js/
    │   ├── main.js
    │   └── upload.js
    └── uploads/                    # Temporary files
        ├── original/
        └── processed/
```

## Chi tiết thuật toán

### Dodge-Burn Sketch

```python
# Các bước:
1. CLAHE preprocessing
2. Invert: inverted = 255 - image
3. Gaussian Blur: blurred = GaussianBlur(inverted)
4. Invert blur: inv_blur = 255 - blurred
5. Divide: sketch = (image × 256) / inv_blur
6. Post-processing: GaussianBlur nhẹ
```

### Combined Sketch

```python
# Kết hợp dodge-burn và edge detection:
1. sketch_db = DodgeBurn(image)
2. edges = CannyEdgeDetector(image)
3. result = 0.9 × sketch_db + 0.1 × edges
4. Post-processing với gamma correction
```

### Canny Edge Detection

```python
# 5 bước của thuật toán Canny:
1. blurred = GaussianBlur(image)           # Giảm nhiễu
2. gx, gy = SobelOperator(blurred)         # Tính gradient
3. nms = NonMaxSuppression(magnitude, direction)  # Làm mỏng biên
4. edges = DoubleThreshold(nms)            # Phân loại biên
5. result = Hysteresis(edges)              # Nối biên
```

## API Endpoints

| Method | Endpoint               | Mô tả                       |
| ------ | ---------------------- | --------------------------- |
| GET    | `/`                    | Trang upload                |
| POST   | `/upload`              | Upload file                 |
| POST   | `/process`             | Xử lý ảnh                   |
| GET    | `/download/<filename>` | Download kết quả            |
| GET    | `/result`              | Trang kết quả               |
| GET    | `/about`               | Trang giới thiệu            |
| GET    | `/api/algorithms`      | Danh sách thuật toán (JSON) |

## Cấu hình

File `config.py`:

```python
UPLOAD_FOLDER = 'static/uploads/original'
PROCESSED_FOLDER = 'static/uploads/processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

## Troubleshooting

### Lỗi: "ModuleNotFoundError: No module named 'cv2'"

```bash
pip install opencv-python
```

### Lỗi: "File too large"

Kiểm tra kích thước file (max 16MB) hoặc tăng `MAX_CONTENT_LENGTH` trong config.

### Ảnh xử lý chậm

Ảnh lớn sẽ tự động resize xuống max 1024px để tăng tốc xử lý.

## Tài liệu tham khảo

- Gonzalez & Woods - Digital Image Processing (4th ed.)
- Canny, J. - A Computational Approach to Edge Detection (1986)
- [OpenCV Documentation](https://docs.opencv.org/)
- Đề cương học phần Xử lý ảnh - INT13146

## License

Educational project for learning purposes.
