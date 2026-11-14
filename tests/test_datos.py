"""Los archivos de datos/ cargan, son coherentes y están rotulados como demostración."""

import copy
import json

import pytest

from havenhero._archivos import DIRECTORIO_DATOS, DatosInvalidos, leer_json
from havenhero.refugios import cargar_refugios, refugios_desde
from havenhero.regla import cargar_regla, regla_desde
from havenhero.zonas import cargar_tipos, cargar_zonas, zonas_desde

ZONA = {"id": "z", "tipo": "ladera", "lat": 3.4, "lon": -76.5, "alcance_km": 5.0}


def test_todos_los_archivos_de_datos_se_declaran_demostracion():
    archivos = sorted(DIRECTORIO_DATOS.glob("*.json"))
    assert archivos
    for archivo in archivos:
        contenido = json.loads(archivo.read_text(encoding="utf-8"))
        assert contenido.get("demostracion") is True, archivo.name
        assert contenido.get("nota"), archivo.name


def test_los_datos_de_la_demo_cargan_y_caen_dentro_del_area():
    area = cargar_regla().area
    assert len(cargar_zonas()) >= 2
    assert {z.tipo for z in cargar_zonas()} == set(cargar_tipos())
    assert cargar_refugios()
    for item in (*cargar_zonas(), *cargar_refugios()):
        assert area.contiene(item.lat, item.lon), item.id
    for punto in leer_json("puntos_referencia.json")["puntos"]:
        assert area.contiene(punto["lat"], punto["lon"]), punto["id"]


@pytest.mark.parametrize(
    "cambio",
    [{"alcance_km": 0}, {"alcance_km": -1}, {"lat": 95}, {"id": "Con Espacios"}, {"id": "ñandú"}, {"tipo": "sismo"}],
)
def test_zona_invalida_se_rechaza(cambio):
    with pytest.raises(ValueError):
        zonas_desde([{**ZONA, **cambio}], tipos=["ladera", "inundacion"])


def test_ids_repetidos_se_rechazan():
    with pytest.raises(DatosInvalidos):
        zonas_desde([ZONA, ZONA])
    with pytest.raises(DatosInvalidos):
        refugios_desde([{"id": "r", "lat": 3.4, "lon": -76.5}] * 2)


def test_refugio_con_coordenadas_invalidas_se_rechaza():
    with pytest.raises(ValueError):
        refugios_desde([{"id": "r", "lat": 3.4, "lon": 200}])


@pytest.mark.parametrize(
    "romper",
    [
        lambda r: r["niveles"].pop(),  # ya no termina en desde=0
        lambda r: r["niveles"].reverse(),  # orden ascendente
        lambda r: r["niveles"][0].update(desde=101),
        lambda r: r["niveles"][1].update(desde=67),  # umbral repetido
        lambda r: r.update(radio_tierra_km=0),
        lambda r: r["area_de_estudio"].update(lat_min=4.0),
    ],
)
def test_regla_invalida_se_rechaza(romper):
    cruda = copy.deepcopy(leer_json("regla.json"))
    romper(cruda)
    with pytest.raises(DatosInvalidos):
        regla_desde(cruda)
