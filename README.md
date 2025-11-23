# SketchLab - Image to Sketch Converter

Ứng dụng web chuyển đổi ảnh thành sketch sử dụng Computer Vision và Image Processing.

## 📋 Tổng quan

SketchLab là một ứng dụng web Flask cho phép người dùng chuyển đổi ảnh thành sketch (ảnh vẽ phác thảo) với 6 thuật toán khác nhau. Dự án được xây dựng dựa trên kiến thức từ học phần **Xử lý ảnh (INT13146)** - Học viện Công nghệ Bưu chính Viễn thông.

## ✨ Tính năng

- **Upload ảnh**: Drag & drop hoặc click để chọn file
- **6 thuật toán xử lý**:
  - Combined Sketch (Recommended) - Kết hợp dodge-burn và edges
  - Dodge-Burn Sketch - Shading tự nhiên
  - Edge-Based Sketch - Tập trung đường nét
  - Canny Edge Detection - Phát hiện biên chất lượng cao
  - Sobel Edge Detection - Nhanh và đơn giản
  - Laplacian Edge Detection - Phát hiện theo mọi hướng
- **Enhancement options**:
  - Denoise - Loại bỏ nhiễu
  - Connect Lines - Nối đường gãy
  - Thin Lines - Làm mỏng nét
  - Thicken Lines - Làm đậm nét
- **Preview**: So sánh side-by-side giữa ảnh gốc và sketch
- **Download**: Tải về ảnh đã xử lý

## 🛠️ Công nghệ

- **Backend**: Python 3.8+, Flask
- **Image Processing**: OpenCV, NumPy, Pillow
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Local (localhost:5000)

## 📦 Cài đặt

### 1. Clone repository (hoặc download source code)

```bash
cd /Volumes/QUANGANH1TB/Coding/SketchLab
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

## 🚀 Chạy ứng dụng

### Development mode

```bash
python app.py
```

Hoặc sử dụng Flask CLI:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Ứng dụng sẽ chạy tại: **http://127.0.0.1:5000**

## 📖 Hướng dẫn sử dụng

1. Mở trình duyệt và truy cập: `http://127.0.0.1:5000`
2. Upload ảnh:
   - Kéo thả ảnh vào vùng "Drop Zone"
   - Hoặc click "Chọn File"
3. Chọn thuật toán xử lý (khuyến nghị: **Combined Sketch**)
4. Chọn enhancement options nếu cần (khuyến nghị check **Denoise**)
5. Click nút "Xử lý ảnh"
6. Xem kết quả so sánh side-by-side
7. Click "Tải về" để download ảnh sketch

## 🗂️ Cấu trúc dự án

```
SketchLab/
├── app.py                      # Flask application chính
├── config.py                   # Cấu hình
├── requirements.txt            # Dependencies
├── README.md                   # File này
├── BaoCao_*.md                 # Báo cáo chi tiết
│
├── core/                       # Image processing modules
│   ├── __init__.py
│   ├── edge_detector.py       # EdgeDetector class
│   ├── sketch_converter.py    # SketchConverter class
│   ├── sketch_enhancer.py     # SketchEnhancer class
│   └── utils.py               # Helper functions
│
├── templates/                  # HTML templates
│   ├── base.html              # Base layout
│   ├── index.html             # Upload page
│   ├── result.html            # Result display
│   └── about.html             # About page
│
└── static/                     # Static files
    ├── css/
    │   └── style.css          # Main stylesheet
    ├── js/
    │   ├── main.js            # Main logic
    │   └── upload.js          # Upload handler
    └── uploads/               # Temporary files
        ├── original/          # Uploaded images
        └── processed/         # Processed sketches
```

## 🔬 Thuật toán

### Edge Detection

**Canny Edge Detector:**
- 4 bước: Gaussian smoothing → Gradient → Non-max suppression → Hysteresis thresholding
- Biên mỏng, chính xác nhất
- Tốt cho: Yêu cầu chất lượng cao

**Sobel Edge Detector:**
- Tính gradient bằng Sobel operator (3×3 kernels)
- Nhanh, đơn giản
- Tốt cho: Real-time, xử lý nhanh

**Laplacian Edge Detector:**
- Sử dụng đạo hàm bậc 2
- Phát hiện theo mọi hướng
- Tốt cho: Phát hiện chi tiết nhỏ

### Sketch Conversion

**Dodge-Burn Sketch:**
```python
# Công thức
Sketch = (Gray * 256) / (255 - GaussianBlur(Inverted))
```
- Tạo shading mềm mại tự nhiên
- Giống hiệu ứng vẽ bút chì

**Edge-Based Sketch:**
- Sử dụng Canny edge detection
- Tập trung vào đường nét rõ ràng

**Combined Sketch:**
```python
Result = 0.7 * DodgeBurn + 0.3 * Edges
```
- Cân bằng giữa shading và clarity
- **Recommended** cho hầu hết ảnh

### Morphological Enhancement

- **Denoise (Opening)**: Erosion → Dilation, loại bỏ nhiễu
- **Connect Lines (Closing)**: Dilation → Erosion, nối đường gãy
- **Thin Lines (Erosion)**: Thu nhỏ đường nét
- **Thicken Lines (Dilation)**: Mở rộng đường nét

## 📊 API Endpoints

- `GET /` - Upload page
- `POST /upload` - Upload file
- `POST /process` - Process image
- `GET /download/<filename>` - Download result
- `GET /result` - Result page
- `GET /about` - About page
- `GET /api/algorithms` - List algorithms (JSON)

## ⚙️ Cấu hình

File `config.py`:

```python
UPLOAD_FOLDER = 'static/uploads/original'
PROCESSED_FOLDER = 'static/uploads/processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

## 🧪 Testing

Để test ứng dụng:

1. Chạy ứng dụng: `python app.py`
2. Mở browser: `http://127.0.0.1:5000`
3. Test các chức năng:
   - Upload ảnh (PNG, JPG)
   - Test tất cả 6 algorithms
   - Test enhancement options
   - Download kết quả

## 🐛 Troubleshooting

### Lỗi: "ModuleNotFoundError: No module named 'cv2'"
```bash
pip install opencv-python
```

### Lỗi: "File too large"
- Kiểm tra kích thước file (max 16MB)
- Hoặc tăng `MAX_CONTENT_LENGTH` trong `config.py`

### Lỗi: "Permission denied" khi save file
```bash
chmod -R 755 static/uploads
```

### Ảnh xử lý quá chậm
- Resize ảnh trước khi upload (ứng dụng tự động resize xuống max 1024px)
- Chọn algorithm nhanh hơn (Sobel thay vì Canny)

## 📚 Tài liệu tham khảo

- [Báo cáo chi tiết](BaoCao_PhatHienBien_ChuyenAnhThanhSketch.md)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- Gonzalez & Woods - Digital Image Processing (4th ed.)
- Đề cương học phần Xử lý ảnh - INT13146

## 👨‍💻 Tác giả

Dự án học phần **Xử lý ảnh (INT13146)**
Học viện Công nghệ Bưu chính Viễn thông
Năm 2025

## 📄 License

Educational project for learning purposes.

## 🙏 Credits

- OpenCV - Computer Vision library
- Flask - Web framework
- NumPy - Numerical computing
- Các thuật toán dựa trên tài liệu học phần và nghiên cứu

---

**Enjoy sketching! 🎨**
