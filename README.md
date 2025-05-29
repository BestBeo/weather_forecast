Dự Báo Thời Tiết
Weather Forecast là một ứng dụng web được xây dựng bằng Streamlit để cung cấp thông tin dự báo thời tiết theo thời gian thực và trực quan hóa dữ liệu thời tiết. Ứng dụng tích hợp API từ OpenWeatherMap và VisualCrossing để lấy dữ liệu thời tiết, sử dụng mô hình học máy (Gradient Boosting Classifier) để dự đoán tình trạng thời tiết, và hiển thị bản đồ thời tiết cùng các biểu đồ phân tích.
Tính Năng

Tìm kiếm thời tiết theo địa điểm: Nhập tên thành phố (ví dụ: Hanoi, Da Nang) để xem thông tin thời tiết chi tiết.
Nhập thông số thủ công: Cho phép người dùng nhập các tham số thời tiết (nhiệt độ, độ ẩm, lượng mưa, v.v.) để dự đoán tình trạng thời tiết.
Bản đồ thời tiết tương tác: Hiển thị bản đồ thời tiết với các lớp như mưa, nhiệt độ, độ ẩm, tốc độ gió, v.v., sử dụng Folium và OpenWeatherMap.
Trực quan hóa dữ liệu: Cung cấp các biểu đồ theo giờ về nhiệt độ, lượng mưa, tuyết, tầm nhìn, độ ẩm, mức độ mây, và tốc độ gió.
Dự đoán thời tiết: Sử dụng mô hình Gradient Boosting Classifier để dự đoán các điều kiện thời tiết như "Clear", "Rain", "Snow", v.v.
Giao diện thân thiện: Được xây dựng với Streamlit, hỗ trợ bố cục rộng và giao diện trực quan.

Công Nghệ Sử Dụng

Ngôn ngữ lập trình: Python 3.8+
Thư viện chính:
Streamlit: Giao diện người dùng web.
Folium: Hiển thị bản đồ thời tiết tương tác.
P byas, NumPy: Xử lý và phân tích dữ liệu.
Matplotlib, Seaborn: Trực quan hóa dữ liệu bằng biểu đồ.
Scikit-learn: Xử lý mô hình học máy và chuẩn hóa dữ liệu.
Feature-engine, Imbalanced-learn: Xử lý đặc trưng và cân bằng dữ liệu.
CatBoost, XGBoost, LightGBM: Các mô hình học máy nâng cao.
TensorFlow: Hỗ trợ Deep Learning.
Pickle: Lưu và tải mô hình học máy.


API:
OpenWeatherMap: Cung cấp dữ liệu bản đồ thời tiết.
VisualCrossing: Cung cấp dữ liệu thời tiết chi tiết (ngày, giờ, hiện tại).


Mô hình học máy: Gradient Boosting Classifier (OneVsRestClassifier) để dự đoán tình trạng thời tiết.

Cài Đặt
Yêu cầu

Python 3.8 hoặc cao hơn.
Kết nối internet để truy cập API thời tiết.
Tài khoản OpenWeatherMap và VisualCrossing để lấy API Key.

Hướng dẫn cài đặt

Clone repository:git clone https://github.com/BestBeo/weather_forecast.git
cd weather_forecast


Tạo môi trường ảo (khuyến nghị):python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Cài đặt các thư viện:Tất cả các thư viện cần thiết đã được liệt kê trong tệp requirements.txt. Chạy lệnh sau để cài đặt:pip install -r requirements.txt


Cấu hình API Key:
Đăng ký tài khoản tại OpenWeatherMap và VisualCrossing.
Thay thế api_key trong tệp map.py bằng API Key của bạn:api_key = "your_openweathermap_api_key"


Cập nhật URL API trong crawl.py với API Key của VisualCrossing:url = f"https://weather.visualcrossing.com/...&key=your_visualcrossing_api_key"




Chuẩn bị mô hình học máy:
Tệp mô hình (gbC.pkl, scaler.pkl, label_encoder.pkl, best_grid_gb.pkl) đã được lưu sẵn trong thư mục source/save.
Nếu bạn muốn huấn luyện lại mô hình, chạy notebook final_160_Weather_Prediction.ipynb với dữ liệu thời tiết phù hợp.


