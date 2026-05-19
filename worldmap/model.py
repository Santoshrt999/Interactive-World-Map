import math
import os
import threading
import urllib.request
import urllib.error
from collections import deque
from typing import Dict, List, Optional, Tuple

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

from PyQt6.QtGui import QImage, QColor

from .data.geojson import SAMPLE_FEATURES
from .data.places import SEARCH_INDEX

TILE_SERVER = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".interactive_world_map", "tiles")
TILE_SIZE = 256


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


class OfflineError(Exception):
    pass


class SpatialIndex:
    def __init__(self, features: List[Dict]):
        self.cell_size = 30.0
        self.grid: Dict[Tuple[int, int], List[Dict]] = {}
        for feature in features:
            bbox = self._feature_bbox(feature)
            feature["bbox"] = bbox
            for key in self._cells(bbox):
                self.grid.setdefault(key, []).append(feature)

    def _feature_bbox(self, feature: Dict) -> Tuple[float, float, float, float]:
        coords = feature["geometry"]["coordinates"][0]
        lons = [pt[0] for pt in coords]
        lats = [pt[1] for pt in coords]
        return min(lons), min(lats), max(lons), max(lats)

    def _cells(self, bbox: Tuple[float, float, float, float]) -> List[Tuple[int, int]]:
        minx, miny, maxx, maxy = bbox
        x0 = int(math.floor((minx + 180.0) / self.cell_size))
        y0 = int(math.floor((miny + 90.0) / self.cell_size))
        x1 = int(math.floor((maxx + 180.0) / self.cell_size))
        y1 = int(math.floor((maxy + 90.0) / self.cell_size))
        return [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]

    def query(self, lon: float, lat: float) -> List[Dict]:
        key = (
            int(math.floor((lon + 180.0) / self.cell_size)),
            int(math.floor((lat + 90.0) / self.cell_size)),
        )
        candidates = self.grid.get(key, [])
        matches = []
        for feature in candidates:
            minx, miny, maxx, maxy = feature["bbox"]
            if minx <= lon <= maxx and miny <= lat <= maxy:
                matches.append(feature)
        return matches


class MapModel:
    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        self.mode = "projection"
        self.zoom = 2
        self.center_lat = 20.0
        self.center_lon = 0.0
        self.opacity = 0.88
        self.overlay_mode = "population"
        self.offline = False
        self._tile_lock = threading.Lock()
        self._tile_cache: Dict[str, QImage] = {}
        self.features = SAMPLE_FEATURES
        self.spatial_index = SpatialIndex(self.features)
        self.search_index = SEARCH_INDEX
        self.notifications: deque[str] = deque(maxlen=5)

    @staticmethod
    def lonlat_to_tile(lon: float, lat: float, zoom: int) -> Tuple[float, float]:
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        x = (lon + 180.0) / 360.0 * n
        y = (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n
        return x, clamp(y, 0.0, n - 1)

    def _tile_cache_path(self, x: int, y: int, z: int) -> str:
        return os.path.join(CACHE_DIR, f"tile_{z}_{x}_{y}.png")

    def fetch_tile_image(self, x: int, y: int, z: int) -> QImage:
        key = f"{z}/{x}/{y}"
        with self._tile_lock:
            if key in self._tile_cache:
                return self._tile_cache[key]
        path = self._tile_cache_path(x, y, z)
        image = None

        if os.path.exists(path):
            image = QImage(path)
            if image.isNull():
                image = None

        if image is None:
            try:
                url = TILE_SERVER.format(z=z, x=x, y=y)
                tile_bytes = self._download_tile(url)
                with open(path, "wb") as handle:
                    handle.write(tile_bytes)
                image = QImage.fromData(tile_bytes)
            except Exception:
                self.offline = True
                image = self._make_placeholder_tile()
                self.notifications.append("Offline or tile server unavailable. Using cached / placeholder tiles.")
            else:
                self.offline = False

    def _download_tile(self, url: str) -> bytes:
        if requests is not None:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.content
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.read()

        if image is None or image.isNull():
            image = self._make_placeholder_tile()

        with self._tile_lock:
            self._tile_cache[key] = image
        return image

    @staticmethod
    def _make_placeholder_tile() -> QImage:
        image = QImage(TILE_SIZE, TILE_SIZE, QImage.Format.Format_RGBA8888)
        image.fill(QColor(20, 24, 35, 255))
        return image

    def search_suggestions(self, query: str, limit: int = 6) -> List[Dict]:
        search = query.strip().lower()
        if not search:
            return []
        matches = [item for item in self.search_index if search in item["label"].lower()]
        return matches[:limit]

    def set_overlay(self, mode: str) -> None:
        self.overlay_mode = mode

    def toggle_mode(self) -> None:
        self.mode = "globe" if self.mode == "projection" else "projection"

    def update_center(self, lon: float, lat: float) -> None:
        self.center_lon = ((lon + 180.0) % 360.0) - 180.0
        self.center_lat = clamp(lat, -85.0, 85.0)

    def update_zoom(self, delta: int) -> None:
        self.zoom = clamp(self.zoom + delta, 1, 5)

    def inspect_location(self, lon: float, lat: float) -> Optional[Dict]:
        matches = self.spatial_index.query(lon, lat)
        return matches[0] if matches else None

    def get_overlay_value(self, feature: Dict) -> float:
        return feature["properties"].get(self.overlay_mode, 0.0)

    def get_overlay_color(self, feature: Dict) -> Tuple[float, float, float, float]:
        value = self.get_overlay_value(feature)
        if self.overlay_mode == "population":
            normalized = min(value / 1500.0, 1.0)
            return (0.95, 0.35 * normalized + 0.15, 0.12, self.opacity)
        if self.overlay_mode == "climate":
            normalized = min(max((value - 10.0) / 30.0, 0.0), 1.0)
            return (0.16, 0.65, 0.95 - normalized * 0.35, self.opacity)
        if self.overlay_mode == "gdp":
            normalized = min(value / 20000.0, 1.0)
            return (0.12 + normalized * 0.65, 0.33, 0.84, self.opacity)
        return (0.76, 0.80, 0.92, self.opacity)

    def get_notification(self) -> Optional[str]:
        return self.notifications[-1] if self.notifications else None
