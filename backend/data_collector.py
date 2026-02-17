"""
Maximum Satellite Data Collector — All Free, No-Auth APIs
═════════════════════════════════════════════════════════
Pulls from 6 public APIs for 127 Indian districts × 2 years.
No account creation needed. Fully automated.

Sources:
  1. NASA POWER — temp, humidity, precip, solar, wind, pressure, cloud, dewpoint
  2. Open-Meteo Historical Weather — daily weather + ET₀
  3. Open-Meteo Soil — soil temp & moisture at 4 depths
  4. Open-Meteo Air Quality — PM2.5, PM10, aerosol, dust, UV
  5. Open-Meteo Elevation — terrain elevation
  6. SoilGrids (ISRIC) — soil organic carbon, clay, sand, pH
"""

import aiohttp, asyncio, json, math, logging, time
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

# ═════════════════════════════════════════
# 127 INDIAN AGRICULTURAL DISTRICTS
# ═════════════════════════════════════════
DISTRICTS = [
    # Uttar Pradesh
    {"n":"Varanasi","s":"UP","lat":25.32,"lon":83.01,"c":["rice","wheat"],"i":"canal"},
    {"n":"Lucknow","s":"UP","lat":26.85,"lon":80.95,"c":["wheat","rice"],"i":"canal"},
    {"n":"Allahabad","s":"UP","lat":25.43,"lon":81.85,"c":["rice","wheat"],"i":"canal"},
    {"n":"Gorakhpur","s":"UP","lat":26.76,"lon":83.37,"c":["rice","sugarcane"],"i":"canal"},
    {"n":"Agra","s":"UP","lat":27.18,"lon":78.02,"c":["wheat","mustard"],"i":"borewell"},
    {"n":"Meerut","s":"UP","lat":28.98,"lon":77.71,"c":["sugarcane","wheat"],"i":"canal"},
    {"n":"Bareilly","s":"UP","lat":28.37,"lon":79.42,"c":["wheat","rice"],"i":"borewell"},
    {"n":"Sultanpur","s":"UP","lat":26.26,"lon":82.07,"c":["rice","wheat"],"i":"rainfed"},
    {"n":"Jhansi","s":"UP","lat":25.45,"lon":78.57,"c":["wheat","gram"],"i":"rainfed"},
    {"n":"Faizabad","s":"UP","lat":26.77,"lon":82.14,"c":["rice","wheat"],"i":"canal"},
    # Punjab
    {"n":"Ludhiana","s":"PB","lat":30.90,"lon":75.86,"c":["wheat","rice"],"i":"canal"},
    {"n":"Amritsar","s":"PB","lat":31.63,"lon":74.87,"c":["wheat","rice"],"i":"canal"},
    {"n":"Bathinda","s":"PB","lat":30.21,"lon":74.96,"c":["cotton","wheat"],"i":"canal"},
    {"n":"Sangrur","s":"PB","lat":30.25,"lon":75.84,"c":["wheat","rice"],"i":"canal"},
    {"n":"Patiala","s":"PB","lat":30.34,"lon":76.39,"c":["wheat","rice"],"i":"canal"},
    {"n":"Firozpur","s":"PB","lat":30.93,"lon":74.61,"c":["wheat","rice"],"i":"canal"},
    # Haryana
    {"n":"Karnal","s":"HR","lat":29.69,"lon":76.98,"c":["wheat","rice"],"i":"canal"},
    {"n":"Hisar","s":"HR","lat":29.15,"lon":75.72,"c":["cotton","wheat"],"i":"canal"},
    {"n":"Sirsa","s":"HR","lat":29.53,"lon":75.03,"c":["cotton","wheat"],"i":"canal"},
    {"n":"Rohtak","s":"HR","lat":28.89,"lon":76.57,"c":["wheat","bajra"],"i":"canal"},
    # Maharashtra
    {"n":"Nagpur","s":"MH","lat":21.15,"lon":79.09,"c":["cotton","soybean"],"i":"rainfed"},
    {"n":"Nashik","s":"MH","lat":20.00,"lon":73.79,"c":["grapes","onion"],"i":"drip"},
    {"n":"Pune","s":"MH","lat":18.52,"lon":73.86,"c":["sugarcane","wheat"],"i":"canal"},
    {"n":"Ahmednagar","s":"MH","lat":19.09,"lon":74.74,"c":["sugarcane","cotton"],"i":"canal"},
    {"n":"Solapur","s":"MH","lat":17.66,"lon":75.91,"c":["sugarcane","jowar"],"i":"rainfed"},
    {"n":"Aurangabad","s":"MH","lat":19.88,"lon":75.34,"c":["cotton","soybean"],"i":"rainfed"},
    {"n":"Yavatmal","s":"MH","lat":20.39,"lon":78.13,"c":["cotton","soybean"],"i":"rainfed"},
    {"n":"Amravati","s":"MH","lat":20.93,"lon":77.75,"c":["cotton","soybean"],"i":"rainfed"},
    {"n":"Jalgaon","s":"MH","lat":21.01,"lon":75.57,"c":["banana","cotton"],"i":"drip"},
    {"n":"Kolhapur","s":"MH","lat":16.70,"lon":74.24,"c":["sugarcane","rice"],"i":"canal"},
    # Madhya Pradesh
    {"n":"Indore","s":"MP","lat":22.72,"lon":75.86,"c":["soybean","wheat"],"i":"rainfed"},
    {"n":"Bhopal","s":"MP","lat":23.26,"lon":77.41,"c":["wheat","soybean"],"i":"borewell"},
    {"n":"Jabalpur","s":"MP","lat":23.18,"lon":79.95,"c":["rice","wheat"],"i":"canal"},
    {"n":"Ujjain","s":"MP","lat":23.18,"lon":75.77,"c":["wheat","gram"],"i":"borewell"},
    {"n":"Sagar","s":"MP","lat":23.84,"lon":78.74,"c":["wheat","gram"],"i":"rainfed"},
    {"n":"Rewa","s":"MP","lat":24.53,"lon":81.30,"c":["rice","wheat"],"i":"rainfed"},
    {"n":"Gwalior","s":"MP","lat":26.22,"lon":78.18,"c":["wheat","mustard"],"i":"canal"},
    # Rajasthan
    {"n":"Jaipur","s":"RJ","lat":26.91,"lon":75.79,"c":["wheat","mustard"],"i":"borewell"},
    {"n":"Jodhpur","s":"RJ","lat":26.29,"lon":73.02,"c":["bajra","guar"],"i":"rainfed"},
    {"n":"Kota","s":"RJ","lat":25.18,"lon":75.86,"c":["soybean","wheat"],"i":"canal"},
    {"n":"Bikaner","s":"RJ","lat":28.02,"lon":73.31,"c":["bajra","mustard"],"i":"rainfed"},
    {"n":"Udaipur","s":"RJ","lat":24.58,"lon":73.68,"c":["maize","wheat"],"i":"rainfed"},
    {"n":"Alwar","s":"RJ","lat":27.56,"lon":76.63,"c":["wheat","mustard"],"i":"borewell"},
    {"n":"Barmer","s":"RJ","lat":25.75,"lon":71.39,"c":["bajra","guar"],"i":"rainfed"},
    # Gujarat
    {"n":"Ahmedabad","s":"GJ","lat":23.02,"lon":72.57,"c":["cotton","wheat"],"i":"borewell"},
    {"n":"Rajkot","s":"GJ","lat":22.30,"lon":70.80,"c":["groundnut","cotton"],"i":"borewell"},
    {"n":"Junagadh","s":"GJ","lat":21.52,"lon":70.46,"c":["groundnut","cotton"],"i":"borewell"},
    {"n":"Surat","s":"GJ","lat":21.17,"lon":72.83,"c":["sugarcane","cotton"],"i":"canal"},
    {"n":"Bhavnagar","s":"GJ","lat":21.76,"lon":72.15,"c":["cotton","groundnut"],"i":"rainfed"},
    {"n":"Banaskantha","s":"GJ","lat":24.17,"lon":72.43,"c":["potato","mustard"],"i":"borewell"},
    # Karnataka
    {"n":"Belgaum","s":"KA","lat":15.85,"lon":74.50,"c":["sugarcane","jowar"],"i":"canal"},
    {"n":"Dharwad","s":"KA","lat":15.46,"lon":75.01,"c":["cotton","jowar"],"i":"rainfed"},
    {"n":"Mysuru","s":"KA","lat":12.30,"lon":76.66,"c":["rice","ragi"],"i":"canal"},
    {"n":"Shimoga","s":"KA","lat":13.93,"lon":75.57,"c":["rice","areca"],"i":"canal"},
    {"n":"Gulbarga","s":"KA","lat":17.33,"lon":76.83,"c":["jowar","gram"],"i":"rainfed"},
    {"n":"Bellary","s":"KA","lat":15.14,"lon":76.92,"c":["rice","groundnut"],"i":"canal"},
    {"n":"Raichur","s":"KA","lat":16.20,"lon":77.36,"c":["rice","cotton"],"i":"canal"},
    # Andhra Pradesh + Telangana
    {"n":"Guntur","s":"AP","lat":16.31,"lon":80.44,"c":["rice","cotton"],"i":"canal"},
    {"n":"Krishna","s":"AP","lat":16.57,"lon":80.36,"c":["rice","sugarcane"],"i":"canal"},
    {"n":"Kurnool","s":"AP","lat":15.83,"lon":78.05,"c":["groundnut","cotton"],"i":"rainfed"},
    {"n":"Anantapur","s":"AP","lat":14.68,"lon":77.60,"c":["groundnut","rice"],"i":"rainfed"},
    {"n":"Nellore","s":"AP","lat":14.45,"lon":79.99,"c":["rice","sugarcane"],"i":"canal"},
    {"n":"Warangal","s":"TS","lat":17.97,"lon":79.60,"c":["rice","cotton"],"i":"borewell"},
    {"n":"Nizamabad","s":"TS","lat":18.67,"lon":78.09,"c":["rice","turmeric"],"i":"canal"},
    {"n":"Karimnagar","s":"TS","lat":18.44,"lon":79.13,"c":["rice","cotton"],"i":"borewell"},
    {"n":"Medak","s":"TS","lat":18.05,"lon":78.26,"c":["rice","maize"],"i":"borewell"},
    # Tamil Nadu
    {"n":"Thanjavur","s":"TN","lat":10.79,"lon":79.14,"c":["rice","banana"],"i":"canal"},
    {"n":"Coimbatore","s":"TN","lat":11.00,"lon":76.96,"c":["cotton","coconut"],"i":"borewell"},
    {"n":"Madurai","s":"TN","lat":9.92,"lon":78.12,"c":["rice","cotton"],"i":"canal"},
    {"n":"Salem","s":"TN","lat":11.65,"lon":78.16,"c":["rice","sugarcane"],"i":"borewell"},
    {"n":"Tiruchirapalli","s":"TN","lat":10.79,"lon":78.69,"c":["rice","groundnut"],"i":"canal"},
    {"n":"Erode","s":"TN","lat":11.34,"lon":77.72,"c":["turmeric","sugarcane"],"i":"borewell"},
    # Kerala
    {"n":"Thrissur","s":"KL","lat":10.53,"lon":76.21,"c":["rice","coconut"],"i":"rainfed"},
    {"n":"Palakkad","s":"KL","lat":10.78,"lon":76.65,"c":["rice","coconut"],"i":"canal"},
    {"n":"Wayanad","s":"KL","lat":11.60,"lon":76.08,"c":["coffee","pepper"],"i":"rainfed"},
    # West Bengal
    {"n":"Burdwan","s":"WB","lat":23.23,"lon":87.86,"c":["rice","wheat"],"i":"canal"},
    {"n":"Hooghly","s":"WB","lat":22.91,"lon":88.39,"c":["rice","potato"],"i":"canal"},
    {"n":"Murshidabad","s":"WB","lat":24.18,"lon":88.27,"c":["rice","jute"],"i":"canal"},
    {"n":"Nadia","s":"WB","lat":23.47,"lon":88.56,"c":["rice","jute"],"i":"canal"},
    {"n":"Midnapore","s":"WB","lat":22.42,"lon":87.32,"c":["rice","vegetables"],"i":"rainfed"},
    {"n":"Malda","s":"WB","lat":25.01,"lon":88.14,"c":["rice","mango"],"i":"rainfed"},
    # Bihar
    {"n":"Patna","s":"BR","lat":25.61,"lon":85.14,"c":["rice","wheat"],"i":"canal"},
    {"n":"Muzaffarpur","s":"BR","lat":26.12,"lon":85.39,"c":["rice","litchi"],"i":"canal"},
    {"n":"Bhagalpur","s":"BR","lat":25.25,"lon":86.98,"c":["rice","wheat"],"i":"canal"},
    {"n":"Darbhanga","s":"BR","lat":26.17,"lon":85.90,"c":["rice","maize"],"i":"rainfed"},
    {"n":"Gaya","s":"BR","lat":24.80,"lon":84.99,"c":["rice","wheat"],"i":"rainfed"},
    {"n":"Samastipur","s":"BR","lat":25.86,"lon":85.78,"c":["rice","wheat"],"i":"canal"},
    # Odisha
    {"n":"Cuttack","s":"OR","lat":20.46,"lon":85.88,"c":["rice","vegetables"],"i":"canal"},
    {"n":"Sambalpur","s":"OR","lat":21.47,"lon":83.97,"c":["rice","cotton"],"i":"rainfed"},
    {"n":"Balasore","s":"OR","lat":21.49,"lon":86.93,"c":["rice","jute"],"i":"canal"},
    {"n":"Puri","s":"OR","lat":19.81,"lon":85.83,"c":["rice","coconut"],"i":"canal"},
    # Assam
    {"n":"Nagaon","s":"AS","lat":26.35,"lon":92.69,"c":["rice","tea"],"i":"rainfed"},
    {"n":"Jorhat","s":"AS","lat":26.76,"lon":94.22,"c":["tea","rice"],"i":"rainfed"},
    {"n":"Dibrugarh","s":"AS","lat":27.47,"lon":94.91,"c":["tea","rice"],"i":"rainfed"},
    # Jharkhand
    {"n":"Ranchi","s":"JH","lat":23.34,"lon":85.31,"c":["rice","vegetables"],"i":"rainfed"},
    {"n":"Dhanbad","s":"JH","lat":23.80,"lon":86.43,"c":["rice","wheat"],"i":"rainfed"},
    # Chhattisgarh
    {"n":"Raipur","s":"CG","lat":21.25,"lon":81.63,"c":["rice","wheat"],"i":"canal"},
    {"n":"Bilaspur","s":"CG","lat":22.08,"lon":82.15,"c":["rice","maize"],"i":"rainfed"},
    {"n":"Durg","s":"CG","lat":21.19,"lon":81.28,"c":["rice","wheat"],"i":"canal"},
    # Uttarakhand
    {"n":"Dehradun","s":"UK","lat":30.32,"lon":78.03,"c":["rice","wheat"],"i":"canal"},
    {"n":"Haridwar","s":"UK","lat":29.95,"lon":78.16,"c":["sugarcane","wheat"],"i":"canal"},
    # Himachal Pradesh
    {"n":"Shimla","s":"HP","lat":31.10,"lon":77.17,"c":["apple","wheat"],"i":"rainfed"},
    {"n":"Kangra","s":"HP","lat":32.10,"lon":76.27,"c":["rice","wheat"],"i":"rainfed"},
    # Tripura / Manipur / Meghalaya
    {"n":"Agartala","s":"TR","lat":23.83,"lon":91.27,"c":["rice","rubber"],"i":"rainfed"},
    {"n":"Imphal","s":"MN","lat":24.81,"lon":93.94,"c":["rice","vegetables"],"i":"rainfed"},
    {"n":"Shillong","s":"ML","lat":25.57,"lon":91.88,"c":["rice","potato"],"i":"rainfed"},
    # Goa
    {"n":"Panaji","s":"GA","lat":15.50,"lon":73.83,"c":["rice","coconut"],"i":"rainfed"},
    # J&K
    {"n":"Jammu","s":"JK","lat":32.73,"lon":74.87,"c":["rice","wheat"],"i":"canal"},
    {"n":"Srinagar","s":"JK","lat":34.08,"lon":74.80,"c":["rice","saffron"],"i":"canal"},
    # Arunachal / Mizoram / Nagaland / Sikkim
    {"n":"Itanagar","s":"AR","lat":27.08,"lon":93.62,"c":["rice","maize"],"i":"rainfed"},
    {"n":"Aizawl","s":"MZ","lat":23.73,"lon":92.72,"c":["rice","maize"],"i":"rainfed"},
    {"n":"Kohima","s":"NL","lat":25.67,"lon":94.12,"c":["rice","maize"],"i":"rainfed"},
    {"n":"Gangtok","s":"SK","lat":27.33,"lon":88.62,"c":["rice","cardamom"],"i":"rainfed"},
]

