# Weather Forecast ⛅️

**Weather Forecast** là một ứng dụng web dự báo thời tiết theo thời gian thật, được xây dựng bằng Streamlit. Ứng dụng khai thác API từ OpenWeatherMap và VisualCrossing để lấy dữ liệu thời tiết, kết hợp với mô hình học máy (Gradient Boosting Classifier) để dự đoán tình trạng thời tiết và trực quan hóa dữ liệu trên bản đồ và biểu đồ.

---

## ✨ Tính Năng

* ⛺ Tìm kiếm thời tiết theo địa điểm
* ✍️ Nhập thông số thủ công để dự đoán
* 🌍 Bản đồ thời tiết tương tác với Folium
* 📊 Trực quan hóa dữ liệu theo giờ
* ✨ Dự đoán thời tiết bằng mô hình ML
* 📅 Giao diện Streamlit dễ dùng, thân thiện

---

## 🚀 Công Nghệ Sử Dụng

### Ngôn ngữ

* Python 3.8+

### Thư viện chính

* `streamlit`: Giao diện web
* `folium`: Bản đồ tương tác
* `pandas`, `numpy`: Xử lý dữ liệu
* `matplotlib`, `seaborn`: Biểu đồ
* `scikit-learn`: Mô hình học máy
* `feature-engine`, `imbalanced-learn`: Tiền xử dữ liệu
* `catboost`, `xgboost`, `lightgbm`, `tensorflow`: Hỗ trợ ML/DL
* `pickle`: Lưu/tải mô hình

### API

* **OpenWeatherMap**: Dữ liệu thời tiết bản đồ
* **VisualCrossing**: Dữ liệu thời tiết theo ngày/giờ

### Mô hình học máy

* `GradientBoostingClassifier` (OneVsRestClassifier)

---

## 📁 Cài Đặt

### Yêu cầu

* Python >= 3.8
* Kết nối Internet
* API Key: OpenWeatherMap và VisualCrossing

### Hướng dẫn cài đặt

```bash
# Clone repository
$ git clone https://github.com/BestBeo/weather_forecast.git
$ cd weather_forecast

# Tạo và kích hoạt môi trường ảo
$ python -m venv venv
$ source venv/bin/activate      # Linux/Mac
$ venv\Scripts\activate        # Windows

# Cài đặt thư viện
$ pip install -r requirements.txt
```

### Cấu hình API Key

* Vào `source/map.py`, thay `api_key = "your_openweathermap_api_key"`
* Vào `source/crawl.py`, thay API Key trong URL:

  ```python
  url = f"https://weather.visualcrossing.com/...&key=your_visualcrossing_api_key"
  ```

### Chuẩn bị mô hình

* Tệp mô hình đã có trong `source/save/`:

  * `gbC.pkl`, `scaler.pkl`, `label_encoder.pkl`, `best_grid_gb.pkl`
* Muốn huấn luyện lại: chạy notebook `final_160_Weather_Prediction.ipynb`

### Chạy ứng dụng

```bash
$ streamlit run source/deploy.py
```

---

## ⛰️ Cách Sử Dụng

1. **Khởi chạy:**

   * Vào [http://localhost:8501](http://localhost:8501) sau khi chạy lệnh trên

2. **Tìm kiếm địa điểm:**

   * Chọn tab "🌍 Search"
   * Nhập tên thành phố (vd: Hanoi)
   * Xem thời tiết, bản đồ, biểu đồ

3. **Nhập thông số thủ công:**

   * Tab "📋 Input Parameters"
   * Nhập nhiệt độ, độ ẩm, mưa...
   * Nhấn "🔍 Dự đoán"

4. **Xem bản đồ:**

   * Chọn lớp mưa, gió, nhiệt độ...

5. **Xem biểu đồ:**

   * Chọn loại biểu đồ để xem theo giờ

---

## 🗂️ Cấu Trúc Thư Mục

```
weather_forecast/
├── baocao/              # Báo cáo & tài liệu
├── data/                # Dữ liệu & hình ảnh
│   ├── day/, hour/, images/
├── source/              # Mã nguồn & mô hình
│   ├── crawl.py
│   ├── deploy.py
│   ├── map.py
│   ├── visualization.py
│   └── save/
│       ├── gbC.pkl, scaler.pkl, label_encoder.pkl, best_grid_gb.pkl
├── final_160_Weather_Prediction.ipynb
├── requirements.txt
```

---

## 🙏 Cảm ơn bạn đã sử dụng **Weather Forecast**! 🌧️
