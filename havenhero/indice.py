"""Índice de exposición de demostración.

Para cada zona el puntaje baja en línea recta de 100 en el centro a 0 en el
borde del alcance. El índice del punto es el puntaje más alto. No es una
probabilidad ni una medida calibrada contra eventos reales.
"""

from __future__ import annotations

from typing import Any, Sequence

from havenhero.distancia import distancia_m, redondear
from havenhero.regla import Regla
from havenhero.zonas import Zona


def puntaje_de_zona(distancia_en_m: int, alcance_km: float) -> int:
    return redondear(max(0.0, 100.0 * (1.0 - distancia_en_m / (alcance_km * 1000.0))))


def nivel_de(puntaje: int, regla: Regla) -> str:
    """Primer nivel cuyo umbral alcanza el puntaje. El último nivel empieza en 0."""
    for nivel in regla.niveles:
        if puntaje >= nivel.desde:
            return nivel.id
    raise ValueError(f"puntaje sin nivel: {puntaje!r}")


def exposicion(lat: float, lon: float, zonas: Sequence[Zona], regla: Regla) -> dict[str, Any]:
    """Puntaje por zona, índice del punto y zonas dominantes.

    ``dominantes`` lleva los ids de las zonas con el puntaje máximo, en orden
    alfabético. Queda vacía cuando el índice es 0: sin exposición no hay amenaza
    que nombrar.
    """
    detalle = []
    for zona in zonas:
        metros = distancia_m(lat, lon, zona.lat, zona.lon, regla.radio_tierra_km)
        detalle.append(
            {
                "id": zona.id,
                "tipo": zona.tipo,
                "distancia_m": metros,
                "puntaje": puntaje_de_zona(metros, zona.alcance_km),
            }
        )
    puntaje = max((z["puntaje"] for z in detalle), default=0)
    dominantes = sorted(z["id"] for z in detalle if z["puntaje"] == puntaje) if puntaje > 0 else []
    return {
        "puntaje": puntaje,
        "nivel": nivel_de(puntaje, regla),
        "dominantes": dominantes,
        "zonas": detalle,
    }
