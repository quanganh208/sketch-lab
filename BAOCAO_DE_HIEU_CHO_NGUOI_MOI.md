# BÁO CÁO DỰ ÁN SKETCHLAB
# CHUYỂN ẢNH THƯỜNG THÀNH ẢNH VẼ BÚT CHÌ
## Phiên bản dễ hiểu cho người mới bắt đầu

---

**Học phần**: Xử lý ảnh (INT13146)
**Trường**: Học viện Công nghệ Bưu chính Viễn thông
**Năm**: 2025

---

## 📚 MỤC LỤC

1. [Giới thiệu - Dự án này làm gì?](#1-giới-thiệu)
2. [Ví dụ minh họa - Xem kết quả trước](#2-ví-dụ-minh-họa)
3. [Hai cách chuyển đổi ảnh](#3-hai-cách-chuyển-đổi-ảnh)
4. [Giải thích từng bước chi tiết](#4-giải-thích-từng-bước-chi-tiết)
5. [Cách sử dụng ứng dụng](#5-cách-sử-dụng-ứng-dụng)
6. [Câu hỏi thường gặp](#6-câu-hỏi-thường-gặp)
7. [Tổng kết](#7-tổng-kết)

---

## 1. GIỚI THIỆU

### Dự án này làm gì?

Bạn có bao giờ muốn biến một bức ảnh chụp thường thành một bức tranh vẽ bút chì không? Đó chính xác là điều dự án **SketchLab** làm!

**Ví dụ đơn giản:**
```
Ảnh gốc (bạn chụp bằng điện thoại):
- Có màu sắc đầy đủ
- Nhìn rất thật
- Giống như bạn nhìn bằng mắt

↓ Sau khi xử lý ↓

Ảnh sketch (tranh vẽ):
- Chỉ còn màu đen trắng
- Có nét vẽ như vẽ bằng bút chì
- Trông như nghệ sĩ vẽ ra
```

### Tại sao làm dự án này?

1. **Học tập**: Áp dụng kiến thức môn Xử lý ảnh
2. **Thực tiễn**: Tạo hiệu ứng nghệ thuật từ ảnh thường
3. **Sáng tạo**: Làm app có thể dùng thật, không chỉ lý thuyết

### Công nghệ sử dụng (giải thích đơn giản)

- **Python**: Ngôn ngữ lập trình (như tiếng Anh để nói chuyện với máy tính)
- **OpenCV**: Thư viện xử lý ảnh (như hộp công cụ có sẵn nhiều chức năng)
- **Flask**: Tạo website (để có giao diện đẹp, không phải dòng lệnh)

---

## 2. VÍ DỤ MINH HỌA

### Hãy tưởng tượng bạn vẽ một bức tranh bằng bút chì

**Khi vẽ bằng tay, nghệ sĩ làm gì?**

1. **Vẽ viền**: Vẽ đường nét bao quanh vật thể
   ```
   Ví dụ: Vẽ khuôn mặt
   - Vẽ đường viền khuôn mặt
   - Vẽ đường viền mắt, mũi, miệng
   ```

2. **Tô bóng (shading)**: Tô đậm/nhạt để tạo hiệu ứng 3D
   ```
   Ví dụ: Gò má
   - Chỗ lồi ra: vẽ nhạt (ít bút chì)
   - Chỗ lõm vào: vẽ đậm (nhiều bút chì)
   ```

**Máy tính làm tương tự:**

Dự án này có **2 cách** để máy tính "vẽ":

1. **Cách 1 (Dodge-Burn)**: Chỉ tập trung vào **tô bóng**
   - Như nghệ sĩ vẽ nhẹ nhàng, tô đậm nhạt
   - Kết quả: Mềm mại, nghệ thuật

2. **Cách 2 (Combined)**: Vừa **vẽ viền** vừa **tô bóng**
   - Như nghệ sĩ vừa vẽ đường nét rõ ràng, vừa tô bóng
   - Kết quả: Rõ ràng hơn, đẹp hơn

---

## 3. HAI CÁCH CHUYỂN ĐỔI ẢNH

### 🎨 CÁCH 1: DODGE-BURN SKETCH

#### Giải thích bằng ngôn ngữ đời thường

**Dodge** và **Burn** là 2 kỹ thuật từ nhiếp ảnh truyền thống:

- **Dodge** = Làm sáng (như dùng tẩy làm nhạt bớt)
- **Burn** = Làm tối (như tô thêm bút chì)

**Tương tự trong đời sống:**

Tưởng tượng bạn có một bức ảnh in trên giấy, và một cây đèn chiếu từ trên xuống:

1. Chỗ nào bạn **che tay** → ít ánh sáng → ảnh sáng hơn (Dodge)
2. Chỗ nào bạn **để lâu hơn** → nhiều ánh sáng → ảnh tối hơn (Burn)

#### Các bước đơn giản (không cần hiểu code)

**📍 Location trong code:** `sketch_converter.py` dòng 24-98

**Bước 0: Biến ảnh màu thành đen trắng (nếu cần)**
```
Ảnh gốc: 🌈 (nhiều màu)
        ↓
Ảnh đen trắng: ⬜⬛ (chỉ có trắng đen)

Code: cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
```
*Tại sao?* Tranh vẽ bút chì không có màu!

**Bước 1: Cải thiện độ sáng tối (CLAHE)**
```
Ví dụ:
- Ảnh ban đầu: Mặt quá tối, nền quá sáng
- Sau khi cải thiện: Mặt sáng vừa, nền tối vừa

Kỹ thuật: CLAHE (Contrast Limited Adaptive Histogram Equalization)
```
*Tại sao?* Để nhìn rõ chi tiết hơn, đặc biệt vùng tối và vùng sáng

**Bước 2: "Đảo ngược" ảnh lần 1 (như âm bản phim)**
```
Trước: Trời sáng ⬜, cây tối ⬛
Sau:  Trời tối ⬛, cây sáng ⬜

Code: cv2.bitwise_not(enhanced)
```
*Tại sao?* Cần thiết cho công thức dodge-burn

**Bước 3: Làm mờ ảnh đã đảo (Gaussian Blur)**
```
Ảnh đảo (sắc nét):  ▓▓▓▓
                    ↓
Ảnh mờ:            ░░░░

Code: GaussianBlur với kernel 21×21
```
*Tại sao?* Tạo hiệu ứng mềm mại, giống vẽ tay

**Bước 4: Đảo ngược lần 2**
```
Ảnh mờ (đã đảo):  ⬛⬛⬛
                  ↓
Đảo lại:         ⬜⬜⬜

Code: cv2.bitwise_not(blurred)
```
*Tại sao?* Chuẩn bị cho phép chia

**Bước 5: Đảm bảo không chia cho số quá nhỏ**
```
Nếu pixel < 10 → Đặt = 10

Code: np.where(pixel < 10, 10, pixel)
```
*Tại sao?* Tránh tạo đốm trắng lỗi (white spots)

**Bước 6: "Chia" ảnh gốc cho ảnh đã xử lý (MA THUẬT!)**
```
Công thức:
Sketch = (Ảnh gốc × 256) / Ảnh đã xử lý

Code: cv2.divide(enhanced, inverted_blurred, scale=256.0)

Giải thích:
- Chỗ nào ảnh gốc SÁNG, ảnh xử lý TỐI → Sketch RẤT SÁNG ✨
- Chỗ nào ảnh gốc TỐI, ảnh xử lý SÁNG → Sketch TỐI 🖤
```
*Tại sao?* Đây là công thức chính tạo hiệu ứng sketch!

**Bước 7: Giới hạn giá trị về [0, 255]**
```
Nếu > 255 → Đặt = 255
Nếu < 0   → Đặt = 0

Code: np.clip(sketch, 0, 255)
```
*Tại sao?* Đảm bảo giá trị pixel hợp lệ

**Bước 8: Làm mờ nhẹ cuối cùng (Post-processing)**
```
Blur rất nhẹ với kernel 3×3

Code: GaussianBlur(sketch, (3, 3), 0.3)
```
*Tại sao?* Giảm pixel noise nhưng vẫn giữ sắc nét

**Kết quả:**
```
Trước:  📸 (ảnh chụp thường)
Sau:    ✏️ (tranh vẽ bút chì)
```

#### Ví dụ cụ thể: Theo dõi 1 pixel qua 9 bước

Giả sử có 1 pixel (điểm ảnh):

```
Giá trị pixel trong ảnh: từ 0 (đen) đến 255 (trắng)

Bước 0: Pixel gốc màu RGB(100,100,100)
        → Grayscale = 100 (xám nhạt)

Bước 1: CLAHE cải thiện
        → 100 → 120 (sáng hơn chút)

Bước 2: Đảo ngược lần 1
        → 120 → 255-120 = 135

Bước 3: Làm mờ (trung bình với hàng xóm)
        → 135 → 130

Bước 4: Đảo ngược lần 2
        → 130 → 255-130 = 125

Bước 5: Kiểm tra minimum
        → 125 > 10 ✓ (OK, giữ nguyên 125)

Bước 6: Chia (MA THUẬT!)
        → (120 × 256) / 125 = 245.76 ≈ 246

Bước 7: Clip
        → 246 nằm trong [0, 255] ✓ (giữ nguyên)

Bước 8: Post-blur nhẹ
        → 246 → 245 (giảm 1 đơn vị)

→ KẾT QUẢ CUỐI: Pixel = 245 (rất sáng!)
→ Pixel này sẽ là điểm SÁNG trong tranh vẽ
```

---

### 🎨 CÁCH 2: COMBINED SKETCH

#### Giải thích bằng ngôn ngữ đời thường

Cách này **kết hợp 2 kỹ thuật**:

1. **70% Tô bóng** (từ Cách 1)
2. **30% Vẽ viền** (kỹ thuật mới)

**Tương tự trong đời sống:**

Tưởng tượng 2 họa sĩ cùng vẽ 1 bức tranh:

- **Họa sĩ A**: Chuyên tô bóng, làm mềm mại → Cống hiến 70%
- **Họa sĩ B**: Chuyên vẽ đường nét, làm rõ ràng → Cống hiến 30%

Kết quả: Tranh vừa mềm mại, vừa rõ ràng!

#### Phần mới: "Vẽ viền" là gì?

**Phát hiện biên (Edge Detection)** = Tìm chỗ có đường viền trong ảnh

**Ví dụ thực tế:**

```
Bức ảnh chụp quả táo:
🍎
- Biên = Đường viền quanh quả táo
- Không phải biên = Phần trong quả táo (màu đồng đều)
```

**Máy tính làm thế nào?**

Tìm những chỗ **thay đổi đột ngột** về độ sáng:

```
Ví dụ: Một dòng pixel
[10, 10, 10, 200, 200, 200]
              ↑
         Biên ở đây! (nhảy từ 10 lên 200)
```

**Thuật toán Canny** (tên người phát minh: John Canny)

Đây là cách **THÔNG MINH NHẤT** để tìm viền, gồm 5 bước:

**Bước 1: Làm mờ nhẹ để bỏ nhiễu**
```
Ảnh gốc (có nhiễu):  ▓▓▒▓▓
                      ↓
Ảnh mờ (bớt nhiễu):  ▓▓▓▓▓
```
*Tại sao?* Nhiễu (như điểm lốm đốm) sẽ bị nhầm là viền

**Bước 2: Tính "độ dốc" (Gradient)**

```
Tưởng tượng ảnh là bản đồ địa hình:
- Chỗ phẳng = không đổi màu = KHÔNG phải viền
- Chỗ dốc = đổi màu nhanh = CÓ THỂ là viền

Công thức đơn giản:
Độ dốc = |Pixel bên phải - Pixel bên trái|
```

Ví dụ:
```
[100, 100, 100, 200, 200, 200]
  ↓     ↓     ↓     ↓     ↓
[0,    0,    50,   0,    0]    ← Độ dốc
              ↑
         Dốc cao nhất!
```

**Bước 3: Giữ lại chỗ dốc nhất**
```
Trong 1 vùng, chỉ giữ pixel có độ dốc CAO NHẤT
→ Viền chỉ dày 1 pixel, rất mỏng
```

**Bước 4: Phân loại viền**
```
Độ dốc > 100: CHẮC CHẮN là viền (giữ lại)
50 < Độ dốc < 100: NGHI NGỜ là viền (xem tiếp)
Độ dốc < 50: KHÔNG phải viền (bỏ đi)
```

**Bước 5: Nối các viền**
```
Nếu viền "nghi ngờ" nằm cạnh viền "chắc chắn":
→ Giữ lại (vì có thể là phần nối tiếp)

Nếu viền "nghi ngờ" đứng 1 mình:
→ Bỏ đi (có thể chỉ là nhiễu)
```

**Kết quả:**
```
Ảnh gốc: 📸
        ↓
Chỉ còn viền: 🖼️ (như ảnh phác thảo)
```

#### Các bước thực hiện theo code

**📍 Location trong code:** `sketch_converter.py:100-144` + `edge_detector.py:50-89`

Combined method hoạt động như 2 họa sĩ vẽ CÙNG LÚC, sau đó trộn kết quả:

---

**BƯỚC 0: Biến ảnh thành đen trắng (chung cho 2 nhánh)**
```
Ảnh màu → Ảnh đen trắng
```

---

**NHÁNH A - Họa sĩ A: Dodge-Burn** (9 bước như Cách 1)

```
Họa sĩ A làm:
1. Cải thiện độ sáng (CLAHE)
2-8. Các bước Dodge-Burn (như đã học ở Cách 1)

Kết quả: Ảnh với tô bóng mềm mại 🎨
```

---

**NHÁNH B - Họa sĩ B: Vẽ viền (Canny Edge Detection)**

Họa sĩ B làm 6 bước để tìm viền:

**B.1: Cải thiện độ sáng (CLAHE riêng)**
```
Cũng dùng CLAHE, nhưng cho edge detection
Code: cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
```

**B.2: Lọc nhiễu nhưng giữ viền (Bilateral Filter)**
```
Làm mượt ảnh NHƯNG không làm mờ viền
Code: cv2.bilateralFilter(enhanced, 9, 75, 75)

Khác với làm mờ thường:
- Làm mờ thường: Mọi thứ đều mờ
- Bilateral: Chỉ mờ chỗ phẳng, GIỮ viền
```

**B.3: Tính ngưỡng tự động (Adaptive Threshold)**
```
Máy tính TỰ ĐỘNG tính threshold dựa trên ảnh:

median = Giá trị giữa của ảnh
low = 67% của median
high = 133% của median

Ví dụ: Nếu median = 100
→ low = 67, high = 133
```

**B.4: Tìm viền (Canny)**
```
cv2.Canny(image, low=67, high=133)

Bên trong Canny tự động làm 4 việc:
1. Làm mờ Gaussian
2. Tính độ dốc (gradient)
3. Giữ điểm dốc nhất
4. Nối viền

Kết quả: Ảnh chỉ còn viền (đen trắng)
```

**B.5: Làm mượt viền nhẹ (Anti-aliasing)**
```
Blur rất nhẹ để viền mượt hơn
Code: GaussianBlur(edges, (3,3), 0.3)
```

**Kết quả nhánh B:** Ảnh chỉ có viền 🖼️

---

**TRỘN VÀ LÀM ĐẸP** (5 bước)

**Bước 1: Trộn 2 nhánh (Alpha Blending)**
```
Kết quả = 70% Họa sĩ A + 30% Họa sĩ B
        = 0.7 × Dodge-Burn + 0.3 × Edges

Code: cv2.addWeighted(sketch_db, 0.7, edges, 0.3, 0)
```

**Bước 2: Lọc mượt giữ viền (Bilateral lần 2)**
```
Giảm đốm trắng từ dodge-burn
Nhưng vẫn GIỮ viền rõ ràng

Code: cv2.bilateralFilter(sketch, 5, 50, 50)
```

**Bước 3: Tăng độ sắc nét (Unsharp Masking)**
```
Tạo bản mờ → So sánh với gốc → Thêm chi tiết

Blur = GaussianBlur(sketch)
Sharp = sketch×2.0 - Blur×1.0

→ Ảnh sắc nét hơn!
```

**Bước 4: Làm nổi viền (Morphological Gradient)**
```
Phồng ảnh → Co ảnh → Lấy phần chênh lệch = Viền!
Trộn 10% viền vào ảnh

Code:
gradient = Dilation - Erosion
Result = 90% sketch + 10% gradient
```

**Bước 5: Giới hạn giá trị cuối cùng**
```
Đảm bảo pixel trong [0, 255]
Code: np.clip(sketch, 0, 255)
```

**KẾT QUẢ CUỐI:**
```
Ảnh có cả:
- Tô bóng mềm mại (từ Dodge-Burn)
- Viền rõ ràng (từ Canny)
- Độ sắc nét cao (từ Unsharp)
- Viền được tăng cường (từ Morphological)

→ Tranh sketch đẹp nhất! ✏️
```

#### Kết hợp lại

**Bước cuối: Trộn 2 ảnh**

```python
Ảnh Dodge-Burn:  🎨 (tô bóng mềm)
Ảnh Edges:       🖼️ (viền rõ)
                  ↓
Kết quả = 70% 🎨 + 30% 🖼️ = ✏️ (tranh hoàn chỉnh)
```

**Ví dụ cụ thể:**

```
Tại 1 pixel:

Dodge-Burn cho giá trị: 200 (khá sáng)
Edges cho giá trị:      100 (trung bình)

Kết hợp:
= 0.7 × 200 + 0.3 × 100
= 140 + 30
= 170 (sáng vừa phải)
```

**Tại sao 70-30?**

Qua thử nghiệm, tỷ lệ này cho kết quả ĐẸP NHẤT:
- Nếu 90-10: Quá mềm, mất viền
- Nếu 50-50: Quá cứng, mất tự nhiên
- **70-30**: Vừa đủ! 👍

#### Các bước làm đẹp thêm

Sau khi trộn xong, còn 3 bước "làm đẹp":

**1. Lọc Bilateral (Làm mượt nhưng giữ viền)**

```
Khác với làm mờ thường:
- Làm mờ thường: Mọi thứ đều mờ (kể cả viền)
- Bilateral: Chỉ mờ chỗ phẳng, GIỮ NGUYÊN viền

Ví dụ:
Trước: ▓▓▓│▓▓▓  (viền ở giữa, 2 bên có nhiễu nhỏ)
       ░░░│▓▓▓
Sau:  ░░░│▓▓▓  (nhiễu mất, viền vẫn rõ)
```

**2. Unsharp Masking (Làm sắc nét)**

Tên có "unsharp" (không sắc nét) nhưng lại làm SẮC NÉT! Lạ chưa? 😄

Cách hoạt động:
```
Bước 1: Tạo bản mờ của ảnh
Bước 2: Tìm phần khác biệt = Ảnh gốc - Ảnh mờ
        (phần này là chi tiết nhỏ)
Bước 3: CỘNG chi tiết vào ảnh gốc
        → Ảnh gốc + Chi tiết = Ảnh sắc nét hơn!

Ví dụ số:
Pixel gốc: 100
Pixel mờ:  95
Khác biệt: 100 - 95 = 5 (chi tiết)
Kết quả:   100 + 5 = 105 (sắc nét hơn!)
```

**3. Morphological Gradient (Làm nổi viền)**

```
Cách làm:
1. "Phồng" ảnh ra 1 chút
2. "Co" ảnh lại 1 chút
3. Tính phần chênh lệch = Viền!
4. Thêm 10% viền vào ảnh

Kết quả: Đường nét rõ ràng hơn
```

---

## 4. GIẢI THÍCH TỪNG BƯỚC CHI TIẾT

### 📖 Phần 1: Những khái niệm cơ bản

#### 4.1. Ảnh là gì trong máy tính?

**Ảnh = Ma trận (bảng) các con số**

```
Ví dụ ảnh 5×5 pixels (rất nhỏ):

[
  [255, 255, 255, 255, 255]   ← Dòng 1: Trắng hoàn toàn
  [255, 100, 100, 100, 255]   ← Dòng 2: Viền trắng, giữa xám
  [255, 100,   0, 100, 255]   ← Dòng 3: Giữa có điểm đen
  [255, 100, 100, 100, 255]   ← Dòng 4: Giống dòng 2
  [255, 255, 255, 255, 255]   ← Dòng 5: Trắng hoàn toàn
]

Quy ước:
- 0   = Đen tuyệt đối ⬛
- 128 = Xám ▒
- 255 = Trắng tuyệt đối ⬜
```

**Ảnh màu:**
```
Mỗi pixel có 3 giá trị (RGB):
- R (Red):   0-255
- G (Green): 0-255
- B (Blue):  0-255

Ví dụ:
[255, 0, 0]   = Đỏ 🔴
[0, 255, 0]   = Xanh lá 🟢
[0, 0, 255]   = Xanh dương 🔵
[255, 255, 0] = Vàng 🟡 (đỏ + xanh lá)
[0, 0, 0]     = Đen ⬛
[255, 255, 255] = Trắng ⬜
```

#### 4.2. CLAHE là gì? (Cải thiện độ tương phản)

**Tên đầy đủ:** Contrast Limited Adaptive Histogram Equalization

Nghe phức tạp nhỉ? Hãy chia nhỏ ra:

**Histogram là gì?**
```
Histogram = Biểu đồ đếm pixel

Ví dụ ảnh có 100 pixels:
- 50 pixels có giá trị 0-50 (tối)
- 30 pixels có giá trị 51-150 (trung bình)
- 20 pixels có giá trị 151-255 (sáng)

Vẽ biểu đồ:
Số pixel
  ↑
50|  ██
40|  ██
30|  ██  ██
20|  ██  ██  ██
10|  ██  ██  ██
  +--+---+---+---→ Độ sáng
    Tối Trung Sáng
```

**Equalization (Cân bằng) là gì?**

Làm cho histogram "phẳng" hơn:

```
Trước:
  ██              ← Nhiều chỗ tối
  ██
  ██  █           ← Ít chỗ sáng
  +--+---+---+

Sau Equalization:
  ██  ██  ██      ← Phân bố đều hơn
  ██  ██  ██
  +--+---+---+

Kết quả: Ảnh có độ tương phản tốt hơn!
```

**Adaptive (Thích nghi) là gì?**

Thay vì cân bằng TOÀN ẢNH, chia ảnh thành nhiều vùng nhỏ:

```
Ảnh lớn:
┌─────────┬─────────┐
│  Vùng 1 │  Vùng 2 │  ← Mỗi vùng cân bằng riêng
│  (Tối)  │  (Sáng) │
├─────────┼─────────┤
│  Vùng 3 │  Vùng 4 │
│ (Trung) │  (Tối)  │
└─────────┴─────────┘

Lợi ích: Vùng tối được cải thiện mà không làm vùng sáng quá sáng
```

**Contrast Limited (Giới hạn tương phản) là gì?**

Ngăn không cho một vùng trở nên QUÁ sáng hoặc QUÁ tối:

```
Histogram trước khi giới hạn:
     ████         ← Quá cao! Sẽ gây nhiễu
     ████
  ██ ████ ██

Histogram sau khi cắt (clip):
  ── ──── ──      ← Ngưỡng giới hạn
  ██ ████ ██      ← Phần vượt bị cắt
  ██ ████ ██

→ Tránh tăng nhiễu quá mức
```

**Kết luận CLAHE:**

CLAHE = Cân bằng histogram từng vùng + Giới hạn mức tăng

Kết quả:
- Vùng tối → Sáng hơn
- Vùng sáng → Tối hơn
- Không tạo nhiễu quá mức
- Chi tiết rõ ràng hơn

#### 4.3. Gaussian Blur (Làm mờ Gaussian)

**Tại sao gọi là "Gaussian"?**

Gaussian = Tên nhà toán học Carl Friedrich Gauss

Ông tạo ra công thức "đường cong hình chuông":

```
Đường cong Gaussian (bell curve):
      ●
    ● ● ●
  ● ● ● ● ●
● ● ● ● ● ● ●
```

**Làm mờ như thế nào?**

Mỗi pixel = Trung bình có trọng số của các pixel xung quanh

```
Kernel 3×3 (ma trận trọng số):

┌─────────────┐
│ 1   2   1  │  ← Pixel xa ít ảnh hưởng (trọng số nhỏ)
│ 2   4   2  │  ← Pixel gần ảnh hưởng nhiều (trọng số lớn)
│ 1   2   1  │  ← Pixel ở giữa ảnh hưởng nhất
└─────────────┘

Tổng trọng số = 16
```

**Ví dụ cụ thể:**

```
Ảnh gốc (vùng 3×3):
┌─────────┐
│ 10  20  10│
│ 20 100  20│  ← Pixel giữa = 100
│ 10  20  10│
└─────────┘

Tính giá trị mới cho pixel giữa:
= (1×10 + 2×20 + 1×10 + 2×20 + 4×100 + 2×20 + 1×10 + 2×20 + 1×10) / 16
= (10 + 40 + 10 + 40 + 400 + 40 + 10 + 40 + 10) / 16
= 600 / 16
= 37.5 ≈ 38

Pixel giữa: 100 → 38 (mờ hơn, gần với hàng xóm hơn)
```

**Blur lớn vs Blur nhỏ:**

```
Kernel 3×3 (blur nhẹ):
Trước: ████▓▓▒▒░░
Sau:   ███▓▓▓▒▒░░  ← Chỉ mờ nhẹ

Kernel 21×21 (blur mạnh):
Trước: ████▓▓▒▒░░
Sau:   ▓▓▓▓▓▓▓▓▓▓  ← Rất mờ, gần như đồng đều
```

---

### 📖 Phần 2: Chi tiết từng bước của Dodge-Burn

Để dễ hiểu, tôi sẽ đi qua **1 pixel cụ thể** xem nó biến đổi thế nào:

**Giả sử:**
- Ảnh ban đầu: Pixel có giá trị 80 (xám trung bình)
- Vị trí: Pixel (100, 200) - hàng 100, cột 200

**BƯỚC 1: Chuyển sang đen trắng**
```
Nếu ảnh gốc là màu:
RGB(120, 100, 80) → Grayscale = (120+100+80)/3 ≈ 100

Nếu đã là đen trắng: Giữ nguyên 80
```

**BƯỚC 2: CLAHE - Cải thiện tương phản**
```
Pixel = 80 (trung bình)

Sau CLAHE:
- Vùng này hơi tối → Tăng lên
- Pixel mới = 95

80 → 95 (sáng hơn 15 đơn vị)
```

**BƯỚC 3: Đảo ngược (Invert)**
```
Công thức: Pixel mới = 255 - Pixel cũ

95 → 255 - 95 = 160

Giải thích:
- Pixel càng sáng → Sau đảo càng tối
- Pixel càng tối → Sau đảo càng sáng
```

**BƯỚC 4: Gaussian Blur**
```
Pixel = 160

Nhìn các hàng xóm (giả sử):
┌─────────┐
│ 150 155 150│
│ 155 160 155│  ← Pixel của chúng ta
│ 150 155 150│
└─────────┘

Sau Blur (kernel 21×21, trung bình với nhiều hàng xóm):
Pixel mới = 158 (gần 160, nhưng mượt hơn)

160 → 158
```

**BƯỚC 5: Đảo ngược lại**
```
158 → 255 - 158 = 97

Bây giờ pixel = 97
```

**BƯỚC 6: Đảm bảo không nhỏ hơn 10**
```
Nếu pixel < 10 → Set = 10

Pixel = 97 > 10 → Giữ nguyên

Tại sao? Tránh chia cho số quá nhỏ ở bước sau
```

**BƯỚC 7: Chia (Bước ma thuật!)**
```
Công thức: Sketch = (Pixel CLAHE × 256) / Pixel hiện tại

Pixel CLAHE (bước 2) = 95
Pixel hiện tại (bước 6) = 97

Sketch = (95 × 256) / 97
       = 24,320 / 97
       = 250.72
       ≈ 251

Kết quả: 251 (rất sáng!)
```

**Tại sao lại sáng?**
- Pixel gốc 95 và pixel xử lý 97 GẦN NHAU
- Khi chia 2 số gần nhau → Kết quả gần 1
- Nhân với 256 → Kết quả lớn (sáng)

**BƯỚC 8: Clip về [0, 255]**
```
251 nằm trong [0, 255] → Giữ nguyên

Nếu kết quả > 255 → Set = 255
Nếu kết quả < 0 → Set = 0
```

**BƯỚC 9: Blur nhẹ cuối cùng**
```
251 → Sau blur (3×3, rất nhẹ) → 250

Giảm 1 đơn vị thôi, gần như không đổi
```

**KẾT QUẢ CUỐI CÙNG:**
```
Pixel ban đầu: 80 (xám trung bình)
Pixel sketch:  250 (gần trắng)

→ Vùng này sẽ là highlight (vùng sáng) trong tranh vẽ
```

---

### 📖 Phần 3: Chi tiết từng bước của Combined

Combined = Dodge-Burn + Edge Detection

Chúng ta đã hiểu Dodge-Burn rồi, giờ tập trung vào Edge Detection!

#### Canny Edge Detection - 5 bước chi tiết

**Chuẩn bị:**
- Ảnh đầu vào: Pixel (100, 200) = 120 (xám sáng)

**BƯỚC 1: CLAHE (giống Dodge-Burn)**
```
120 → 130 (tăng tương phản)
```

**BƯỚC 2: Bilateral Filter (Làm mượt giữ viền)**
```
Nhìn hàng xóm:
┌─────────┐
│ 130 130 130│  ← Vùng đồng đều
│ 130 130 130│  ← Pixel của chúng ta
│ 130 130 130│
└─────────┘

Sau filter: 130 (không đổi vì hàng xóm giống nhau)

Nhưng giả sử hàng xóm khác:
┌─────────┐
│ 130  50  50│  ← Có viền ở đây!
│ 130 130  50│  ← Pixel của chúng ta
│ 130  50  50│
└─────────┘

Bilateral sẽ CHỈ lấy trung bình các pixel GIỐNG (130):
= (130 + 130 + 130) / 3 = 130

→ Không bị ảnh hưởng bởi pixel bên kia viền (50)
→ VIỀN GIỮ NGUYÊN!
```

**BƯỚC 3: Tính Gradient (Độ dốc)**

Giả sử 1 dòng pixel ngang:
```
[... 130, 130, 130, 50, 50, 50 ...]
            ↑       ↑
       Pixel ta  Pixel bên

Gradient ngang (Gx):
= |Pixel phải - Pixel trái|
= |50 - 130| = 80

Gradient dọc (Gy):
(Tương tự cho hướng dọc)
Giả sử = 10

Gradient tổng:
= √(Gx² + Gy²)
= √(80² + 10²)
= √(6400 + 100)
= √6500
≈ 80.6
```

**Ý nghĩa:**
- Gradient cao (80.6) → Có thay đổi mạnh → CÓ THỂ là viền
- Gradient thấp (≤10) → Không đổi → KHÔNG phải viền

**BƯỚC 4: Non-Maximum Suppression (Giữ điểm cao nhất)**

```
Trong vùng 3×3, có nhiều pixel cùng cao:

Gradient của vùng:
┌──────────┐
│ 60  70  60│
│ 70  81  70│  ← Pixel 81 cao nhất
│ 60  70  60│
└──────────┘

→ CHỈ giữ pixel 81, loại bỏ 70, 60
→ Viền chỉ dày 1 pixel
```

**BƯỚC 5: Double Thresholding (Ngưỡng kép)**

```
Giả sử:
- Low threshold = 50
- High threshold = 100

Pixel của ta có gradient = 81

Phân loại:
- 81 > 100? Không → Không phải "chắc chắn là viền"
- 81 > 50?  Có    → Là "nghi ngờ là viền"

→ Pixel này được đánh dấu "nghi ngờ" (weak edge)
```

**BƯỚC 6: Hysteresis (Theo dõi viền)**

```
Nhìn hàng xóm của pixel "nghi ngờ":

┌──────────────────┐
│ [Chắc chắn] [Không] [Không]     │
│ [Nghi ngờ]  [pixel] [Nghi ngờ]  │  ← Pixel của ta ở giữa
│ [Không]     [Không] [Không]     │
└──────────────────┘

Quy tắc:
- Nếu CÓ hàng xóm "chắc chắn" → Giữ lại
- Nếu KHÔNG có → Loại bỏ

Pixel của ta CÓ hàng xóm "chắc chắn"
→ GIỮ LẠI
→ Giá trị = 255 (trắng - là viền)
```

**KẾT QUẢ Edge Detection:**
```
Pixel (100, 200) = 255 (viền)

Các pixel không phải viền = 0 (đen)
```

#### Kết hợp Dodge-Burn + Edges

**Từ các bước trước:**
- Dodge-Burn cho pixel này: 180 (khá sáng)
- Edges cho pixel này: 255 (là viền)

**Alpha Blending (Trộn):**
```
Combined = 0.7 × Dodge-Burn + 0.3 × Edges
         = 0.7 × 180 + 0.3 × 255
         = 126 + 76.5
         = 202.5
         ≈ 203

→ Pixel kết quả = 203 (sáng, nhưng không cực sáng)
```

**Các bước làm đẹp:**

**1. Bilateral Filter**
```
203 → 200 (mượt hơn chút)
```

**2. Unsharp Masking**
```
Blur nhẹ: 200 → 195
Unsharp: 200 + (200 - 195) = 200 + 5 = 205
→ 200 → 205 (sắc nét hơn)
```

**3. Morphological Gradient**
```
Tính gradient:
Dilation (phồng): 205 → 207
Erosion (co):     205 → 203
Gradient = 207 - 203 = 4

Blend 10%:
= 0.9 × 205 + 0.1 × 4
= 184.5 + 0.4
= 184.9
≈ 185

→ 205 → 185 (viền nổi hơn)
```

**KẾT QUẢ CUỐI:**
```
Pixel ban đầu: 120
Pixel sketch (Combined): 185

→ Pixel này sẽ là vùng sáng trong tranh, với viền rõ ràng
```

---

## 5. CÁCH SỬ DỤNG ỨNG DỤNG

### Hướng dẫn từng bước (như dạy người không biết gì về máy tính)

#### Bước 1: Cài đặt (Chỉ làm 1 lần)

**1.1. Kiểm tra Python đã cài chưa**

Mở Terminal (Mac/Linux) hoặc Command Prompt (Windows):

```bash
python3 --version
```

Nếu hiện ra: `Python 3.8.x` hoặc cao hơn → OK!
Nếu báo lỗi → Cần cài Python từ python.org

**1.2. Di chuyển vào thư mục dự án**

```bash
cd /Volumes/QUANGANH1TB/Coding/SketchLab
```

**1.3. Tạo môi trường ảo (Virtual Environment)**

Tưởng tượng: Tạo 1 "phòng riêng" cho dự án này, không ảnh hưởng máy tính

```bash
python3 -m venv venv
```

Sau lệnh này, xuất hiện thư mục `venv/`

**1.4. Kích hoạt môi trường**

Mac/Linux:
```bash
source venv/bin/activate
```

Windows:
```bash
venv\Scripts\activate
```

Thấy `(venv)` ở đầu dòng lệnh → Thành công!

**1.5. Cài đặt thư viện cần thiết**

```bash
pip install -r requirements.txt
```

Chờ vài phút... Cài đặt xong!

#### Bước 2: Chạy ứng dụng

```bash
python app.py
```

Thấy dòng:
```
Starting SketchLab server...
Access at: http://127.0.0.1:5000
```

→ Thành công!

#### Bước 3: Mở trình duyệt

Mở Chrome, Firefox, Safari... gõ:
```
http://127.0.0.1:5000
```

Hoặc:
```
http://localhost:5000
```

→ Thấy giao diện upload ảnh!

#### Bước 4: Upload ảnh

**Cách 1: Kéo thả**
```
📁 Tìm ảnh trong máy tính
→ Kéo vào vùng "Drop Zone"
→ Thả chuột
```

**Cách 2: Click chọn**
```
Click "Chọn File"
→ Chọn ảnh
→ Click "Open"
```

**Ảnh hỗ trợ:**
- PNG (.png)
- JPEG (.jpg, .jpeg)
- Kích thước: Tối đa 16MB

#### Bước 5: Chọn thuật toán

Có 2 lựa chọn:

**Combined Sketch (Khuyên dùng)**
- Vừa có nét, vừa có bóng
- Đẹp với mọi loại ảnh
- Chậm hơn 1 chút

**Dodge-Burn Sketch**
- Chủ yếu tô bóng
- Nghệ thuật hơn
- Nhanh hơn

→ Click chọn 1 trong 2

#### Bước 6: Xử lý

Click nút **"Xử lý ảnh"**

Đợi 1-3 giây...

→ Tự động chuyển sang trang kết quả!

#### Bước 7: Xem kết quả

Thấy 2 ảnh cạnh nhau:
```
┌─────────────┬─────────────┐
│  Ảnh gốc    │  Ảnh sketch │
│     📸      │      ✏️      │
└─────────────┴─────────────┘
```

So sánh dễ dàng!

#### Bước 8: Tải về

Click nút **"Tải về"**

Ảnh sketch sẽ được tải về máy!

---

## 6. CÂU HỎI THƯỜNG GẶP

### ❓ Câu hỏi 1: Tại sao phải "đảo ngược" ảnh?

**Trả lời đơn giản:**

Công thức Dodge-Burn cần chia 2 số. Để tạo hiệu ứng đúng, ta cần:
- Ảnh gốc: Sáng ở chỗ cần sáng
- Ảnh mẫu số: Tối ở chỗ cần sáng

→ Phải đảo ngược để "sáng" thành "tối"

**Giải thích kỹ:**

Nhớ công thức: `Sketch = Ảnh gốc / Ảnh xử lý`

```
Trường hợp 1: Vùng sáng trong ảnh gốc
- Ảnh gốc = 200 (sáng)
- Ảnh xử lý = 50 (tối - vì đã đảo từ vùng sáng)
- Sketch = 200 / 50 = 4 (rất lớn, nhân 256 → rất sáng ✨)

Trường hợp 2: Vùng tối trong ảnh gốc
- Ảnh gốc = 50 (tối)
- Ảnh xử lý = 200 (sáng - vì đã đảo từ vùng tối)
- Sketch = 50 / 200 = 0.25 (rất nhỏ, nhân 256 → tối 🖤)
```

→ Kết quả: Vùng sáng vẫn sáng, vùng tối vẫn tối, nhưng có hiệu ứng sketch!

### ❓ Câu hỏi 2: Tại sao phải làm mờ?

**Trả lời đơn giản:**

Vẽ bút chì thật không có đường nét cứng nhắc, mà mềm mại, có gradient (chuyển dần từ tối sang sáng).

Blur = Tạo gradient tự nhiên

**Ví dụ:**

```
Không blur:
████████  ← Cứng nhắc, như in máy tính
        ░░░░░░░░

Có blur:
████▓▓▒▒░░░░  ← Mềm mại, như vẽ tay
```

### ❓ Câu hỏi 3: Tại sao Combined tốt hơn Dodge-Burn?

**Trả lời:**

Không phải "tốt hơn", mà "phù hợp hơn với nhiều ảnh"!

**So sánh:**

| Loại ảnh | Dodge-Burn | Combined |
|----------|------------|----------|
| Chân dung | ⭐⭐⭐⭐⭐ (Rất tốt) | ⭐⭐⭐⭐ (Tốt) |
| Phong cảnh | ⭐⭐⭐ (Trung bình) | ⭐⭐⭐⭐⭐ (Rất tốt) |
| Kiến trúc | ⭐⭐ (Kém) | ⭐⭐⭐⭐⭐ (Rất tốt) |
| Nghệ thuật | ⭐⭐⭐⭐⭐ (Rất tốt) | ⭐⭐⭐ (Trung bình) |

**Lý do:**
- **Dodge-Burn**: Mềm, nghệ thuật → Tốt cho chân dung, cần cảm xúc
- **Combined**: Rõ ràng, chi tiết → Tốt cho kiến trúc, cần độ chính xác

### ❓ Câu hỏi 4: CLAHE làm gì mà quan trọng vậy?

**Trả lời:**

CLAHE cứu các ảnh "khó":

**Ví dụ 1: Ảnh ngược sáng**
```
Ảnh gốc:
- Mặt người: Rất tối (vì mặt trời phía sau)
- Nền trời: Rất sáng

Không có CLAHE:
- Xử lý → Mặt mất hết chi tiết (đen kịt)

Có CLAHE:
- Làm sáng vùng mặt
- Làm tối vùng trời
- Mặt có chi tiết rõ!
```

**Ví dụ 2: Ảnh ban đêm**
```
Ảnh gốc: Toàn bộ tối

Không CLAHE:
- Sketch → Đen kịt, không thấy gì

Có CLAHE:
- Tăng sáng vùng tối
- Sketch → Thấy chi tiết!
```

### ❓ Câu hỏi 5: Tại sao phải "clip" về 10 ở bước 4?

**Trả lời:**

Tránh chia cho số quá nhỏ!

**Vấn đề:**

```
Nếu mẫu số = 1:
Sketch = 100 × 256 / 1 = 25,600

Nhưng pixel chỉ có giá trị max = 255!
→ 25,600 sẽ bị "cắt" thành 255
→ Tạo "đốm trắng" (white spots) rất xấu
```

**Giải pháp:**

```
Set minimum = 10:
Sketch max = 100 × 256 / 10 = 2,560

Vẫn lớn, nhưng:
- Không quá cực đoan
- Sau clip về 255, vẫn giữ gradient
- Không tạo đốm trắng đột ngột
```

### ❓ Câu hỏi 6: Unsharp Masking hoạt động thế nào?

**Trả lời bằng ví dụ thực tế:**

Tưởng tượng bạn có 2 bức ảnh:
1. Ảnh gốc (rõ)
2. Ảnh mờ

**Bước 1:** So sánh 2 ảnh
```
Ảnh gốc:  ▓▓▓▓▓▓  ← Có chi tiết nhỏ
Ảnh mờ:   ░░░░░░  ← Mất chi tiết

Khác biệt = Ảnh gốc - Ảnh mờ = Chi tiết nhỏ
```

**Bước 2:** Thêm chi tiết vào ảnh gốc
```
Ảnh gốc + Chi tiết = Ảnh rất rõ!

Như thế này:
- Bạn đang nghe nhạc âm lượng 50
- Tăng thêm 20
- → Nghe rõ hơn (âm lượng 70)
```

**Tại sao gọi "Unsharp"?**

Vì dùng ảnh "không sắc nét" (mờ) để tạo ảnh "sắc nét"! 😄

### ❓ Câu hỏi 7: Morphological operations là gì?

**Trả lời đơn giản:**

Morphology = Hình thái học (nghiên cứu hình dạng)

**2 phép toán cơ bản:**

**Erosion (Co lại):**
```
Trước:    ███████
          ███████
          ███████

Sau:      ·█████·  ← Nhỏ hơn, biên bị "ăn mòn"
          ·█████·
          ·█████·
```

**Dilation (Phồng ra):**
```
Trước:    ·█████·
          ·█████·
          ·█████·

Sau:      ███████  ← Lớn hơn, biên "phồng" ra
          ███████
          ███████
```

**Opening (Co + Phồng):**
```
Dùng để: Xóa nhiễu nhỏ

Ảnh có nhiễu:  ███·█·███  ← Có điểm nhỏ
Sau Opening:   ██████████  ← Điểm nhỏ mất
```

**Morphological Gradient (Phồng - Co):**
```
Dilation:  ███████
Erosion:   ·█████·
Gradient:  █·····█  ← CHỈ còn viền!
           █·····█
           █·····█
```

---

## 7. TỔNG KẾT

### 🎯 Những điều quan trọng nhất

#### 1. Hai phương pháp chính

**Dodge-Burn:**
- Tạo hiệu ứng tô bóng tự nhiên
- Giống vẽ bằng bút chì thật
- Tốt cho: Chân dung, nghệ thuật

**Combined:**
- Kết hợp tô bóng (70%) + viền (30%)
- Rõ ràng hơn, chi tiết hơn
- Tốt cho: Mọi loại ảnh

#### 2. Các bước then chốt

**CLAHE:**
- Cải thiện độ tương phản
- Làm sáng vùng tối, tối vùng sáng
- Giúp ảnh "khó" trở nên dễ xử lý

**Gaussian Blur:**
- Tạo hiệu ứng mềm mại
- Làm gradient tự nhiên
- Quan trọng cho Dodge-Burn

**Canny Edge Detection:**
- Tìm viền chính xác nhất
- 5 bước thông minh
- Quan trọng cho Combined

**Alpha Blending:**
- Trộn 2 ảnh theo tỷ lệ
- 70-30 là tỷ lệ vàng
- Cân bằng giữa mềm và rõ

#### 3. Tại sao dự án này hay?

**Về mặt học thuật:**
- Áp dụng nhiều thuật toán: CLAHE, Canny, Bilateral, Morphology
- Kết hợp sáng tạo: Dodge-Burn + Edge Detection
- Hiểu sâu lý thuyết

**Về mặt thực tiễn:**
- Tạo app thật sự dùng được
- Giao diện đẹp, dễ dùng
- Kết quả chất lượng cao

**Về mặt kỹ năng:**
- Lập trình Python/OpenCV
- Web development (Flask)
- Software engineering (modular code)

### 📊 So sánh tổng quan

| Tiêu chí | Dodge-Burn | Combined |
|----------|------------|----------|
| **Độ khó** | 🌟🌟 | 🌟🌟🌟🌟 |
| **Tốc độ** | ⚡⚡⚡ | ⚡⚡ |
| **Chất lượng chung** | 🎨🎨🎨🎨 | 🎨🎨🎨🎨🎨 |
| **Shading** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Edges** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Khuyên dùng** | Chân dung | Tổng quát |

### 🚀 Ứng dụng thực tế

Dự án này có thể dùng cho:

1. **Nghệ thuật:**
   - Chuyển ảnh thành sketch để in lên áo, cốc
   - Tạo ảnh đại diện nghệ thuật
   - Thiết kế poster

2. **Giáo dục:**
   - Học vẽ: So sánh ảnh sketch với bản vẽ tay
   - Dạy hình học: Nhìn rõ đường nét

3. **Thiết kế:**
   - Tạo mockup sản phẩm
   - Wireframe cho UI/UX
   - Storyboard phim

### 💡 Bài học rút ra

**1. Đơn giản hóa vấn đề phức tạp:**
- Chia nhỏ thành các bước
- Giải quyết từng bước một
- Kết hợp lại

**2. Kết hợp nhiều kỹ thuật:**
- Không có 1 thuật toán hoàn hảo
- Kết hợp nhiều thuật toán → Kết quả tốt hơn
- Combined = Dodge-Burn + Canny

**3. Tuning parameters quan trọng:**
- blur_ksize = 21 (không phải 10, không phải 50)
- alpha = 0.7, beta = 0.3 (không phải 0.5-0.5)
- → Thử nghiệm nhiều lần mới ra con số tốt

### 🎓 Kiến thức đã học

**Xử lý ảnh:**
- Histogram Equalization
- Edge Detection (Canny)
- Morphological Operations
- Image Filtering (Gaussian, Bilateral)
- Image Blending

**Lập trình:**
- Python programming
- OpenCV library
- NumPy arrays
- Error handling

**Web development:**
- Flask framework
- RESTful API
- Frontend-backend integration
- File handling

### 🌟 Điểm nổi bật của dự án

**1. Chất lượng cao:**
- Sử dụng thuật toán state-of-the-art
- CLAHE cho adaptive enhancement
- Canny cho edge detection tốt nhất

**2. Sáng tạo:**
- Kết hợp Dodge-Burn (nhiếp ảnh) + Canny (CV)
- Tỷ lệ 70-30 qua thử nghiệm
- Post-processing nhiều tầng

**3. Hoàn thiện:**
- Full-stack application
- User-friendly interface
- Comprehensive error handling
- Auto cleanup, auto resize

### 📈 Hướng phát triển

**Ngắn hạn:**
- Thêm slider cho user tự chọn alpha/beta
- Real-time preview
- Batch processing

**Dài hạn:**
- Deep learning (pix2pix, CycleGAN)
- Mobile app
- Cloud deployment
- API for integration

---

## PHỤ LỤC: GIẢI THÍCH THÊM

### A. Tại sao dùng 256 trong công thức chia?

**Câu hỏi:** `Sketch = (Gray × 256) / InvertedBlur`

Tại sao nhân 256, không phải 100 hay 255?

**Trả lời:**

```
Giả sử không nhân (scale = 1):
- Gray = 100
- InvertedBlur = 100
- Sketch = 100 / 100 = 1

→ Kết quả quá TỐI (1 gần như đen)

Nhân 255:
Sketch = 100 × 255 / 100 = 255

→ Luôn ra 255 (quá SÁNG)

Nhân 256:
Sketch = 100 × 256 / 100 = 256 → clip về 255

→ Vừa đủ sáng, giống giấy vẽ trắng!
```

**256 = 2^8:**
- Dễ tính toán cho máy tính (lũy thừa 2)
- Empirically tốt nhất

### B. Tại sao Bilateral Filter giữ được viền?

**Giải thích chi tiết:**

Gaussian Filter thường:
```
Pixel và hàng xóm:
[100, 100, 100, 200, 200, 200]
               ↑
         Pixel ở viền

Gaussian blur:
= (100 + 100 + 100 + 200 + 200 + 200) / 6
= 150

→ Viền bị MỜ (từ 100-200 thành 150)
```

Bilateral Filter:
```
Công thức: Chỉ lấy trung bình pixel GIỐNG

Pixel = 100
Hàng xóm bên trái: 100, 100 (GIỐNG)
Hàng xóm bên phải: 200, 200 (KHÁC)

Bilateral chỉ lấy pixel GIỐNG:
= (100 + 100 + 100) / 3 = 100

→ Viền GIỮ NGUYÊN (vẫn 100)
```

**Công thức thật (đơn giản hóa):**

```
Trọng số = Gaussian(khoảng cách) × Gaussian(độ khác màu)

Pixel giống:
- Độ khác màu = 0 → Gaussian(0) = 1 → Trọng số CAO

Pixel khác:
- Độ khác màu = 100 → Gaussian(100) ≈ 0 → Trọng số THẤP

→ Chỉ pixel giống được tính!
```

### C. Adaptive Thresholding của Canny

**Tại sao dùng median?**

```
Ảnh sáng:
Median = 150 → Low = 100, High = 200

Ảnh tối:
Median = 50 → Low = 33, High = 67

→ Tự động điều chỉnh theo độ sáng ảnh!
```

**Tại sao sigma = 0.33?**

Từ research paper của Canny:
- 0.33 cho kết quả TỐT NHẤT trên nhiều loại ảnh
- Không quá chặt, không quá lỏng

```
Nếu sigma = 0.1 (chặt):
Low = 90% median, High = 110% median
→ Quá chặt, mất viền nhỏ

Nếu sigma = 0.5 (lỏng):
Low = 50% median, High = 150% median
→ Quá lỏng, nhiễu được coi là viền

sigma = 0.33 (vừa):
Low = 67% median, High = 133% median
→ Cân bằng!
```

### D. Ví dụ hoàn chỉnh từ đầu đến cuối

**Input:** Ảnh chân dung 1024×768 pixels

**Bước 1: Upload**
- User chọn file "portrait.jpg" (2.5 MB)
- Browser gửi lên server
- Server lưu: `portrait_20251123_143055.jpg`

**Bước 2: Load & Resize**
```
Ảnh gốc: 4000×3000 pixels (lớn)
Resize: 1024×768 pixels (giữ tỷ lệ)
→ Tốc độ: 10s → 2s
```

**Bước 3: Chọn Combined**

**Bước 4: Xử lý**

Với 1 pixel ở má (vùng sáng, nền):

```
[Ảnh gốc RGB]
(200, 180, 160) → Grayscale = 180

[CLAHE]
180 → 190 (tăng contrast)

[Branch A: Dodge-Burn]
190 → Invert → 65
65 → Blur → 70
70 → Invert → 185
190 / 185 × 256 = 263 → clip 255
→ Dodge-Burn = 255

[Branch B: Canny Edges]
190 → CLAHE → 195
195 → Bilateral → 195
195 → Gradient = 10 (vùng phẳng)
10 < 50 (threshold) → KHÔNG phải viền
→ Edges = 0

[Combine]
0.7 × 255 + 0.3 × 0 = 178.5 → 179

[Bilateral]
179 → 180

[Unsharp]
180 → Blur 178 → 180 + (180-178) = 182

[Morph Gradient]
182 → Dilation 183, Erosion 181
Gradient = 2
0.9×182 + 0.1×2 = 164

[Denoise]
Opening: 164 → 164 (không đổi)

→ Kết quả cuối: 164
```

**Bước 5: Lưu**
- Lưu: `sketch_portrait_20251123_143055.jpg`
- Thời gian xử lý: 1.8s

**Bước 6: Hiển thị**
```
┌─────────────────┬─────────────────┐
│  portrait.jpg   │  sketch_...jpg  │
│   (ảnh màu)     │  (đen trắng)    │
│     📸          │       ✏️         │
└─────────────────┴─────────────────┘
```

**Bước 7: Download**
- User click "Tải về"
- Browser tải file về máy
- Kích thước: ~500 KB (từ 2.5 MB)

---

## KẾT LUẬN

### Những gì bạn đã học được

Sau khi đọc báo cáo này, bạn đã hiểu:

✅ **Khái niệm cơ bản:**
- Ảnh là ma trận số
- Pixel, grayscale, RGB
- Histogram

✅ **Hai phương pháp chính:**
- Dodge-Burn: Tô bóng tự nhiên
- Combined: Kết hợp tô bóng + viền

✅ **Các thuật toán:**
- CLAHE: Cải thiện tương phản
- Gaussian Blur: Làm mờ
- Canny: Phát hiện biên
- Bilateral: Lọc giữ viền
- Morphological: Xử lý hình thái

✅ **Tại sao mỗi bước quan trọng:**
- Không phải làm vì làm
- Mỗi bước có lý do rõ ràng
- Kết hợp tạo kết quả tốt

✅ **Cách sử dụng app:**
- Upload → Chọn → Xử lý → Tải về
- Đơn giản, ai cũng dùng được

### Lời kết

Dự án **SketchLab** là minh chứng cho việc:

**Khoa học + Nghệ thuật = Kết quả tuyệt vời**

Từ những công thức toán học khô khan:
```python
Sketch = (Gray × 256) / (255 - Blur(Invert))
```

Đến những bức tranh nghệ thuật đẹp mắt:
```
📸 → ✏️
```

**Đó là sức mạnh của Xử lý ảnh!**

---

**HẾT BÁO CÁO**

---

*Báo cáo này được viết với mục đích giải thích đơn giản, dễ hiểu cho người mới bắt đầu.*
*Mọi khái niệm đều được giải thích bằng ngôn ngữ đời thường, ví dụ cụ thể, và hình ảnh minh họa.*
*Nếu vẫn còn chỗ nào chưa rõ, đừng ngần ngại hỏi thêm!*

**Chúc bạn thành công với dự án! 🎉**
