import math

import pytest

from havenhero.distancia import distancia_m, haversine_km, redondear, validar_punto

RADIO = 6371.0


def test_distancia_cero_en_el_mismo_punto():
    assert distancia_m(3.41, -76.49, 3.41, -76.49, RADIO) == 0


def test_un_grado_de_latitud_mide_lo_que_dice_la_formula():
    assert haversine_km(3.0, -76.5, 4.0, -76.5, RADIO) == pytest.approx(math.pi * RADIO / 180, rel=1e-12)


def test_la_distancia_es_simetrica():
    ida = distancia_m(3.41, -76.49, 3.43, -76.57, RADIO)
    assert ida == distancia_m(3.43, -76.57, 3.41, -76.49, RADIO)
    assert ida == 9154


def test_antipodas_no_rompe_el_arcoseno():
    assert haversine_km(0.0, 0.0, 0.0, 180.0, RADIO) == pytest.approx(math.pi * RADIO)


@pytest.mark.parametrize(("valor", "esperado"), [(0.0, 0), (0.49, 0), (0.5, 1), (1.5, 2), (2.5, 3), (99.5, 100)])
def test_redondeo_lleva_las_mitades_hacia_arriba(valor, esperado):
    # round() de Python daría 2 para 2.5; Math.round de JS da 3. La regla usa 3.
    assert redondear(valor) == esperado


@pytest.mark.parametrize(
    ("lat", "lon"),
    [(91, 0), (-90.01, 0), (0, 180.5), (0, -181), (math.nan, 0), (0, math.inf), ("3.4", -76.5), (None, 0), (True, 0)],
)
def test_coordenadas_invalidas_se_rechazan(lat, lon):
    with pytest.raises(ValueError):
        validar_punto(lat, lon)


def test_los_extremos_del_rango_son_validos():
    validar_punto(90, 180)
    validar_punto(-90.0, -180.0)
