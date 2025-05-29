import streamlit as st
st.set_page_config(page_title="Weather Forecast", page_icon="🌦️", layout="wide")

import warnings
warnings.filterwarnings("ignore", message="'Threading' parallel backend is not supported")

import folium
import base64
import pandas as pd
import numpy as np
import pickle
import streamlit.components.v1 as components

from PIL import Image 
from datetime import datetime, timedelta, timezone
from folium.raster_layers import TileLayer
from streamlit_folium import st_folium

from map import show_weather_map
from crawl import get_weather_data, process_info_weather_data, process_day_weather_data, process_hour_weather_data, process_station_info_data
from visualization import preprocess_weather_df, plot_hourly_temperature_averages, plot_precipitation, plot_snow_and_snowdepth, plot_visibility_humidity_cloudcover, plot_wind_by_hour, degree_to_wind_direction_abbr

# Đường dẫn đến các pkl
grid_gb_path = 'D:\\Đồ án\\DACN3\\source\\save\\best_grid_gb.pkl'
model_path = 'D:\\Đồ án\\DACN3\\source\\save\\gbC.pkl'
scaler_path = 'D:\\Đồ án\\DACN3\\source\\save\\scaler.pkl'
encoder_path = 'D:\\Đồ án\\DACN3\\source\\save\\label_encoder.pkl'
background_image_path = 'D:\\Đồ án\\DACN3\\data\\images\\background.png'

weather_images = {
    "Partially cloudy": "../../data/images/cloudy.png",
    "Rain": "../../data/images/rain.png",
    "Clear": "../../data/images/clear.png",
    "Overcast": "../../data/images/overcast.png",
    "Snow": "../../data/images/snow.png",
    "Freezing Drizzle/Freezing Rain": "../../data/images/dizzle.png",
    "Ice": "../../data/images/snow.png"
}

@st.cache_resource
def load_models():
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    with open(scaler_path, 'rb') as f:
        scaler = pickle.load(f)
    with open(encoder_path, 'rb') as f:
        encoder = pickle.load(f)
    with open(grid_gb_path, 'rb') as f:
        grid_gb = pickle.load(f)
    return model, scaler, encoder, grid_gb

model, scaler, encoder, grid_gb = load_models()