Chạy ứng dụng:streamlit run deploy.py



Cách Sử Dụng

Chạy ứng dụng:
Sau khi chạy lệnh streamlit run deploy.py, ứng dụng sẽ mở trong trình duyệt tại http://localhost:8501.


Tìm kiếm thời tiết:
Chọn tab "🌍 Search" ở thanh bên.
Nhập tên địa điểm (ví dụ: Hanoi) và nhấn "🔍 Tìm kiếm".
Xem thông tin thời tiết chi tiết, bản đồ thời tiết, và các biểu đồ theo giờ.


Nhập thông số thủ công:
Chọn tab "📋 Input Parameters" ở thanh bên.
Nhập các thông số thời tiết (nhiệt độ, độ ẩm, lượng mưa, v.v.).
Nhấn "🔍 Dự đoán" để nhận dự đoán tình trạng thời tiết.


Xem bản đồ thời tiết:
Chọn lớp thời tiết (ví dụ: mưa, nhiệt độ, gió) từ menu thả xuống.
Bản đồ sẽ hiển thị dữ liệu thời tiết tương ứng cho khu vực được chọn.


Xem biểu đồ:
Chọn loại biểu đồ (nhiệt độ, lượng mưa, tuyết, v.v.) từ menu thả xuống để xem dữ liệu theo giờ.



Cấu Trúc Dự Án
weather_forecast/
├── baocao/                  # Thư mục chứa báo cáo và tài liệu
│   ├── 07AD-Vẽu đư Đỗ ăn Chuyên ngành 3.docx
│   ├── Báo cáo Đỗ ăn Chuyên ngành 3.pdf
│   ├── DACN3 - Weather Forecast.pdf
│   ├── Đề cương Đỗ ăn Chuyên ngành 3.docx
│   └── Đề cương Đỗ ăn Chuyên ngành 3.pdf
├── data/                    # Thư mục chứa dữ liệu và hình ảnh
│   ├── day/                 # Dữ liệu ngày
│   ├── hour/                # Dữ liệu giờ
│   ├── images/              # Thư mục chứa hình ảnh
│   │   ├── background.png   # Ảnh nền ứng dụng
│   │   ├── clear.png        # Hình ảnh điều kiện thời tiết "Clear"
│   │   ├── cloudy.png       # Hình ảnh điều kiện thời tiết "Cloudy"
│   │   ├── drizzle.png      # Hình ảnh điều kiện thời tiết "Drizzle"
│   │   ├── fog.png          # Hình ảnh điều kiện thời tiết "Fog"
│   │   ├── haze.png         # Hình ảnh điều kiện thời tiết "Haze"
│   │   ├── rain.png         # Hình ảnh điều kiện thời tiết "Rain"
│   │   ├── snow.png         # Hình ảnh điều kiện thời tiết Bergman
│   │   ├── thunderstorms.png # Hình ảnh điều kiện thời tiết "Thunderstorms"
│   ├── 160city_116960rows.csv # Dữ liệu thành phố
│   └── find_data.csv        # Dữ liệu bổ sung
├── source/                  # Thư mục chứa mã nguồn và mô hình
│   ├── __pycache__/         # Cache Python
│   ├── crawl.py             # Lấy và xử lý dữ liệu từ API VisualCrossing
│   ├── deploy.py            # Ứng dụng Streamlit chính
│   ├── map.py               # Hiển thị bản đồ thời tiết với Folium
│   ├── visualization.py     # Tạo các biểu đồ trực quan hóa dữ liệu
│   └── save/                # Thư mục chứa mô hình học máy
│       ├── best_grid_gb.pkl # Mô hình tối ưu hóa GridSearch
│       ├── deep.keras       # Mô hình Deep Learning (TensorFlow)
│       ├── gbC.pkl          # Mô hình Gradient Boosting Classifier
│       ├── label_encoder.pkl # LabelEncoder
│       └── scaler.pkl       # StandardScaler
├── final_160_Weather_Prediction.ipynb # Notebook huấn luyện mô hình
└── requirements.txt         # Danh sách thư viện cần thiết


Cảm ơn bạn đã sử dụng Weather Forecast! 🌦️
