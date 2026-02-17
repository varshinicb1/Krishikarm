"""
Bhoonidhi ISRO Satellite Data Connector
═══════════════════════════════════════
Connects to ISRO's Bhoonidhi API for accessing NISAR, ResourceSat,
EOS-04 SAR, EOS-06 Ocean Color, and Sentinel-1 data.

API Docs: https://bhoonidhi.nrsc.gov.in/bhoonidhi-api/
Requires: Bhoonidhi account + IP whitelisting

Collections available:
  - ResourceSat-2/2A (AWIFS, LISS3, LISS4-MX70)
  - EOS-04 SAR (MRS, CRS, FRS)
  - EOS-06 OCM (NDVI, AOD, CHL, TSM)
  - Sentinel-1A SAR (IW SLC/GRD)
  - NISAR (via bhoonidhi.nrsc.gov.in/NISAR/)
"""

import aiohttp
import logging
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

# Config
BHOONIDHI_API = "https://bhoonidhi-api.nrsc.gov.in"
TOKEN_CACHE = Path("models/bhoonidhi_token.json")


class BhoonidhiConnector:
    """
    ISRO Bhoonidhi API connector for satellite data access.
    Supports search, collection browsing, and data download
    for NISAR, ResourceSat, EOS-04/06, and Sentinel-1.
    """

    # Agriculture-relevant collections
    AGRI_COLLECTIONS = [
        "EOS-06_OCM-LAC_L2C-NDVI",      # NDVI from Oceansat-3
        "EOS-06_OCM-LAC_NDVI_8day_360m", # 8-day NDVI composite
        "ResourceSat-2A_LISS3_L2",       # 23.5m multispectral
        "ResourceSat-2A_AWIFS_L2",       # 56m wide-field
        "EOS-04_SAR-MRS_L2A",            # SAR medium resolution
        "EOS-06_OCM-LAC_L2C-AOD",        # Aerosol (fire/haze)
        "Sentinel-1A_SAR-IW_GRD",        # Sentinel-1 SAR crop monitoring
    ]

    def __init__(self, user_id=None, password=None):
        self.user_id = user_id or os.environ.get("BHOONIDHI_USER")
        self.password = password or os.environ.get("BHOONIDHI_PASS")
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None

    async def authenticate(self):
        """Get access token from Bhoonidhi auth endpoint."""
        if not self.user_id or not self.password:
            logger.warning("Bhoonidhi: No credentials configured. "
                         "Set BHOONIDHI_USER and BHOONIDHI_PASS env vars.")
            return False

        # Check cached token
        if TOKEN_CACHE.exists():
            try:
                cached = json.loads(TOKEN_CACHE.read_text())
                if datetime.fromisoformat(cached.get("expiry", "")) > datetime.now():
                    self.access_token = cached["access_token"]
                    self.refresh_token = cached.get("refresh_token")
                    logger.info("Bhoonidhi: Using cached token")
                    return True
            except Exception:
                pass

        payload = {
            "userId": self.user_id,
            "password": self.password,
            "grant_type": "password"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{BHOONIDHI_API}/auth/token",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self.access_token = data["access_token"]
                        self.refresh_token = data.get("refresh_token")
                        self.token_expiry = datetime.now() + timedelta(seconds=data.get("expires_in", 1200))

                        # Cache token
                        TOKEN_CACHE.parent.mkdir(exist_ok=True)
                        TOKEN_CACHE.write_text(json.dumps({
                            "access_token": self.access_token,
                            "refresh_token": self.refresh_token,
                            "expiry": self.token_expiry.isoformat(),
                        }))
                        logger.info("Bhoonidhi: Authenticated successfully")
                        return True
                    else:
                        text = await resp.text()
                        logger.error(f"Bhoonidhi auth failed ({resp.status}): {text}")
        except Exception as e:
            logger.error(f"Bhoonidhi auth error: {e}")

        return False

    def _headers(self):
        return {"Authorization": f"Bearer {self.access_token}"} if self.access_token else {}

    async def list_collections(self):
        """List available STAC collections."""
        if not self.access_token:
            if not await self.authenticate():
                return []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{BHOONIDHI_API}/data/collections",
                    headers=self._headers(),
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("collections", [])
        except Exception as e:
            logger.error(f"Bhoonidhi collections error: {e}")
        return []

    async def search_satellite_data(self, lat, lon, days_back=30,
                                     collections=None, limit=10):
        """
        Search for satellite data covering a location.
        Returns STAC items with metadata and download links.
        """
        if not self.access_token:
            if not await self.authenticate():
                return {"error": "Not authenticated", "items": []}

        if collections is None:
            collections = self.AGRI_COLLECTIONS

        end = datetime.now()
        start = end - timedelta(days=days_back)

        # Create search point
        payload = {
            "collections": collections,
            "datetime": f"{start.strftime('%Y-%m-%dT00:00:00Z')}/{end.strftime('%Y-%m-%dT23:59:59Z')}",
            "intersects": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "filter": {
                "args": [{"property": "Online"}, "Y"],
                "op": "eq"
            },
            "filter-lang": "cql2-json",
            "limit": limit
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{BHOONIDHI_API}/data/search",
                    json=payload,
                    headers=self._headers(),
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        features = data.get("features", [])
                        return {
                            "total": data.get("context", {}).get("returned", 0),
                            "items": [
                                {
                                    "id": f.get("id"),
                                    "collection": f.get("collection"),
                                    "geometry": f.get("geometry"),
                                    "properties": f.get("properties", {}),
                                }
                                for f in features
                            ]
                        }
                    elif resp.status == 401:
                        logger.warning("Bhoonidhi: Token expired, re-authenticating")
                        self.access_token = None
                        return await self.search_satellite_data(lat, lon, days_back, collections, limit)
        except Exception as e:
            logger.error(f"Bhoonidhi search error: {e}")

        return {"error": "Search failed", "items": []}

    async def search_ndvi(self, lat, lon, days_back=30):
        """Search for NDVI products from EOS-06."""
        return await self.search_satellite_data(
            lat, lon, days_back,
            collections=["EOS-06_OCM-LAC_L2C-NDVI", "EOS-06_OCM-LAC_NDVI_8day_360m"],
            limit=5
        )

    async def search_sar(self, lat, lon, days_back=30):
        """Search for SAR data from EOS-04 and Sentinel-1."""
        return await self.search_satellite_data(
            lat, lon, days_back,
            collections=["EOS-04_SAR-MRS_L2A", "Sentinel-1A_SAR-IW_GRD"],
            limit=5
        )

    async def search_multispectral(self, lat, lon, days_back=30):
        """Search for multispectral data from ResourceSat."""
        return await self.search_satellite_data(
            lat, lon, days_back,
            collections=["ResourceSat-2A_LISS3_L2", "ResourceSat-2A_AWIFS_L2"],
            limit=5
        )

    def get_download_url(self, item_id, collection):
        """Get download URL for a product."""
        return f"{BHOONIDHI_API}/download?id={item_id}&collection={collection}"


# Global instance
bhoonidhi = BhoonidhiConnector()
