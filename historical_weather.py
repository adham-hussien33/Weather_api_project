import sqlite3
import requests
from datetime import datetime, timedelta

def fetch_and_store_historical_data():
    latitude = 40.7128
    longitude = -74.0060
    city_name = "New York"
    
    start_date = "2015-01-01"
    end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_direction_10m_dominant"
    
    print(f"[INFO] Fetching historical weather data for NYC from {start_date} to {end_date}...")
    
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
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather (
                    date TEXT PRIMARY KEY,
                    city TEXT,
                    temperature REAL,
                    wind_speed REAL,
                    wind_direction REAL,
                    data_type TEXT CHECK(data_type IN ('A', 'P'))
                )
            """)
            
            records_count = 0
            for i in range(len(times)):
                date_str = times[i]
                t_max = temps_max[i] if i < len(temps_max) else None
                t_min = temps_min[i] if i < len(temps_min) else None
                
                if t_max is not None and t_min is not None:
                    temperature = round((t_max + t_min) / 2, 2)
                else:
                    temperature = 0.0
                    
                wind_speed = round(winds[i], 2) if i < len(winds) and winds[i] is not None else 0.0
                wind_direction = round(wind_dirs[i], 2) if i < len(wind_dirs) and wind_dirs[i] is not None else 0.0
                
                cursor.execute("""
                    INSERT OR REPLACE INTO weather (date, city, temperature, wind_speed, wind_direction, data_type)
                    VALUES (?, ?, ?, ?, ?, 'A')
                """, (date_str, city_name, temperature, wind_speed, wind_direction))
                records_count += 1
                
            conn.commit()
            conn.close()
            print(f"[OK] Successfully processed and inserted {records_count} historical weather records into database!")
            print("\nSample Historical Records:")
            print(f"{'Date':<12} | {'City':<10} | {'Temp (C)':<10} | {'Wind Speed':<10} | {'Wind Dir (deg)':<14} | {'Type':<5}")
            print("-" * 75)
            for i in list(range(min(5, len(times)))) + list(range(max(0, len(times)-5), len(times))):
                if i < len(times):
                    t_max = temps_max[i] if i < len(temps_max) else 0
                    t_min = temps_min[i] if i < len(temps_min) else 0
                    temp = round((t_max + t_min) / 2, 2) if t_max and t_min else 0.0
                    w_spd = round(winds[i], 2) if i < len(winds) and winds[i] else 0.0
                    w_dir = round(wind_dirs[i], 2) if i < len(wind_dirs) and wind_dirs[i] else 0.0
                    print(f"{times[i]:<12} | {city_name:<10} | {temp:<10} | {w_spd:<10} | {w_dir:<14} | {'A':<5}")
                if i == 4 and len(times) > 10:
                    print("...")
        else:
            print("Failed to fetch data, status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    fetch_and_store_historical_data()