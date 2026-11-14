"""Refugios: puntos a los que se puede remitir a una persona."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Iterable

from havenhero._archivos import leer_json, validar_id, validar_unicos
from havenhero.distancia import validar_punto


@dataclass(frozen=True)
class Refugio:
    id: str
    nombre: str
    lat: float
    lon: float


def refugios_desde(crudos: Iterable[dict[str, Any]]) -> tuple[Refugio, ...]:
    refugios = []
    for crudo in crudos:
        identificador = validar_id(crudo.get("id"), "refugios")
        validar_punto(crudo["lat"], crudo["lon"])
        nombre = str(crudo.get("nombre", identificador))
        refugios.append(Refugio(identificador, nombre, crudo["lat"], crudo["lon"]))
    validar_unicos([r.id for r in refugios], "refugios")
    return tuple(refugios)


@lru_cache(maxsize=1)
def cargar_refugios() -> tuple[Refugio, ...]:
    return refugios_desde(leer_json("refugios.json")["refugios"])
