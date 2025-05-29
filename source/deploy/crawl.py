import urllib.request
import urllib.parse
import json
import sys
import pandas as pd

def get_weather_data(location):
    encoded_location = urllib.parse.quote(location)
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{encoded_location}/today?unitGroup=metric&include=days%2Chours%2Ccurrent&key=T85U8SM5VEPNGZTWX9MLTRLCK&contentType=json"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            return data
    except urllib.error.HTTPError as e:
        error_info = e.read().decode()
        print('HTTP Error:', e.code, error_info)
        sys.exit()
    except urllib.error.URLError as e:
        print('URL Error:', e.reason)
        sys.exit()

def process_info_weather_data(weather):
    
    info_weather_data = {
        "queryCost": weather["queryCost"],
        "latitude": weather["latitude"],
        "longitude": weather["longitude"],
        "resolvedAddress": weather["resolvedAddress"],
        "address": weather["address"],
        "timezone": weather["timezone"],
        "timezone_offset": weather["tzoffset"] 
    }

    df_info = pd.DataFrame([info_weather_data])
    return df_info

def process_day_weather_data(weather):
    # Kiểm tra nếu "days" có dữ liệu
    if not weather.get("days"):
        return pd.DataFrame()  # Nếu không có dữ liệu, trả về DataFrame rỗng

    day_data = weather["days"][0]  # Lấy dữ liệu ngày đầu tiên từ danh sách "days"
    
    # Xử lý các dữ liệu ngày
    day_weather_data = {
        "datetime": day_data.get("datetime", None),
        "datetimeEpoch": day_data.get("datetimeEpoch", None),
        "tempmax": day_data.get("tempmax", None),
        "tempmin": day_data.get("tempmin", None),
        "temp": day_data.get("temp", None),
        "feelslikemax": day_data.get("feelslikemax", None),
        "feelslikemin": day_data.get("feelslikemin", None),
        "feelslike": day_data.get("feelslike", None),
        "dew": day_data.get("dew", None),
        "humidity": day_data.get("humidity", None),
        "precip": day_data.get("precip", None),
        "precipprob": day_data.get("precipprob", None),
        "precipcover": day_data.get("precipcover", None),
        "preciptype": ",".join(day_data["preciptype"]) if day_data.get("preciptype") else None,
        "snow": day_data.get("snow", None),
        "snowdepth": day_data.get("snowdepth", None),
        "windgust": day_data.get("windgust", None),
        "windspeed": day_data.get("windspeed", None),
        "winddir": day_data.get("winddir", None),
        "sealevelpressure": day_data.get("pressure", None),
        "cloudcover": day_data.get("cloudcover", None),
        "visibility": day_data.get("visibility", None),
        "solarradiation": day_data.get("solarradiation", None),
        "solarenergy": day_data.get("solarenergy", None),
        "uvindex": day_data.get("uvindex", None),
        "severerisk": day_data.get("severerisk", None),
        "sunrise": day_data.get("sunrise", None),
        "sunriseEpoch": day_data.get("sunriseEpoch", None),
        "sunset": day_data.get("sunset", None),
        "sunsetEpoch": day_data.get("sunsetEpoch", None),
        "moonphase": day_data.get("moonphase", None),
        "conditions": day_data.get("conditions", None),
        "description": day_data.get("description", None),
        "icon": day_data.get("icon", None),
        "stations": ",".join(day_data["stations"]) if day_data.get("stations") else None
    }

    df_day = pd.DataFrame([day_weather_data])
    return df_day

def process_hour_weather_data(weather):
    hours_list = weather["days"][0]["hours"]  # Truy cập danh sách 24 giờ

    processed_hours = []

    for hour in hours_list:
        hour_data = {
            "datetime": hour["datetime"],
            "datetimeEpoch": hour["datetimeEpoch"],
            "temp": hour["temp"],
            "feelslike": hour["feelslike"],
            "dew": hour["dew"],
            "humidity": hour["humidity"],
            "precip": hour["precip"],
            "precipprob": hour["precipprob"],
            "preciptype": ",".join(hour["preciptype"]) if hour.get("preciptype") else None,
            "snow": hour["snow"],
            "snowdepth": hour["snowdepth"],
            "windgust": hour["windgust"],
            "windspeed": hour["windspeed"],
            "winddir": hour["winddir"],
            "sealevelpressure": hour["pressure"],
            "cloudcover": hour["cloudcover"],
            "visibility": hour["visibility"],
            "solarradiation": hour["solarradiation"],
            "solarenergy": hour["solarenergy"],
            "uvindex": hour["uvindex"],
            "severerisk": hour["severerisk"],
            "conditions": hour["conditions"],
            "icon": hour["icon"],
            "stations": ",".join(hour["stations"]) if hour.get("stations") else None
        }

        processed_hours.append(hour_data)
        df_hour = pd.DataFrame(processed_hours)

    return df_hour

