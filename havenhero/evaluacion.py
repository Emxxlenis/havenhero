"""Punto de entrada de la regla: exposición más refugio para un punto."""

from __future__ import annotations

from typing import Any, Sequence

from havenhero.distancia import validar_punto
from havenhero.indice import exposicion
from havenhero.refugio_cercano import refugio_mas_cercano
from havenhero.refugios import Refugio, cargar_refugios
from havenhero.regla import Regla, cargar_regla
from havenhero.zonas import Zona, cargar_zonas


def evaluar(
    lat: float,
    lon: float,
    *,
    zonas: Sequence[Zona] | None = None,
    refugios: Sequence[Refugio] | None = None,
    regla: Regla | None = None,
) -> dict[str, Any]:
    """Evalúa un punto. Sin argumentos extra usa los archivos de ``datos/``.

    Lanza ``ValueError`` si las coordenadas no son números finitos dentro de rango.
    Una lista vacía de zonas o de refugios es válida y se respeta.
    """
    validar_punto(lat, lon)
    regla = cargar_regla() if regla is None else regla
    zonas = cargar_zonas() if zonas is None else zonas
    refugios = cargar_refugios() if refugios is None else refugios
    return {
        "punto": {"lat": lat, "lon": lon},
        "dentro_del_area": regla.area.contiene(lat, lon),
        "exposicion": exposicion(lat, lon, zonas, regla),
        "refugio": refugio_mas_cercano(lat, lon, refugios, regla),
    }
