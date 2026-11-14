import pytest

from havenhero.indice import exposicion, nivel_de, puntaje_de_zona
from havenhero.regla import cargar_regla
from havenhero.zonas import cargar_zonas, zonas_desde


@pytest.mark.parametrize(
    ("metros", "alcance_km", "esperado"),
    [(0, 9.0, 100), (4500, 9.0, 50), (9000, 9.0, 0), (9001, 9.0, 0), (50000, 9.0, 0), (8955, 9.0, 1), (8956, 9.0, 0)],
)
def test_puntaje_baja_en_linea_recta_y_nunca_es_negativo(metros, alcance_km, esperado):
    assert puntaje_de_zona(metros, alcance_km) == esperado


@pytest.mark.parametrize(
    ("puntaje", "nivel"),
    [(0, "fuera_de_alcance"), (1, "bajo"), (33, "bajo"), (34, "medio"), (66, "medio"), (67, "alto"), (100, "alto")],
)
def test_niveles_en_los_umbrales(puntaje, nivel):
    assert nivel_de(puntaje, cargar_regla()) == nivel


def test_gana_la_zona_de_mayor_puntaje():
    # Punto de referencia "Siloé" de la demo: pegado al centro de la ladera.
    resultado = exposicion(3.428, -76.568, cargar_zonas(), cargar_regla())
    assert resultado["dominantes"] == ["ladera-occidente"]
    assert resultado["puntaje"] == max(z["puntaje"] for z in resultado["zonas"])
    assert [z["id"] for z in resultado["zonas"]] == [z.id for z in cargar_zonas()]


def test_el_orden_de_las_zonas_no_cambia_el_indice():
    zonas = cargar_zonas()
    regla = cargar_regla()
    directo = exposicion(3.44, -76.53, zonas, regla)
    invertido = exposicion(3.44, -76.53, tuple(reversed(zonas)), regla)
    assert (directo["puntaje"], directo["nivel"], directo["dominantes"]) == (
        invertido["puntaje"],
        invertido["nivel"],
        invertido["dominantes"],
    )


def test_el_puntaje_no_sube_al_alejarse_del_centro():
    zona = zonas_desde([{"id": "z", "tipo": "ladera", "lat": 3.43, "lon": -76.57, "alcance_km": 7.0}])
    regla = cargar_regla()
    puntajes = [exposicion(3.43 + paso * 0.005, -76.57, zona, regla)["puntaje"] for paso in range(20)]
    assert puntajes == sorted(puntajes, reverse=True)
    assert puntajes[0] == 100 and puntajes[-1] == 0