def process_current_weather_data(weather):
    # Kiểm tra nếu "currentConditions" có dữ liệu
    if not weather.get("currentConditions"):
        return pd.DataFrame()  # Nếu không có dữ liệu, trả về DataFrame rỗng

    current_conditions = weather["currentConditions"]
    
    current_weather_data = {
        "datetime": current_conditions.get("datetime", None),
        "datetimeEpoch": current_conditions.get("datetimeEpoch", None),
        "temp": current_conditions.get("temp", None),
        "feelslike": current_conditions.get("feelslike", None),
        "dew": current_conditions.get("dew", None),
        "humidity": current_conditions.get("humidity", None),
        "precip": current_conditions.get("precip", None),
        "precipprob": current_conditions.get("precipprob", None),
        # Kiểm tra nếu preciptype là null hoặc không có dữ liệu
        "preciptype": ",".join(current_conditions.get("preciptype", [])) if current_conditions.get("preciptype") else None,
        "snow": current_conditions.get("snow", None),
        "snowdepth": current_conditions.get("snowdepth", None),
        "windgust": current_conditions.get("windgust", None),
        "windspeed": current_conditions.get("windspeed", None),
        "winddir": current_conditions.get("winddir", None),
        "sealevelpressure": current_conditions.get("pressure", None),
        "cloudcover": current_conditions.get("cloudcover", None),
        "visibility": current_conditions.get("visibility", None),
        "solarradiation": current_conditions.get("solarradiation", None),
        "solarenergy": current_conditions.get("solarenergy", None),
        "uvindex": current_conditions.get("uvindex", None),
        "severerisk": current_conditions.get("severerisk", None),
        "sunrise": current_conditions.get("sunrise", None),
        "sunriseEpoch": current_conditions.get("sunriseEpoch", None),
        "sunset": current_conditions.get("sunset", None),
        "sunsetEpoch": current_conditions.get("sunsetEpoch", None),
        "moonphase": current_conditions.get("moonphase", None),
        "conditions": current_conditions.get("conditions", None),
        "icon": current_conditions.get("icon", None),
        # Kiểm tra nếu stations là danh sách rỗng hoặc không có
        "stations": ",".join(current_conditions.get("stations", [])) if current_conditions.get("stations") else None
    }

    df_current = pd.DataFrame([current_weather_data])
    return df_current

def process_station_info_data(weather):
    stations_info = weather.get("stations", {})

    if not stations_info:
        return pd.DataFrame()

    station_list = []
    for info in stations_info.values():
        station_data = {
            "id": info.get("id"),
            "name": info.get("name"),
            "latitude": info.get("latitude"),
            "longitude": info.get("longitude"),
            "distance": info.get("distance"),
            "useCount": info.get("useCount"),
            "quality": info.get("quality"),
            "contribution": info.get("contribution")
        }
        station_list.append(station_data)

    df_station= pd.DataFrame(station_list)
    return df_station

if __name__ == "__main__":
    location = "Jakarta"
    weather = get_weather_data(location)
    
    # Kiểm tra kết quả của hàm get_weather_data
    print("Weather Data:")
    print(json.dumps(weather, indent=4))

    # Kiểm tra các hàm xử lý dữ liệu
    df_info = process_info_weather_data(weather)
    print("\nInfo Weather Data:")
    print(df_info)

    if "days" in weather:
        df_day = process_day_weather_data(weather)
        print("\nDay Weather Data:")
        print(df_day)

    if "days" in weather and "hours" in weather["days"][0]:
        df_hour = process_hour_weather_data(weather)
        print("\nHour Weather Data:")
        print(df_hour)
        df_hour.to_csv("1hour_weather_data.csv", index=False)

    if "currentConditions" in weather:
        df_current = process_current_weather_data(weather)
        print("\nCurrent Weather Data:")
        print(df_current)

    df_station = process_station_info_data(weather)
    print("\nStation Info Data:")
    print(df_station)

