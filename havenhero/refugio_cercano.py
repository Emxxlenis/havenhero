"""Refugio más cercano en línea recta."""

from __future__ import annotations

from typing import Any, Sequence

from havenhero.distancia import distancia_m
from havenhero.refugios import Refugio
from havenhero.regla import Regla


def refugio_mas_cercano(lat: float, lon: float, refugios: Sequence[Refugio], regla: Regla) -> dict[str, Any] | None:
    """Devuelve el refugio de menor distancia, o ``None`` si no hay refugios.

    Dos refugios empatan cuando quedan a la misma distancia en metros enteros.
    El empate se resuelve por id en orden alfabético, así el resultado no
    depende del orden del archivo, y los demás empatados van en ``empatados``
    para que quien decide los vea.
    """
    if not refugios:
        return None
    medidos = sorted(
        ((distancia_m(lat, lon, r.lat, r.lon, regla.radio_tierra_km), r.id, r) for r in refugios),
        key=lambda medido: medido[:2],
    )
    metros, _, elegido = medidos[0]
    return {
        "id": elegido.id,
        "nombre": elegido.nombre,
        "lat": elegido.lat,
        "lon": elegido.lon,
        "distancia_m": metros,
        "empatados": [identificador for m, identificador, _ in medidos[1:] if m == metros],
    }
