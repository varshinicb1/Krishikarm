"""
Kisan-Eye V6 — Satellite Data Advisor
Fetches real satellite and weather data for a farmer's location,
generates data-backed agricultural advice.
"""

import aiohttp
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


async def fetch_weather(lat, lon):
    """Fetch current weather + 7-day forecast from Open-Meteo (free, no API key)."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,et0_fao_evapotranspiration",
        "hourly": "soil_moisture_0_to_1cm",
        "timezone": "Asia/Kolkata",
        "forecast_days": 7
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return {
                        "current": data.get("current", {}),
                        "daily": data.get("daily", {}),
                        "hourly": data.get("hourly", {}),
                    }
    except Exception as e:
        logger.error(f"Weather fetch failed: {e}")
    return None


async def fetch_nasa_power(lat, lon, days_back=30):
    """Fetch NASA POWER data (solar radiation, temperature, humidity)."""
    end = datetime.now()
    start = end - timedelta(days=days_back)
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN,T2M,T2M_MAX,T2M_MIN,RH2M,PRECTOTCORR",
        "community": "ag",
        "longitude": lon,
        "latitude": lat,
        "start": start.strftime("%Y%m%d"),
        "end": end.strftime("%Y%m%d"),
        "format": "json"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("properties", {}).get("parameter", {})
    except Exception as e:
        logger.error(f"NASA POWER fetch failed: {e}")
    return None


def compute_ndvi_estimate(soil_moisture, temperature, humidity, rainfall):
    """Estimate NDVI from available parameters (when no satellite imagery)."""
    # Simplified estimation based on growing conditions
    sm_score = min(1, soil_moisture / 0.4) if soil_moisture else 0.5
    temp_score = max(0, 1 - abs(temperature - 27) / 20) if temperature else 0.5
    humid_score = min(1, humidity / 80) if humidity else 0.5
    rain_score = min(1, rainfall / 50) if rainfall else 0.5

    ndvi = 0.15 + 0.65 * (sm_score * 0.35 + temp_score * 0.25 + humid_score * 0.2 + rain_score * 0.2)
    return round(ndvi, 3)


async def get_farm_intelligence(lat, lon):
    """Complete farm intelligence package for a location."""
    weather = await fetch_weather(lat, lon)
    nasa = await fetch_nasa_power(lat, lon, days_back=7)

    result = {
        "location": {"lat": lat, "lon": lon},
        "timestamp": datetime.now().isoformat(),
    }

    if weather:
        cur = weather.get("current", {})
        daily = weather.get("daily", {})
        hourly = weather.get("hourly", {})

        sm_values = hourly.get("soil_moisture_0_to_1cm", [])
        latest_sm = sm_values[-1] if sm_values else None

        result["temperature"] = cur.get("temperature_2m")
        result["humidity"] = cur.get("relative_humidity_2m")
        result["wind_speed"] = cur.get("wind_speed_10m")
        result["soil_moisture"] = latest_sm

        # 7-day rainfall total
        precip = daily.get("precipitation_sum", [])
        result["rainfall_7d"] = round(sum(p for p in precip if p), 1)

        # ET₀ for irrigation
        et0_values = daily.get("et0_fao_evapotranspiration", [])
        result["et0"] = round(et0_values[0], 1) if et0_values else None

        # Forecast text
        if daily.get("temperature_2m_max"):
            result["forecast_3d"] = ", ".join([
                f"{round(daily['temperature_2m_max'][i])}°/{round(daily['temperature_2m_min'][i])}° {'🌧' if (daily.get('precipitation_sum') or [0]*7)[i] > 1 else '☀️'}"
                for i in range(min(3, len(daily['temperature_2m_max'])))
            ])
        result["rain_expected"] = any((p or 0) > 2 for p in (daily.get("precipitation_sum", [])[:3]))

    if nasa:
        solar = list(nasa.get("ALLSKY_SFC_SW_DWN", {}).values())
        valid_solar = [s for s in solar if s > -990]
        result["solar"] = round(sum(valid_solar) / len(valid_solar), 1) if valid_solar else None

    # Estimate NDVI
    result["ndvi"] = compute_ndvi_estimate(
        result.get("soil_moisture"), result.get("temperature"),
        result.get("humidity"), result.get("rainfall_7d", 0)
    )

    # Crop health label
    ndvi = result["ndvi"]
    if ndvi > 0.6: result["ndvi_label"] = "Excellent"
    elif ndvi > 0.4: result["ndvi_label"] = "Good"
    elif ndvi > 0.25: result["ndvi_label"] = "Fair"
    else: result["ndvi_label"] = "Poor"

    # Irrigation decision
    sm = result.get("soil_moisture")
    rain_exp = result.get("rain_expected", False)
    if rain_exp:
        result["irrigate_decision"] = "NO — Rain expected"
    elif sm and sm > 0.35:
        result["irrigate_decision"] = "NO — Soil moist"
    elif sm and sm < 0.15:
        result["irrigate_decision"] = "YES — Urgent!"
    else:
        result["irrigate_decision"] = "Check by evening"

    return result
