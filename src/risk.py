"""Índice de exposición y refugio más cercano.

El índice es de demostración: acerca el punto a dos zonas ilustrativas
de Cali (ladera e inundación). No es un mapa oficial ni el modelo de 2024.
"""

from __future__ import annotations

import math

ZONES = (
    {"id": "flood", "name": "Inundación", "lat": 3.410, "lon": -76.490, "reach_km": 9.0},
    {"id": "hill", "name": "Ladera", "lat": 3.430, "lon": -76.570, "reach_km": 7.0},
)

SHELTERS = (
    {"name": "Refugio Centro", "lat": 3.452, "lon": -76.532},
    {"name": "Refugio Norte", "lat": 3.478, "lon": -76.527},
    {"name": "Refugio Sur", "lat": 3.395, "lon": -76.540},
    {"name": "Refugio Oriente", "lat": 3.408, "lon": -76.485},
    {"name": "Refugio Ladera", "lat": 3.428, "lon": -76.568},
)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(a))


def exposure(lat: float, lon: float) -> dict:
    parts = []
    for zone in ZONES:
        distance = haversine_km(lat, lon, zone["lat"], zone["lon"])
        score = round(max(0.0, 100.0 * (1 - distance / zone["reach_km"])))
        parts.append({"id": zone["id"], "name": zone["name"], "km": round(distance, 2), "score": score})
    dominant = max(parts, key=lambda item: item["score"])
    return {"score": dominant["score"], "hazard": dominant["name"], "parts": parts}


def nearest_shelter(lat: float, lon: float) -> dict:
    ranked = []
    for shelter in SHELTERS:
        distance = haversine_km(lat, lon, shelter["lat"], shelter["lon"])
        ranked.append({**shelter, "km": round(distance, 2)})
    ranked.sort(key=lambda item: item["km"])
    return ranked[0]
