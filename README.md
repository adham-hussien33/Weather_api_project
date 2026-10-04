# 🌤️ NYC Weather Data Application (Weather API Project)

A Python application for fetching, storing, and displaying historical weather conditions for **New York City** from **2015 until today**, as well as tracking daily 7-day weather forecasts.

---

## 📌 Project Overview

This project satisfies all requirements for **Practical Project 3.1 (Simple Weather App for New York City)**:
1. **Historical Weather Data**: Ingests NYC daily weather data starting from **2015-01-01** up to yesterday from the Open-Meteo Historical Archive API.
2. **7-Day Forecast Script**: Fetches the 7-day daily forecast and updates prediction records.
3. **Data Type Marking**: Classifies records as either:
   - `'A'`: Actual historical data (dates $\le$ today)
   - `'P'`: Prediction forecast data (dates > today)
4. **Automatic Overwrite**: Past prediction records (`'P'`) are automatically replaced by actual records (`'A'`) as time passes using SQLite primary key conflict handling.
5. **Database Storage**: Stores temperature, wind speed, wind direction, city, and data type inside an SQLite database (`weather_data.db`).

---

## 📂 File Structure

| File Name | Description |
|---|---|
| `db_setup.py` | Creates the SQLite database `weather_data.db` and the `weather` table. |
| `historical_weather.py` | Fetches historical NYC weather data from 2015 to today and saves it into the database. |
| `forecast_weather.py` | Fetches the 7-day forecast and updates current/future data in the database. |
| `kelw.py` | Quick API test script that queries live NYC weather parameters and displays them. |
| `weather_data.db` | SQLite database storing all actual and forecast weather records. |
| `README.md` | Comprehensive user and API testing documentation. |

---

## 🛠️ Prerequisites & Setup

### Requirements
- **Python 3.8+**
- `requests` library

### Installation
Open your terminal in the `weather_api_project` directory and install required packages:

```bash
py -m pip install requests
```

---

## 🚀 Steps to Run the Project

Follow these steps in order:

### Step 1: Initialize Database
Run `db_setup.py` to create the SQLite database file and table structure:

```bash
py db_setup.py
```
**Expected Output:**
```text
[OK] Database and table created successfully!
```

### Step 2: Fetch Historical Weather Data (2015 to Today)
Run `historical_weather.py` to ingest historical data from `2015-01-01` to yesterday:

```bash
py historical_weather.py
```
**Expected Output:**
```text
[INFO] Fetching historical weather data for NYC from 2015-01-01 to 2026-10-03...
[OK] Successfully processed and inserted 4294 historical weather records into database!

Sample Historical Records:
Date         | City       | Temp (C)   | Wind Speed | Wind Dir (deg) | Type 
---------------------------------------------------------------------------
2015-01-01   | New York   | -1.0       | 21.3       | 235            | A    
2015-01-02   | New York   | 2.3        | 19.9       | 250            | A    
...
```

### Step 3: Fetch & Update 7-Day Forecast
Run `forecast_weather.py` to pull the latest 7-day prediction data:

```bash
py forecast_weather.py
```
**Expected Output:**
```text
[INFO] Fetching 7-day weather forecast for NYC...

7-Day Forecast Data:
Date         | City       | Temp (C)   | Wind Speed | Wind Dir (deg) | Type 
---------------------------------------------------------------------------
2026-10-04   | New York   | 14.95      | 16.4       | 58             | A    
2026-10-05   | New York   | 14.0       | 28.7       | 309            | P    
2026-10-06   | New York   | 11.85      | 17.9       | 312            | P    
...
[OK] Forecast data fetched, displayed, and updated in database successfully!
```

---

## 🧪 Steps to Test the APIs

You can test the weather APIs using **3 different methods**:

### Method 1: Using `kelw.py` (Quick Script Test)
Run the dedicated test script `kelw.py` to verify that the Open-Meteo API is responsive and returns live current weather data:

```bash
py kelw.py
```
**Expected Output:**
```text
Data fetched successfully!
Current Temperature in New York: 15.2 °C
Wind Speed: 16.4 km/h
```

---

### Method 2: Testing API Endpoints Directly (Browser or Curl)

#### 1. Test Historical Archive API Endpoint
Open the following URL in your web browser or run via `curl`:
```text
https://archive-api.open-meteo.com/v1/archive?latitude=40.7128&longitude=-74.0060&start_date=2023-01-01&end_date=2023-01-05&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_direction_10m_dominant
```
**What to check:**
- HTTP status code `200 OK`
- JSON structure contains key `"daily"` with arrays for `"time"`, `"temperature_2m_max"`, etc.

#### 2. Test 7-Day Forecast API Endpoint
Open the following URL in your web browser or run via `curl`:
```text
https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_direction_10m_dominant&timezone=auto
```
**What to check:**
- Contains array of 7 forecast dates.

---

### Method 3: Programmatic API Testing with Python `requests`

You can test API error handling and response status codes directly in Python:

```python
import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.0060&daily=temperature_2m_max"

response = requests.get(url)
print("Status Code:", response.status_code) # Should print 200

if response.status_code == 200:
    data = response.json()
    print("API Response OK! Daily dates:", data['daily']['time'])
else:
    print("API Error:", response.status_code)
```

---

### Method 4: Verify Database Data Insertion
Run this command to check how many Actual (`'A'`) vs Prediction (`'P'`) rows are saved in your SQLite database:

```bash
py -c "import sqlite3; conn = sqlite3.connect('weather_data.db'); c = conn.cursor(); c.execute('SELECT COUNT(*), data_type FROM weather GROUP BY data_type'); print(c.fetchall())"
```

---

## 📊 Database Schema

```sql
CREATE TABLE IF NOT EXISTS weather (
    date TEXT PRIMARY KEY,
    city TEXT,
    temperature REAL,
    wind_speed REAL,
    wind_direction REAL,
    data_type TEXT CHECK(data_type IN ('A', 'P'))
);
```

| Field | Data Type | Description |
|---|---|---|
| `date` | `TEXT` (Primary Key) | Date string formatted as `YYYY-MM-DD`. |
| `city` | `TEXT` | Name of the target city (`"New York"`). |
| `temperature` | `REAL` | Calculated mean temperature (°C). |
| `wind_speed` | `REAL` | Maximum daily wind speed (km/h). |
| `wind_direction` | `REAL` | Dominant wind direction in degrees (°). |
| `data_type` | `TEXT` | Data classification: `'A'` (Actual) or `'P'` (Prediction). |
