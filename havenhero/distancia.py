"""Distancia en línea recta entre dos puntos y validación de coordenadas."""

from __future__ import annotations

import math


def redondear(valor: float) -> int:
    """Redondeo al entero más cercano, mitades hacia arriba, para valores >= 0.

    No se usa ``round`` porque redondea las mitades al par y ``Math.round`` de
    JS no: la regla tiene que dar lo mismo en los dos lenguajes.
    """
    return math.floor(valor + 0.5)


def validar_punto(lat: object, lon: object) -> None:
    for nombre, valor, limite in (("lat", lat, 90.0), ("lon", lon, 180.0)):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError(f"{nombre} debe ser un número, llegó {valor!r}")
        if not math.isfinite(valor) or abs(valor) > limite:
            raise ValueError(f"{nombre} fuera de rango: {valor!r}")


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float, radio_km: float) -> float:
    fi1, fi2 = math.radians(lat1), math.radians(lat2)
    dfi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dfi / 2) ** 2 + math.cos(fi1) * math.cos(fi2) * math.sin(dlambda / 2) ** 2
    return 2 * radio_km * math.asin(math.sqrt(min(1.0, a)))


def distancia_m(lat1: float, lon1: float, lat2: float, lon2: float, radio_km: float) -> int:
    """Distancia en metros enteros. Es la única distancia que usa la regla."""
    return redondear(haversine_km(lat1, lon1, lat2, lon2, radio_km) * 1000.0)
