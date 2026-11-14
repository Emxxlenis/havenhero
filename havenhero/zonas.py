"""Zonas de exposición: un centro, un tipo de amenaza y un alcance en kilómetros."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Iterable

from havenhero._archivos import DatosInvalidos, leer_json, validar_id, validar_unicos
from havenhero.distancia import validar_punto


@dataclass(frozen=True)
class Zona:
    id: str
    tipo: str
    nombre: str
    lat: float
    lon: float
    alcance_km: float


def zonas_desde(crudas: Iterable[dict[str, Any]], tipos: Iterable[str] | None = None) -> tuple[Zona, ...]:
    """Valida y construye zonas. Si se pasa ``tipos``, el tipo de cada zona debe estar ahí."""
    permitidos = None if tipos is None else set(tipos)
    zonas = []
    for cruda in crudas:
        identificador = validar_id(cruda.get("id"), "zonas")
        validar_punto(cruda["lat"], cruda["lon"])
        alcance = cruda["alcance_km"]
        if isinstance(alcance, bool) or not isinstance(alcance, (int, float)) or alcance <= 0:
            raise DatosInvalidos(f"zona {identificador}: alcance_km debe ser mayor que cero")
        tipo = validar_id(cruda["tipo"], f"zona {identificador}")
        if permitidos is not None and tipo not in permitidos:
            raise DatosInvalidos(f"zona {identificador}: tipo desconocido {tipo!r}")
        nombre = str(cruda.get("nombre", identificador))
        zonas.append(Zona(identificador, tipo, nombre, cruda["lat"], cruda["lon"], alcance))
    validar_unicos([z.id for z in zonas], "zonas")
    return tuple(zonas)


@lru_cache(maxsize=1)
def cargar_tipos() -> dict[str, str]:
    return dict(leer_json("zonas.json")["tipos"])


@lru_cache(maxsize=1)
def cargar_zonas() -> tuple[Zona, ...]:
    return zonas_desde(leer_json("zonas.json")["zonas"], cargar_tipos())
