import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from crawl import get_weather_data, process_hour_weather_data

def preprocess_weather_df(df):
    # Điền giá trị mặc định cho các cột có thể thiếu
    df['preciptype'] = df['preciptype'].fillna('no precipitation')
    df['snowdepth'] = pd.to_numeric(df['snowdepth'], errors='coerce').fillna(0.0)
    
    # Xoá các cột không cần thiết
    df = df.drop(columns=['datetimeEpoch', 'conditions', 'stations'], errors='ignore')

    # Chuyển 'datetime' thành kiểu thời gian
    df['datetime'] = pd.to_datetime(df['datetime'], format='%H:%M:%S', errors='coerce')

    # Trích xuất giờ trong ngày
    df['hour'] = df['datetime'].dt.hour

    return df

def plot_hourly_temperature_averages(df):
    # Tính trung bình theo giờ
    df_hourly_avg = df.groupby('hour')[['temp', 'feelslike', 'dew']].mean()

    # Tạo Figure và Axes
    fig, ax = plt.subplots(figsize=(20,8))

    # Vẽ các đường
    ax.plot(df_hourly_avg.index, df_hourly_avg['temp'], label='Temp', color='tomato')
    ax.plot(df_hourly_avg.index, df_hourly_avg['feelslike'], label='Feels Like', color='darkorange')
    ax.plot(df_hourly_avg.index, df_hourly_avg['dew'], label='Dew', color='peru')

    # Thiết lập tiêu đề và nhãn
    ax.set_title('Trung bình nhiệt độ theo giờ trong ngày')
    ax.set_xlabel('Giờ trong ngày')
    ax.set_ylabel('Nhiệt độ (°C)')
    ax.set_xticks(range(0, 24))
    ax.legend()
    ax.grid(True)

    # Tối ưu layout và trả về Figure
    fig.tight_layout()
    return fig


def plot_precipitation(df):
    # Tạo DataFrame đầy đủ 24 giờ
    full_hours = pd.DataFrame({'hour': range(24)})
    df_merged = pd.merge(full_hours, df, on='hour', how='left')

    # Gán nhãn x trục là giờ
    df_merged['time_label'] = df_merged['hour'].astype(str)

    # Tạo biểu đồ
    fig, ax1 = plt.subplots(figsize=(20, 8))

    # Cột lượng mưa
    bars = ax1.bar(df_merged['time_label'], df_merged['precip'], color='royalblue')
    ax1.set_ylabel('Lượng mưa (mm)', color='skyblue')
    ax1.set_xlabel('Giờ trong ngày')

    # Thêm nhãn loại mưa lên cột
    for bar, label in zip(bars, df_merged['preciptype'].fillna('')):
        height = bar.get_height()
        if pd.notna(label):
            ax1.text(bar.get_x() + bar.get_width() / 2, height + 0.002, label,
                     ha='center', va='bottom', fontsize=7, rotation=25)

    # Đường xác suất mưa
    ax2 = ax1.twinx()
    ax2.plot(df_merged['time_label'], df_merged['precipprob'], color='darkorange', marker='o')
    ax2.set_ylabel('Xác suất mưa (%)', color='orange')

    # Thiết lập chung
    plt.title('Biểu đồ lượng mưa và xác suất mưa theo giờ')
    plt.xticks(rotation=0)
    fig.tight_layout()

    return fig

def plot_snow_and_snowdepth(df):
    # Tạo đủ 24 giờ
    full_hours = pd.DataFrame({'hour': range(24)})
    df_merged = pd.merge(full_hours, df, on='hour', how='left')
    df_merged['time_label'] = df_merged['hour'].astype(str)

    fig, ax1 = plt.subplots(figsize=(20, 8))

    # Cột lượng tuyết
    bars = ax1.bar(df_merged['time_label'], df_merged['snow'], color='lightskyblue', label='Lượng tuyết (cm)')
    ax1.set_ylabel('Lượng tuyết (cm)', color='lightblue')
    ax1.set_xlabel('Giờ trong ngày')

    # Đường độ sâu tuyết
    ax2 = ax1.twinx()
    ax2.plot(df_merged['time_label'], df_merged['snowdepth'], color='deepskyblue', marker='o', label='Độ sâu tuyết (cm)')
    ax2.set_ylabel('Độ sâu tuyết (cm)', color='blue')

    # Tiêu đề, căn chỉnh
    plt.title('Biểu đồ lượng tuyết và độ sâu tuyết theo giờ')
    plt.xticks(rotation=0)
    fig.tight_layout()

    # Thêm chú thích
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    return fig

