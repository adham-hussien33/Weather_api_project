import sqlite3
import requests
from datetime import datetime

def update_and_fetch_forecast():
    latitude = 40.7128
    longitude = -74.0060
    city_name = "New York"
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_direction_10m_dominant&timezone=auto"
    
    print("[INFO] Fetching 7-day weather forecast for NYC...")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            daily = data.get("daily", {})
            
            times = daily.get("time", [])
            temps_max = daily.get("temperature_2m_max", [])
            temps_min = daily.get("temperature_2m_min", [])
            winds = daily.get("wind_speed_10m_max", [])
            wind_dirs = daily.get("wind_direction_10m_dominant", [])
            
            conn = sqlite3.connect("weather_data.db")
            cursor = conn.cursor()
            
            today_str = datetime.now().strftime("%Y-%m-%d")
            
            print("\n7-Day Forecast Data:")
            print(f"{'Date':<12} | {'City':<10} | {'Temp (C)':<10} | {'Wind Speed':<10} | {'Wind Dir (deg)':<14} | {'Type':<5}")
            print("-" * 75)
            
            for i in range(len(times)):
                date_str = times[i]
                t_max = temps_max[i]
                t_min = temps_min[i]
                temperature = round((t_max + t_min) / 2, 2) if t_max is not None and t_min is not None else 0.0
                wind_speed = round(winds[i], 2) if winds[i] is not None else 0.0
                wind_direction = round(wind_dirs[i], 2) if wind_dirs[i] is not None else 0.0
                
                data_type = 'A' if date_str <= today_str else 'P'
                
                cursor.execute("""
                    INSERT OR REPLACE INTO weather (date, city, temperature, wind_speed, wind_direction, data_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (date_str, city_name, temperature, wind_speed, wind_direction, data_type))
                
                print(f"{date_str:<12} | {city_name:<10} | {temperature:<10} | {wind_speed:<10} | {wind_direction:<14} | {data_type:<5}")
                
            conn.commit()
            conn.close()
            print("\n[OK] Forecast data fetched, displayed, and updated in database successfully!")
        else:
            print("Failed to fetch forecast, status code:", response.status_code)
    except Exception as e:
        print("An error occurred while fetching forecast:", e)

if __name__ == "__main__":
    update_and_fetch_forecast()