import itertools

from havenhero.refugio_cercano import refugio_mas_cercano
from havenhero.refugios import cargar_refugios, refugios_desde
from havenhero.regla import cargar_regla

REGLA = cargar_regla()


def test_sin_refugios_devuelve_none():
    assert refugio_mas_cercano(3.45, -76.53, (), REGLA) is None


def test_un_solo_refugio_es_el_elegido_aunque_este_lejos():
    unico = refugios_desde([{"id": "unico", "lat": 4.7, "lon": -74.0}])
    resultado = refugio_mas_cercano(3.45, -76.53, unico, REGLA)
    assert resultado["id"] == "unico"
    assert resultado["distancia_m"] > 250_000
    assert resultado["empatados"] == []


def test_elige_el_de_menor_distancia_entre_los_de_la_demo():
    refugios = cargar_refugios()
    resultado = refugio_mas_cercano(3.40, -76.50, refugios, REGLA)
    assert resultado["id"] == "refugio-oriente"
    assert resultado["empatados"] == []


def test_el_empate_no_depende_del_orden_de_entrada():
    crudos = [
        {"id": "b", "lat": 3.46, "lon": -76.53},
        {"id": "a", "lat": 3.44, "lon": -76.53},
        {"id": "c", "lat": 3.46, "lon": -76.53},
    ]
    for permutacion in itertools.permutations(crudos):
        resultado = refugio_mas_cercano(3.45, -76.53, refugios_desde(permutacion), REGLA)
        assert resultado["id"] == "a"
        assert resultado["empatados"] == ["b", "c"]


def test_un_metro_de_diferencia_no_es_empate():
    # 0.00001 grados de latitud son 1,1 m: el segundo queda más lejos y no empata.
    crudos = [{"id": "a", "lat": 3.46001, "lon": -76.53}, {"id": "b", "lat": 3.46, "lon": -76.53}]
    resultado = refugio_mas_cercano(3.45, -76.53, refugios_desde(crudos), REGLA)
    assert resultado["id"] == "b"
    assert resultado["empatados"] == []
