"""Una sola regla: la de Python y la de la demo en JS tienen que dar lo mismo.

Se evalúa una grilla de puntos, puntos aleatorios con semilla fija y todos los
casos de casos.json en los dos lenguajes, y se comparan los resultados
completos. Si alguien cambia la regla o los datos en un solo lado, esto falla.

Si no hay ``node`` el test falla en vez de saltarse: una paridad sin comprobar
no cuenta como comprobada.
"""

from __future__ import annotations

import json
import random
import shutil
import subprocess

from conftest import CASOS, RAIZ, evaluar_trabajo


def _trabajos() -> list[dict]:
    trabajos = [
        {"lat": round(3.25 + i * 0.0125, 6), "lon": round(-76.70 + j * 0.0125, 6)} for i in range(29) for j in range(29)
    ]
    azar = random.Random(20261113)
    trabajos += [{"lat": azar.uniform(3.2, 3.6), "lon": azar.uniform(-76.75, -76.3)} for _ in range(500)]
    trabajos += [{"lat": azar.uniform(-90, 90), "lon": azar.uniform(-180, 180)} for _ in range(100)]
    trabajos += [{"lat": 90, "lon": 180}, {"lat": -90, "lon": -180}, {"lat": 0, "lon": 0}, {"lat": 90.5, "lon": 0}]
    trabajos += [{k: v for k, v in caso.items() if k in ("lat", "lon", "zonas", "refugios")} for caso in CASOS]
    return trabajos


def _evaluar_en_js(trabajos: list[dict]) -> list[dict]:
    node = shutil.which("node")
    assert node, "hace falta node en el PATH para comprobar que docs/regla.js coincide con havenhero/"
    proceso = subprocess.run(
        [node, str(RAIZ / "tests" / "paridad_runner.js")],
        input=json.dumps(trabajos),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        check=False,
    )
    assert proceso.returncode == 0, proceso.stderr
    return json.loads(proceso.stdout)


def test_python_y_js_dan_el_mismo_resultado():
    trabajos = _trabajos()
    en_python = [evaluar_trabajo(t) for t in trabajos]
    en_js = _evaluar_en_js(trabajos)

    assert len(en_js) == len(en_python)
    distintos = [(t, p, j) for t, p, j in zip(trabajos, en_python, en_js) if p != j]
    assert not distintos, f"{len(distintos)} de {len(trabajos)} resultados difieren. Primero: {distintos[0]}"

    # La muestra tiene que ejercitar la regla, no solo ceros.
    puntajes = {r["ok"]["exposicion"]["puntaje"] for r in en_python if "ok" in r}
    elegidos = {r["ok"]["refugio"]["id"] for r in en_python if "ok" in r and r["ok"]["refugio"]}
    assert {0, 100} <= puntajes and len(puntajes) > 50
    assert len(elegidos) >= 5
    assert any("error" in r for r in en_python)
