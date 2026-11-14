"""Parámetros de la regla: radio terrestre, niveles del índice y área de estudio."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from havenhero._archivos import DatosInvalidos, leer_json, validar_id, validar_unicos


@dataclass(frozen=True)
class Nivel:
    id: str
    etiqueta: str
    desde: int


@dataclass(frozen=True)
class Area:
    lat_min: float
    lat_max: float
    lon_min: float
    lon_max: float

    def contiene(self, lat: float, lon: float) -> bool:
        return self.lat_min <= lat <= self.lat_max and self.lon_min <= lon <= self.lon_max


@dataclass(frozen=True)
class Regla:
    radio_tierra_km: float
    niveles: tuple[Nivel, ...]
    area: Area


def regla_desde(crudo: dict[str, Any]) -> Regla:
    radio = crudo["radio_tierra_km"]
    if isinstance(radio, bool) or not isinstance(radio, (int, float)) or radio <= 0:
        raise DatosInvalidos(f"regla: radio_tierra_km inválido {radio!r}")

    niveles = tuple(
        Nivel(validar_id(n["id"], "regla.niveles"), str(n["etiqueta"]), n["desde"]) for n in crudo["niveles"]
    )
    validar_unicos([n.id for n in niveles], "regla.niveles")
    desdes = [n.desde for n in niveles]
    if not all(isinstance(d, int) and not isinstance(d, bool) for d in desdes):
        raise DatosInvalidos("regla.niveles: 'desde' debe ser entero")
    if not desdes or desdes[-1] != 0 or desdes[0] > 100:
        raise DatosInvalidos("regla.niveles: debe terminar en desde=0 y no pasar de 100")
    if any(a <= b for a, b in zip(desdes, desdes[1:])):
        raise DatosInvalidos("regla.niveles: deben ir de mayor a menor sin repetir 'desde'")

    a = crudo["area_de_estudio"]
    area = Area(a["lat_min"], a["lat_max"], a["lon_min"], a["lon_max"])
    if not (area.lat_min < area.lat_max and area.lon_min < area.lon_max):
        raise DatosInvalidos("regla.area_de_estudio: mínimos y máximos invertidos")
    return Regla(float(radio), niveles, area)


@lru_cache(maxsize=1)
def cargar_regla() -> Regla:
    return regla_desde(leer_json("regla.json"))
