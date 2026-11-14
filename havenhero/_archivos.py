"""Lectura de los archivos de ``datos/`` y validaciones compartidas."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parent.parent
DIRECTORIO_DATOS = RAIZ / "datos"

_ID_VALIDO = re.compile(r"^[a-z0-9]+(?:[-_][a-z0-9]+)*$")


class DatosInvalidos(ValueError):
    """Un archivo de ``datos/`` no cumple el formato esperado."""


def leer_json(nombre: str) -> Any:
    with (DIRECTORIO_DATOS / nombre).open(encoding="utf-8") as archivo:
        return json.load(archivo)


def validar_id(valor: object, contexto: str) -> str:
    # Los ids son ASCII para que el orden alfabético sea el mismo en Python y en JS.
    if not isinstance(valor, str) or not _ID_VALIDO.match(valor):
        raise DatosInvalidos(f"{contexto}: id inválido {valor!r}")
    return valor


def validar_unicos(ids: list[str], contexto: str) -> None:
    repetidos = sorted({i for i in ids if ids.count(i) > 1})
    if repetidos:
        raise DatosInvalidos(f"{contexto}: ids repetidos {repetidos}")
