"""Genera ``docs/datos.js`` a partir de ``datos/``.

La demo es una página estática que también se abre con ``file://``, donde
``fetch`` de un JSON no funciona. Por eso los datos se publican como un script.
``datos/`` es la fuente; ``docs/datos.js`` no se edita a mano.
"""

from __future__ import annotations

import json
from typing import Any

from havenhero._archivos import RAIZ, leer_json
from havenhero.refugios import cargar_refugios
from havenhero.regla import cargar_regla
from havenhero.zonas import cargar_zonas

RUTA_DATOS_JS = RAIZ / "docs" / "datos.js"

_CABECERA = (
    "// ARCHIVO GENERADO. No editar a mano.\n"
    "// Fuente: datos/*.json. Regenerar con: python3 -m havenhero generar-demo\n"
    "// Todo el contenido es de demostración: zonas, refugios, umbrales y área.\n"
)
_PIE = 'if (typeof module === "object" && module.exports) {\n  module.exports = HAVENHERO_DATOS;\n}\n'


def datos_de_la_demo() -> dict[str, Any]:
    # Cargar por los módulos valida los archivos antes de publicarlos.
    cargar_zonas()
    cargar_refugios()
    cargar_regla()
    zonas, regla = leer_json("zonas.json"), leer_json("regla.json")
    return {
        "tipos": zonas["tipos"],
        "zonas": zonas["zonas"],
        "refugios": leer_json("refugios.json")["refugios"],
        "regla": {clave: regla[clave] for clave in ("radio_tierra_km", "niveles", "area_de_estudio")},
        "puntos_referencia": leer_json("puntos_referencia.json")["puntos"],
    }


def contenido_datos_js() -> str:
    cuerpo = json.dumps(datos_de_la_demo(), ensure_ascii=False, indent=2)
    return f"{_CABECERA}var HAVENHERO_DATOS = {cuerpo};\n{_PIE}"


def esta_al_dia() -> bool:
    return RUTA_DATOS_JS.exists() and RUTA_DATOS_JS.read_text(encoding="utf-8") == contenido_datos_js()


def escribir() -> None:
    RUTA_DATOS_JS.write_text(contenido_datos_js(), encoding="utf-8")
