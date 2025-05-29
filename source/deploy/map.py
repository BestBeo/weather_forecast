import streamlit as st
import folium
from folium.raster_layers import TileLayer
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# --- Map các lớp thời tiết ---
layer_map = {
    "PAC0 - Mưa đối lưu": "PAC0",
    "PR0 - Cường độ mưa": "PR0",
    "PARAIN - Tổng lượng mưa (rain)": "PARAIN",
    "PASNOW - Tổng lượng tuyết": "PASNOW",
    "SD0 - Độ sâu tuyết": "SD0",
    "WS10UV - Tốc độ gió (10m)": "WS10UV",
    "WNDUV - Hướng và tốc độ gió": "WNDUV",
    "APM - Áp suất khí quyển (mực nước biển)": "APM",
    "TA2 - Nhiệt độ không khí (2m)": "TA2",
    "TD2 - Điểm sương": "TD2",
    "TS0 - Nhiệt độ đất (0-10cm)": "TS0",
    "TS10 - Nhiệt độ đất (>10cm)": "TS10",
    "HRD0 - Độ ẩm tương đối": "HRD0",
    "CL - Mây": "CL"
}

# --- Chọn lớp thời tiết ---
selected_layer = st.selectbox("Chọn lớp thời tiết", list(layer_map.keys()))
layer_code = layer_map[selected_layer]
api_key = "0dbef9ad5e17aa391a3bf37e018be427"

tile_url = f"https://maps.openweathermap.org/maps/2.0/weather/1h/{layer_code}/{{z}}/{{x}}/{{y}}?appid={api_key}"

# --- Tạo bản đồ ---
m = folium.Map(location=[10.762622, 106.660172], zoom_start=10)

# --- Thêm lớp thời tiết (chỉ giữ thuộc tính cơ bản) ---
TileLayer(
    tiles=tile_url,
    attr="OpenWeatherMap",
    overlay=True,
    opacity=0.6
).add_to(m)

# --- Hiển thị bản đồ ---
st_folium(m, width=1500, height=700)

def show_weather_map(lat, lon, layer_code="temp_new", api_key="0dbef9ad5e17aa391a3bf37e018be427",
                     width_px=500, height_px=300):
    """
    Hiển thị bản đồ thời tiết từ OpenWeatherMap trên Streamlit.

    Parameters:
    - lat: vĩ độ
    - lon: kinh độ
    - layer_code: mã lớp bản đồ của OpenWeatherMap (ví dụ: "temp_new", "clouds_new", ...)
    - api_key: API key của bạn từ OpenWeatherMap
    - width_px: chiều rộng bản đồ (px)
    - height_px: chiều cao bản đồ (px)
    """
    tile_url = f"https://maps.openweathermap.org/maps/2.0/weather/1h/{layer_code}/{{z}}/{{x}}/{{y}}?appid={api_key}"
    
    m = folium.Map(location=[lat, lon], zoom_start=7)
    folium.TileLayer(tiles=tile_url, attr="OpenWeatherMap", overlay=True).add_to(m)
    
    map_html = m._repr_html_().replace("height:500%;", f"height:{height_px}px;")\
                              .replace("width:100%;", f"width:{width_px}px;")
    
    components.html(map_html, height=height_px + 120, width=width_px)