STATES_FULL = {
    'UP':'Uttar Pradesh','PB':'Punjab','HR':'Haryana','MH':'Maharashtra',
    'MP':'Madhya Pradesh','RJ':'Rajasthan','GJ':'Gujarat','KA':'Karnataka',
    'AP':'Andhra Pradesh','TS':'Telangana','TN':'Tamil Nadu','KL':'Kerala',
    'WB':'West Bengal','BR':'Bihar','OR':'Odisha','AS':'Assam','JH':'Jharkhand',
    'CG':'Chhattisgarh','UK':'Uttarakhand','HP':'Himachal Pradesh',
    'TR':'Tripura','MN':'Manipur','ML':'Meghalaya','GA':'Goa',
    'JK':'Jammu & Kashmir','AR':'Arunachal Pradesh','MZ':'Mizoram',
    'NL':'Nagaland','SK':'Sikkim',
}

# ═════════════════════════════════════════
# API FETCHERS (all free, no auth)
# ═════════════════════════════════════════

async def fetch_nasa_power(session, lat, lon, start, end):
    """NASA POWER: 11 daily parameters."""
    params = "T2M,T2M_MAX,T2M_MIN,RH2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN,WS2M,ALLSKY_SFC_LW_DWN,T2MDEW,PS,CLOUD_AMT"
    url = (f"https://power.larc.nasa.gov/api/temporal/daily/point"
           f"?parameters={params}&community=AG"
           f"&longitude={lon}&latitude={lat}&start={start}&end={end}&format=JSON")
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as r:
            if r.status == 200:
                d = await r.json()
                return d.get("properties",{}).get("parameter",{})
    except Exception as e:
        logger.debug(f"NASA POWER err ({lat},{lon}): {e}")
    return None

