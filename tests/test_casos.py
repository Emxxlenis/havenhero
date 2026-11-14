"""Casos de negocio compartidos con la demo (tests/casos.json)."""

import pytest
from conftest import CASOS, contiene, evaluar_trabajo


@pytest.mark.parametrize("caso", CASOS, ids=[c["nombre"] for c in CASOS])
def test_caso(caso):
    salida = evaluar_trabajo(caso)
    if caso.get("espera_error"):
        assert salida == {"error": True}
        return
    assert "ok" in salida, salida
    assert contiene(salida["ok"], caso["espera"]), salida["ok"]


def test_los_casos_cubren_los_bordes_pedidos():
    nombres = " | ".join(c["nombre"] for c in CASOS)
    for borde in ("lejos", "empate de distancia", "encima del centro", "sin refugios"):
        assert borde in nombres, f"falta un caso para: {borde}"
