"""Utilidades compartidas por los tests de Python."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from havenhero import evaluar
from havenhero.refugios import refugios_desde
from havenhero.zonas import zonas_desde

RAIZ = Path(__file__).resolve().parent.parent
CASOS = json.loads((RAIZ / "tests" / "casos.json").read_text(encoding="utf-8"))["casos"]


def evaluar_trabajo(trabajo: dict[str, Any]) -> dict[str, Any]:
    """Evalúa un caso o trabajo con la forma de casos.json por el camino real de Python.

    Devuelve ``{"ok": resultado}`` o ``{"error": True}``, igual que
    tests/paridad_runner.js, para poder comparar las dos salidas tal cual.
    """
    extras: dict[str, Any] = {}
    if "zonas" in trabajo:
        extras["zonas"] = zonas_desde(trabajo["zonas"])
    if "refugios" in trabajo:
        extras["refugios"] = refugios_desde(trabajo["refugios"])
    try:
        return {"ok": evaluar(trabajo["lat"], trabajo["lon"], **extras)}
    except ValueError:
        return {"error": True}


def contiene(real: Any, esperado: Any) -> bool:
    """True si ``esperado`` es un subconjunto de ``real`` (dicts por clave, listas por posición)."""
    if isinstance(esperado, dict):
        return isinstance(real, dict) and all(k in real and contiene(real[k], v) for k, v in esperado.items())
    if isinstance(esperado, list):
        return (
            isinstance(real, list)
            and len(real) == len(esperado)
            and all(contiene(r, e) for r, e in zip(real, esperado))
        )
    return real == esperado and type(real) is type(esperado)