def plot_visibility_humidity_cloudcover(df):
    # Tạo DataFrame đủ 24 giờ
    full_hours = pd.DataFrame({'hour': range(24)})
    df_merged = pd.merge(full_hours, df, on='hour', how='left')
    df_merged['time_label'] = df_merged['hour'].astype(str)

    fig, ax1 = plt.subplots(figsize=(20, 8))

    # Cột: Tầm nhìn xa
    bars = ax1.bar(df_merged['time_label'], df_merged['visibility'], color='dimgray', label='Tầm nhìn xa (km)')
    ax1.set_ylabel('Tầm nhìn xa (km)', color='gray')
    ax1.set_xlabel('Giờ trong ngày')

    # Đường: Độ ẩm và mức độ mây
    ax2 = ax1.twinx()
    ax2.plot(df_merged['time_label'], df_merged['humidity'], color='seagreen', marker='o', label='Độ ẩm (%)')
    ax2.plot(df_merged['time_label'], df_merged['cloudcover'], color='mediumorchid', marker='s', label='Mức độ mây (%)')
    ax2.set_ylabel('Độ ẩm / Mức độ mây (%)')

    # Tiêu đề và định dạng
    plt.title('Tầm nhìn xa, độ ẩm và mức độ mây theo giờ')
    plt.xticks(rotation=0)
    fig.tight_layout()

    # Gộp chú thích từ cả hai trục
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    return fig

def degree_to_wind_direction_abbr(degree):
    directions = [
        'N', 'NNE', 'NE', 'ENE',
        'E', 'ESE', 'SE', 'SSE',
        'S', 'SSW', 'SW', 'WSW',
        'W', 'WNW', 'NW', 'NNW'
    ]
    idx = int((degree % 360) / 22.5 + 0.5) % 16
    return directions[idx]

def plot_wind_by_hour(df, direction_func):
    # Tạo DataFrame đủ 24 giờ
    full_hours = pd.DataFrame({'hour': range(24)})
    df_merged = pd.merge(full_hours, df, on='hour', how='left')
    df_merged['time_label'] = df_merged['hour'].astype(str)

    # Thêm cột tên hướng gió viết tắt
    df_merged['winddir_abbr'] = df_merged['winddir'].apply(direction_func)

    fig, ax1 = plt.subplots(figsize=(20, 8))

    # Cột: Hướng gió
    bars = ax1.bar(df_merged['time_label'], df_merged['winddir'], color='slategray', label='Hướng gió (°)')
    ax1.set_ylabel('Hướng gió (°)', color='skyblue')
    ax1.set_xlabel('Giờ trong ngày')

    # Ghi tên hướng gió trên đầu mỗi cột
    for bar, label in zip(bars, df_merged['winddir_abbr']):
        height = bar.get_height()
        if pd.notna(label):
            ax1.text(bar.get_x() + bar.get_width() / 2, height + 5, label,
                     ha='center', va='bottom', fontsize=9, color='blue')

    # Đường: Tốc độ gió và gió giật
    ax2 = ax1.twinx()
    ax2.plot(df_merged['time_label'], df_merged['windspeed'], color='orange', marker='o', label='Tốc độ gió (km/h)')
    ax2.plot(df_merged['time_label'], df_merged['windgust'], color='firebrick', marker='s', label='Gió giật (km/h)')
    ax2.set_ylabel('Tốc độ / Gió giật (km/h)')

    plt.title('Biểu đồ gió theo giờ')
    plt.xticks(rotation=0)
    fig.tight_layout()

    # Gộp legend từ cả hai trục
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    return fig  

if __name__ == "__main__":
    location = "Jakarta"
    weather = get_weather_data(location)

    if "days" in weather and "hours" in weather["days"][0]:

        df_hour = process_hour_weather_data(weather)
        df_process = preprocess_weather_df(df_hour)

        # plot_hourly_temperature_averages(df_process)
        # plot_precipitation(df_process)
        # plot_visibility_humidity_cloudcover(df_process)
        # plot_wind_by_hour(df_process, degree_to_wind_direction_abbr)