async def fetch_open_meteo_weather(session, lat, lon, start, end):
    """Open-Meteo Historical: daily weather + ET₀."""
    url = (f"https://archive-api.open-meteo.com/v1/archive"
           f"?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}"
           f"&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,"
           f"precipitation_sum,rain_sum,et0_fao_evapotranspiration,"
           f"windspeed_10m_max,shortwave_radiation_sum,weathercode"
           f"&timezone=Asia/Kolkata")
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as r:
            if r.status == 200:
                return (await r.json()).get("daily",{})
    except Exception as e:
        logger.debug(f"Open-Meteo weather err: {e}")
    return None

async def fetch_open_meteo_soil(session, lat, lon, start, end):
    """Open-Meteo: soil temp & moisture at multiple depths."""
    url = (f"https://archive-api.open-meteo.com/v1/archive"
           f"?latitude={lat}&longitude={lon}&start_date={start}&end_date={end}"
           f"&hourly=soil_temperature_0cm,soil_temperature_6cm,"
           f"soil_moisture_0_to_1cm,soil_moisture_1_to_3cm,soil_moisture_3_to_9cm"
           f"&timezone=Asia/Kolkata")
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as r:
            if r.status == 200:
                h = (await r.json()).get("hourly",{})
                # Average hourly to daily
                daily = {}
                for key in h:
                    if key == "time": continue
                    vals = h[key]
                    if vals:
                        n = min(len(vals)//24, 730)
                        daily[key] = [np.nanmean([v for v in vals[i*24:(i+1)*24] if v is not None])
                                      for i in range(n)]
                return daily
    except Exception as e:
        logger.debug(f"Open-Meteo soil err: {e}")
    return None

async def fetch_open_meteo_air(session, lat, lon, start, end):
    """Open-Meteo Air Quality: PM2.5, dust, UV, aerosol."""
    url = (f"https://air-quality-api.open-meteo.com/v1/air-quality"
           f"?latitude={lat}&longitude={lon}"
           f"&hourly=pm2_5,pm10,dust,uv_index,aerosol_optical_depth"
           f"&start_date={start}&end_date={end}&timezone=Asia/Kolkata")
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as r:
            if r.status == 200:
                h = (await r.json()).get("hourly",{})
                daily = {}
                for key in h:
                    if key == "time": continue
                    vals = h[key]
                    if vals:
                        n = min(len(vals)//24, 730)
                        daily[key] = [np.nanmean([v for v in vals[i*24:(i+1)*24] if v is not None])
                                      for i in range(n)]
                return daily
    except Exception as e:
        logger.debug(f"Open-Meteo air err: {e}")
    return None

async def fetch_elevation(session, lat, lon):
    """Open-Meteo Elevation API."""
    url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as r:
            if r.status == 200:
                d = await r.json()
                return d.get("elevation", [0])[0] if isinstance(d.get("elevation"), list) else d.get("elevation", 0)
    except:
        pass
    return 0

async def fetch_soilgrids(session, lat, lon):
    """ISRIC SoilGrids: soil properties (free, no auth)."""
    url = (f"https://rest.isric.org/soilgrids/v2.0/properties/query"
           f"?lon={lon}&lat={lat}"
           f"&property=clay&property=sand&property=soc&property=phh2o"
           f"&depth=0-5cm&value=mean")
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as r:
            if r.status == 200:
                d = await r.json()
                result = {}
                for layer in d.get("properties", {}).get("layers", []):
                    name = layer.get("name", "")
                    depths = layer.get("depths", [])
                    if depths:
                        val = depths[0].get("values", {}).get("mean")
                        if val is not None:
                            result[name] = val
                return result
    except Exception as e:
        logger.debug(f"SoilGrids err: {e}")
    return {}


# ═════════════════════════════════════════
# MAIN COLLECTOR
# ═════════════════════════════════════════

async def collect_all(districts=None, days_back=730):
    """Pull from all 6 APIs for all districts."""
    if districts is None:
        districts = DISTRICTS

    end_dt = datetime.now() - timedelta(days=5)  # API lag
    start_dt = end_dt - timedelta(days=days_back)
    nasa_s = start_dt.strftime("%Y%m%d")
    nasa_e = end_dt.strftime("%Y%m%d")
    iso_s = start_dt.strftime("%Y-%m-%d")
    iso_e = end_dt.strftime("%Y-%m-%d")

    all_samples = []
    conn = aiohttp.TCPConnector(limit=3)

    async with aiohttp.ClientSession(connector=conn) as session:
        for i, d in enumerate(districts):
            print(f"  [{i+1}/{len(districts)}] {d['n']} ({d['s']}) ...", end="", flush=True)

            # Fetch all sources concurrently
            tasks = [
                fetch_nasa_power(session, d['lat'], d['lon'], nasa_s, nasa_e),
                fetch_open_meteo_weather(session, d['lat'], d['lon'], iso_s, iso_e),
                fetch_open_meteo_soil(session, d['lat'], d['lon'], iso_s, iso_e),
                fetch_open_meteo_air(session, d['lat'], d['lon'], iso_s, iso_e),
                fetch_elevation(session, d['lat'], d['lon']),
                fetch_soilgrids(session, d['lat'], d['lon']),
            ]
            nasa, weather, soil, air, elev, soilg = await asyncio.gather(*tasks)

            if not nasa and not weather:
                print(" ❌"); continue

            # Merge daily
            dates = []
            if nasa and "T2M" in nasa:
                dates = sorted(nasa["T2M"].keys())

            n_added = 0
            for di, dk in enumerate(dates):
                s = {
                    "district": d['n'], "state": d['s'],
                    "lat": d['lat'], "lon": d['lon'],
                    "crops": d['c'], "irrig": d['i'],
                    "elevation": elev or 0,
                    "soil_clay": soilg.get("clay", 250) / 10.0,
                    "soil_sand": soilg.get("sand", 500) / 10.0,
                    "soil_soc": soilg.get("soc", 100) / 10.0,
                    "soil_ph": soilg.get("phh2o", 65) / 10.0,
                }

                # NASA features
                if nasa:
                    s["T2M"] = nasa.get("T2M",{}).get(dk,-999)
                    s["T2M_MAX"] = nasa.get("T2M_MAX",{}).get(dk,-999)
                    s["T2M_MIN"] = nasa.get("T2M_MIN",{}).get(dk,-999)
                    s["RH2M"] = nasa.get("RH2M",{}).get(dk,-999)
                    s["PREC"] = nasa.get("PRECTOTCORR",{}).get(dk,-999)
                    s["SOLAR"] = nasa.get("ALLSKY_SFC_SW_DWN",{}).get(dk,-999)
                    s["WIND"] = nasa.get("WS2M",{}).get(dk,-999)
                    s["LW"] = nasa.get("ALLSKY_SFC_LW_DWN",{}).get(dk,-999)
                    s["TDEW"] = nasa.get("T2MDEW",{}).get(dk,-999)
                    s["PS"] = nasa.get("PS",{}).get(dk,-999)
                    s["CLOUD"] = nasa.get("CLOUD_AMT",{}).get(dk,-999)

                # Weather features
                if weather and di < len(weather.get("time",[])):
                    s["ET0"] = (weather.get("et0_fao_evapotranspiration") or [None]*999)[di]
                    s["RAD"] = (weather.get("shortwave_radiation_sum") or [None]*999)[di]
                    s["WCODE"] = (weather.get("weathercode") or [None]*999)[di]
                    s["WMAX"] = (weather.get("windspeed_10m_max") or [None]*999)[di]

                # Soil features
                if soil and di < len(soil.get("soil_moisture_0_to_1cm",[])):
                    s["SM0"] = soil.get("soil_moisture_0_to_1cm",[None]*999)[di]
                    s["SM1"] = soil.get("soil_moisture_1_to_3cm",[None]*999)[di]
                    s["SM3"] = soil.get("soil_moisture_3_to_9cm",[None]*999)[di]
                    s["ST0"] = soil.get("soil_temperature_0cm",[None]*999)[di]
                    s["ST6"] = soil.get("soil_temperature_6cm",[None]*999)[di]

                # Air quality features
                if air and di < len(air.get("pm2_5",[])):
                    s["PM25"] = air.get("pm2_5",[None]*999)[di]
                    s["PM10"] = air.get("pm10",[None]*999)[di]
                    s["DUST"] = air.get("dust",[None]*999)[di]
                    s["UV"] = air.get("uv_index",[None]*999)[di]
                    s["AOD"] = air.get("aerosol_optical_depth",[None]*999)[di]

                if s.get("T2M",-999) == -999: continue

                # Temporal
                try:
                    doy = datetime.strptime(str(dk).replace("-","")[:8], "%Y%m%d").timetuple().tm_yday
                except:
                    doy = 180
                s["DOY_SIN"] = math.sin(2*math.pi*doy/365)
                s["DOY_COS"] = math.cos(2*math.pi*doy/365)
                s["MON_SIN"] = math.sin(2*math.pi*(doy//30)/12)
                s["MON_COS"] = math.cos(2*math.pi*(doy//30)/12)

                all_samples.append(s)
                n_added += 1

            print(f" ✅ {n_added} days")
            await asyncio.sleep(0.3)

    return all_samples


if __name__ == "__main__":
    print("═"*60)
    print("  Maximum Satellite Data Collector")
    print("═"*60)
    print(f"  Districts: {len(DISTRICTS)}")
    print(f"  APIs: NASA POWER, Open-Meteo (Weather+Soil+Air+Elev), SoilGrids")
    data = asyncio.run(collect_all(days_back=730))
    print(f"\n  Total samples: {len(data)}")
    Path("models").mkdir(exist_ok=True)
    with open("models/max_satellite_data.json","w") as f:
        json.dump(data, f)
    print(f"  Saved to models/max_satellite_data.json")
