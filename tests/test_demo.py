"""La demo de docs/ sigue siendo una página estática, en español, sin secretos y al día con datos/."""

from __future__ import annotations

import re
from html.parser import HTMLParser

from conftest import RAIZ

from havenhero import demo

DOCS = RAIZ / "docs"
TEXTOS = [
    *DOCS.glob("*.html"),
    *DOCS.glob("*.js"),
    *DOCS.glob("*.css"),
    *(RAIZ / "datos").glob("*.json"),
    *(RAIZ / "havenhero").glob("*.py"),
    RAIZ / "README.md",
]
EMOJI = re.compile("[\U0001f000-\U0001faff☀-➿️]")
SECRETO = re.compile(r"mapbox|access_token|api[_-]?key|\bpk\.[A-Za-z0-9]|\bsk\.[A-Za-z0-9]", re.IGNORECASE)


class _Recursos(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.idioma = None
        self.recursos: list[str] = []

    def handle_starttag(self, etiqueta, atributos):
        atributos = dict(atributos)
        if etiqueta == "html":
            self.idioma = atributos.get("lang")
        if etiqueta == "script" and atributos.get("src"):
            self.recursos.append(atributos["src"])
        if etiqueta == "link" and atributos.get("rel") == "stylesheet":
            self.recursos.append(atributos["href"])


def _pagina() -> _Recursos:
    lector = _Recursos()
    lector.feed((DOCS / "index.html").read_text(encoding="utf-8"))
    return lector


def test_datos_js_esta_generado_desde_datos():
    assert demo.esta_al_dia(), "docs/datos.js no coincide con datos/. Corré: python3 -m havenhero generar-demo"


def test_la_pagina_esta_en_espanol_y_sus_archivos_locales_existen():
    pagina = _pagina()
    assert pagina.idioma == "es"
    locales = [r for r in pagina.recursos if not r.startswith("http")]
    assert {"datos.js", "regla.js", "app.js", "estilos.css"} <= set(locales)
    for recurso in locales:
        assert (DOCS / recurso).is_file(), recurso
    assert (DOCS / ".nojekyll").exists()


def test_los_recursos_externos_son_solo_leaflet():
    externos = [r for r in _pagina().recursos if r.startswith("http")]
    assert externos and all(r.startswith("https://unpkg.com/leaflet@") for r in externos), externos


def test_los_scripts_cargan_datos_y_regla_antes_que_la_interfaz():
    locales = [r for r in _pagina().recursos if r.endswith(".js") and not r.startswith("http")]
    assert locales == ["datos.js", "regla.js", "app.js"]


def test_la_interfaz_no_lleva_datos_ni_regla_propios():
    app = (DOCS / "app.js").read_text(encoding="utf-8")
    assert "regla.evaluar(" in app
    for prohibido in ("alcance_km:", "Math.asin", "Math.sin", "6371"):
        assert prohibido not in app, prohibido
    # Ninguna coordenada escrita a mano: los únicos decimales son opacidades.
    assert set(re.findall(r"-?\d+\.\d{2,}", app)) <= {"0.06", "0.85"}


def test_sin_tokens_ni_proveedores_de_pago_ni_emojis():
    for archivo in TEXTOS:
        texto = archivo.read_text(encoding="utf-8")
        assert not SECRETO.search(texto), archivo.name
        assert not EMOJI.search(texto), archivo.name