def set_background(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()
    css_code = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{base64_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

def preprocess_input(df_day):
    df_day_copy = df_day.copy()

    # Tách data datetime
    df_day_copy['datetime'] = pd.to_datetime(df_day_copy['datetime'], format='mixed')
    df_day_copy['year'] = df_day_copy['datetime'].dt.year
    df_day_copy['month'] = df_day_copy['datetime'].dt.month
    df_day_copy['day'] = df_day_copy['datetime'].dt.day
    df_day_copy.drop('datetime',axis=1,inplace=True)

    # Tách data sunrise
    df_day_copy['sunrise'] = pd.to_datetime(df_day_copy['sunrise'],errors='coerce')
    df_day_copy['hour_sunrise'] = df_day_copy['sunrise'].dt.hour
    df_day_copy['minute_sunrise'] = df_day_copy['sunrise'].dt.minute
    df_day_copy['second_sunrise'] = df_day_copy['sunrise'].dt.second
    df_day_copy.drop('sunrise',axis=1,inplace=True)

    # Tách data sunset
    df_day_copy['sunset'] = pd.to_datetime(df_day_copy['sunset'],errors='coerce')
    df_day_copy['hour_sunset'] = df_day_copy['sunset'].dt.hour
    df_day_copy['minute_sunset'] = df_day_copy['sunset'].dt.minute
    df_day_copy['second_sunset'] = df_day_copy['sunset'].dt.second
    df_day_copy.drop('sunset',axis=1,inplace=True)

    # Xử lý giá trị thiếu
    df_day_copy['preciptype'] = df_day_copy['preciptype'].fillna('no precipitation')
    df_day_copy['snowdepth'] = pd.to_numeric(df_day_copy['snowdepth'], errors='coerce').fillna(0.0)
    df_day_copy['severerisk'] = df_day_copy['severerisk'].fillna(0)

    # Mã hóa cột preciptype
    df_day_copy['preciptype'] = df_day_copy['preciptype'].apply(
        lambda x: x if x in encoder.classes_ else 'no precipitation'
    )
    df_day_copy['preciptype'] = encoder.transform(df_day_copy['preciptype'])

    # Lựa chọn đặc trưng
    features = [
        'tempmax', 'tempmin', 'temp', 'feelslikemax', 'feelslikemin',
        'feelslike', 'dew', 'humidity', 'precip', 'precipprob', 'precipcover',
        'preciptype', 'snow', 'snowdepth', 'windgust', 'windspeed', 'winddir',
        'sealevelpressure', 'cloudcover', 'visibility', 'solarradiation',
        'solarenergy', 'uvindex', 'severerisk', 'moonphase',
        'year', 'month', 'day', 'hour_sunrise', 'minute_sunrise',
        'second_sunrise', 'hour_sunset', 'minute_sunset', 'second_sunset'
    ]
    df_day_copy = df_day_copy[features]

    # Chuẩn hóa dữ liệu
    df_day_copy = scaler.transform(df_day_copy)
    df_day_copy = pd.DataFrame(df_day_copy, columns=features)

    return df_day_copy

def fetch_and_store_weather(location):
    weather = get_weather_data(location)
    st.session_state["df_info"] = process_info_weather_data(weather)
    st.session_state["df_day"] = process_day_weather_data(weather)
    st.session_state["df_hour"] = process_hour_weather_data(weather)
    st.session_state["df_station"] = process_station_info_data(weather)
    st.session_state["location"] = location
    st.session_state["weather_ready"] = True

def write_location(location: str) -> str:
    flocation = location.title()
    return flocation

def get_current_time(timezone_offset) -> str:
    # Lấy thời gian hiện tại ở UTC
    current_utc_time = datetime.now(timezone.utc)

    # Nếu là Series, lấy giá trị đầu tiên
    if isinstance(timezone_offset, pd.Series):
        timezone_offset = timezone_offset.iloc[0]

    # Chuyển sang giờ địa phương (timezone_offset tính theo giờ)
    local_time = current_utc_time + timedelta(hours=timezone_offset)

    # Trả về chuỗi thời gian định dạng
    return local_time.strftime('%m/%d/%Y  %I:%M:%S %p')

def main():
    st.title('🌦️ Weather Forecast')
    # set_background(background_image_path)
    menu_choice = st.sidebar.radio("Choose Action:", ["🌍 Search", "📋 Input Parameters"])

    if menu_choice == "🌍 Search":
        col1, col2 = st.columns([8,2])
        with col1:
            location = st.text_input("🌍Nhập địa điểm", placeholder="Ví dụ: Hanoi")
        with col2:
            st.markdown("""
                <style>
                div.stButton > button:first-child {
                    height: auto; /* Hoặc một giá trị pixel cụ thể, ví dụ: 50px */
                    min-width: 50px; /* Đặt chiều rộng tối thiểu */
                    padding: 10px 20px; /* Điều chỉnh khoảng cách bên trong nút */
                }
                </style>""", unsafe_allow_html=True)
            if st.button("🔍 Tìm kiếm"):
                if location:
                    fetch_and_store_weather(location)
                else:
                    st.warning("Vui lòng nhập địa điểm trước khi tìm.")

    elif menu_choice == "📋 Input Parameters":
        location = 'Location'
        st.sidebar.header('📋 Input Parameters')

        # Nhập các thông số từ người dùng
        datetime = st.sidebar.date_input('📅 Date', value=pd.Timestamp('today').date()).strftime('%#m/%#d/%Y')

        tempmax = st.sidebar.number_input("🌡️ Nhiệt độ tối đa (°C)", value=0.0)
        tempmin = st.sidebar.number_input("🌡️ Nhiệt độ tối thiểu (°C)", value=0.0)
        temp = st.sidebar.number_input("🌡️ Nhiệt độ trung bình (°C)", value=0.0)
        feelslikemax = st.sidebar.number_input("🤒 Cảm giác nhiệt tối đa (°C)", value=0.0)
        feelslikemin = st.sidebar.number_input("🤒 Cảm giác nhiệt thiểu (°C)", value=0.0)
        feelslike = st.sidebar.number_input("🤒 Cảm giác nhiệt trung bình (°C)", value=0.0)
        dew = st.sidebar.number_input("❄️ Nhiệt độ điểm sương (°C)", value=0.0)
        humidity = st.sidebar.number_input("💧 Độ ẩm (%)", min_value=0.0, max_value=100.0, value=0.0)
        precip = st.sidebar.number_input("🌧️ Lượng mưa (mm)", min_value=0.0, value=0.0)
        precipprob = st.sidebar.selectbox("🌧️ Xác suất mưa (%)", options=[0, 100])
        precipcover = st.sidebar.number_input("🌧️ Phủ mưa (%)", min_value=0.0, max_value=100.0, value=0.0)
        preciptype = st.sidebar.selectbox("🌧️ Loại mưa", options=[
            'freezingrain', 'snow', 'no precipitation', 'rain', 'rain,freezingrain',
            'rain,freezingrain,snow', 'rain,freezingrain,snow,ice', 'rain,ice',
            'rain,snow', 'rain,snow,ice', 'snow,ice'
        ])
        snow = st.sidebar.number_input("❄️ Lượng tuyết (cm)", min_value=0.0, value=0.0)
        snowdepth = st.sidebar.number_input("❄️ Độ sâu tuyết (cm)", min_value=0.0, value=0.0)
        windgust = st.sidebar.number_input("💨 Gió giật (kph)", min_value=0.0, value=0.0)
        windspeed = st.sidebar.number_input("💨 Tốc độ gió (kph)", min_value=0.0, value=0.0)
        winddir = st.sidebar.number_input("🧭 Hướng gió (độ)", min_value=0.0, max_value=360.0, value=0.0)
        sealevelpressure = st.sidebar.number_input("🌍 Áp suất khí quyển (mb)", min_value=0.0, value=1000.0)
        cloudcover = st.sidebar.number_input("☁️ Mức độ mây (%)", min_value=0.0, max_value=100.0, value=0.0)
        visibility = st.sidebar.number_input("👀 Tầm nhìn (km)", min_value=0.0, max_value=50.0, value=0.0)
        solarradiation = st.sidebar.number_input("☀️ Bức xạ mặt trời (W/m²)", min_value=0.0, value=0.0)
        solarenergy = st.sidebar.number_input("🔋 Năng lượng mặt trời (MJ/m²)", min_value=0.0, value=0.0)
        uvindex = st.sidebar.selectbox("🔆 Chỉ số UV", options=list(range(11)))
        severerisk = st.sidebar.slider("⚠️ Rủi ro thời tiết nghiêm trọng", min_value=0, max_value=100, value=0)

        datetime_str = pd.to_datetime(datetime).strftime('%Y-%m-%d')
        sunrise = st.sidebar.text_input("🌅 Giờ mặt trời mọc (ISO 8601)", value=f"{datetime_str}T06:00:00")
        sunset = st.sidebar.text_input("🌇 Giờ mặt trời lặn (ISO 8601)", value=f"{datetime_str}T18:00:00")
        moonphase = st.sidebar.number_input("🌙 Pha mặt trăng", min_value=0.00, max_value=1.00, value=0.00)

        # Tạo DataFrame từ thông tin nhập từ người dùng
        if st.sidebar.button("🔍 Dự đoán"):
            fetch_and_store_weather(location)
            st.session_state["df_day"] = pd.DataFrame({
                "datetime": [datetime],
                "tempmax": [tempmax],
                "tempmin": [tempmin],
                "temp": [temp],
                "feelslikemax": [feelslikemax],
                "feelslikemin": [feelslikemin],
                "feelslike": [feelslike],
                "dew": [dew],
                "humidity": [humidity],
                "precip": [precip],
                "precipprob": [precipprob],
                "precipcover": [precipcover],
                "preciptype": [preciptype],
                "snow": [snow],
                "snowdepth": [snowdepth],
                "windgust": [windgust],
                "windspeed": [windspeed],
                "winddir": [winddir],
                "sealevelpressure": [sealevelpressure],
                "cloudcover": [cloudcover],
                "visibility": [visibility],
                "solarradiation": [solarradiation],
                "solarenergy": [solarenergy],
                "uvindex": [uvindex],
                "severerisk": [severerisk],
                "sunrise": [sunrise],
                "sunset": [sunset],
                "moonphase": [moonphase]
            })
        
    if st.session_state.get("weather_ready") and st.session_state["df_day"] is not None:

        df_day = st.session_state["df_day"]
        processed_data = preprocess_input(df_day)

        # Dự đoán với model đã load
        predictions = grid_gb.predict(processed_data)

        # Giải mã dự đoán thành DataFrame với cột nhãn
        label_names = ['Partially cloudy', 'Rain', 'Clear', 'Overcast', 'Snow', 'Freezing Drizzle/Freezing Rain', 'Ice']
        predicted_labels_df = pd.DataFrame(predictions, columns=label_names)

        # Lấy nhãn được dự đoán (dự đoán 1 dòng)
        predicted_row = predicted_labels_df.iloc[0]
        predicted_labels = [label for label, value in predicted_row.items() if value == 1]

        # Lấy dữ liệu input dòng đầu tiên (vì chỉ 1 dòng)
        input_data = df_day.iloc[0]
        st.markdown("""
        <style>
        .weather-container {
            background-color: #f0f7fd; /* Màu xanh da trời nhạt */
            border-radius: 10px; /* Bo góc với bán kính 10px */
            
            border-left: 5px solid #c3d3e0;
            
            padding: 15px; /* Thêm padding */
            padding-left: 25px;
            display: flex; /* Sử dụng flexbox cho bố cục */
            flex-direction: column; /* Các phần tử con xếp theo chiều dọc */
        }

        .subcol-container {
            display: flex; /* Sử dụng flexbox cho các sub-column */
            gap: 10px; /* Khoảng cách giữa các sub-column */
            margin-bottom: 10px; /* Khoảng cách với phần tử tiếp theo */
        }

        .subcol-2 {
            flex: 1; /* Chiếm không gian bằng nhau */
        }

        .subcol-4-6 {
            display: grid;
            grid-template-columns: 5fr 5fr;
            gap: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        # Tạo 2 cột
        col1, col2, col3 = st.columns([11,7,12])

        # Chuyển input_data sang list để dễ chia đôi
        input_items = list(input_data.items())
        with col1:
                formatted_location = write_location(location)
                st.markdown(f"""
                    <h3 style='margin-bottom: 0;'> Weather in {formatted_location} </h3>
                    """, unsafe_allow_html=True)
                weather_html = f"""
                    <div class="weather-container">
                        <div class="subcol-container">
                            <div class="subcol-2">
                                <h4 style='font-size: 50px; margin-bottom: 0;margin-top: 0;'>Now</h4>
                """
                for key, value in input_items:
                    if key == "temp":
                        weather_html += f"<p style='font-size: 32px; font-weight: bold; margin: 0;'>{value} °C</p>"
                if predicted_labels:
                    labels_string = ", ".join(predicted_labels)
                    
                    weather_html += f"<p style='font-size: 15px; margin: 0;'>{labels_string}</p>"
                    
                
                else:
                    weather_html += '<i style="color: #888;">No weather condition predicted.</i>'
                weather_html += """
                    </div>
                    <div class="subcol-2">
                """
                
                priority_order = ["Snow", "Rain", "Overcast", "Partially cloudy", "Clear"]
                if predicted_labels:
                    for label in priority_order:
                        if label in predicted_labels and label in weather_images:
                            with open(weather_images[label], 'rb') as img_file:
                                encoded_img = base64.b64encode(img_file.read()).decode()
                            weather_html += f'<img src="data:image/png;base64,{encoded_img}" style="width: 150px; height: auto;">'
                            break  # Hiển thị xong 1 ảnh là thoát luôn
                weather_html += """
                            </div> </div>
                        <div class="subcol-4-6">
                """
                for key, value in input_items:
                    if key == "feelslike":
                        weather_html += f"<div><b>Feelslike:</b> {value} °C</div>"
                    if key == "windspeed":
                        for dir_key, dir_value in input_items:
                            if dir_key == "winddir":
                                weather_html += f"<div><b>Wind:</b> {value} km/h {degree_to_wind_direction_abbr(dir_value)}</div>"
                    if key == "snow":
                        weather_html += f"<div><b>Snow:</b> {value} cm</div>"
                    if key == "sealevelpressure":
                        weather_html += f"<div><b>Pressure:</b> {value}</div>"
                    if key == "dew":
                        weather_html += f"<div><b>Dew Point:</b> {value} °C</div>"
                    if key == "visibility":
                        weather_html += f"<div><b>Visibility:</b> {value} km</div>"
                    if key == "humidity":
                        weather_html += f"<div><b>Humidity:</b> {value} %</div>"
                    if key == "cloudcover":
                        weather_html += f"<div><b>Cloud Cover:</b> {value} %</div>"

                weather_html += """
                        </div>
                    </div>
                """
                st.markdown(weather_html, unsafe_allow_html=True)   
        with col2:
            st.markdown(f"<h3 style='margin-bottom: 0;'> </h3>", unsafe_allow_html=True)
            st.markdown(f"<b>Location:</b> {write_location(location)}", unsafe_allow_html=True)
            for key, value in input_items:
                if key == "datetime":
                    df_info = st.session_state["df_info"]
                    timeoff= df_info["timezone_offset"].iloc[0]
                    st.markdown(f"<b>Current Time:</b> {get_current_time(timeoff)} ", unsafe_allow_html=True)  
            for key, value in input_items:
                if key == "sunrise":
                    st.markdown(f"<b>Sunrise:</b> {value}", unsafe_allow_html=True)
            for key, value in input_items:
                if key == "sunset":
                    st.markdown(f"<b>Sunset:</b> {value}", unsafe_allow_html=True)
            for key, value in input_items: 
                if key == "tempmax":
                    for key1, value1 in input_items:
                        if key1 == "tempmin":
                            st.markdown(f"<b>Temperature:</b> {value1} - {value} °C ", unsafe_allow_html=True)   
            for key, value in input_items:
                if key == "sealevelpressure" :
                    st.markdown(f"<b>Sea Level Pressure:</b> {value} mb", unsafe_allow_html=True)
            for key, value in input_items:
                if key == "uvindex":
                    st.markdown(f"<b>UV:</b> {value} ", unsafe_allow_html=True)  
            for key, value in input_items:
                if key == "moonphase":
                    st.markdown(f"<b>Moon Phase:</b> {value} ", unsafe_allow_html=True)  
            
        with col3:
            if location == "Location":
                fetch_and_store_weather('da nang')
                df_info = st.session_state["df_info"]
                lat = df_info["latitude"].iloc[0]
                lon = df_info["longitude"].iloc[0]
                st.markdown(f"<h3 style='margin-bottom: 0;'> </h3>", unsafe_allow_html=True)
                show_weather_map(lat,lon)
            else:
                df_info = st.session_state["df_info"]
                lat = df_info["latitude"].iloc[0]
                lon = df_info["longitude"].iloc[0]
                st.markdown(f"<h3 style='margin-bottom: 0;'> </h3>", unsafe_allow_html=True)
                show_weather_map(lat,lon)

    if st.session_state.get("weather_ready") and st.session_state.get("df_hour") is not None:
        df_hour = st.session_state["df_hour"]
        df_process = preprocess_weather_df(df_hour)

        if location == "Location":
            st.subheader("")
        else:
            st.subheader("📊 Biểu đồ thời tiết theo giờ")

            # Danh sách các biểu đồ
            chart_options = [
                "Nhiệt độ (Temperature)",
                "Lượng mưa (Precipitation)",
                "Tuyết & Độ dày tuyết (Snow & Snowdepth)",
                "Tầm nhìn - Độ ẩm - Mây (Visibility - Humidity - Cloudcover)",
                "Gió theo giờ (Wind by Hour)"
            ]

            # Selectbox thay cho hàng nút
            selected_chart = st.selectbox("📊 Chọn biểu đồ thời tiết:", chart_options)

            # Lưu vào session state nếu cần dùng lại
            st.session_state.selected_chart = selected_chart

            # Ánh xạ biểu đồ tương ứng
            figs = {
                "Nhiệt độ (Temperature)": plot_hourly_temperature_averages(df_process),
                "Lượng mưa (Precipitation)": plot_precipitation(df_process),
                "Tuyết & Độ dày tuyết (Snow & Snowdepth)": plot_snow_and_snowdepth(df_process),
                "Tầm nhìn - Độ ẩm - Mây (Visibility - Humidity - Cloudcover)": plot_visibility_humidity_cloudcover(df_process),
                "Gió theo giờ (Wind by Hour)": plot_wind_by_hour(df_process, degree_to_wind_direction_abbr),
            }

            # Hiển thị biểu đồ tương ứng
            st.pyplot(figs[st.session_state.selected_chart])
    else:
        st.info("🔍 Hãy nhập địa điểm và nhấn Tìm để hiển thị biểu đồ thời tiết.")

if __name__ == '__main__':
    main()
