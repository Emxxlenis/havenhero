import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.risk import exposure, nearest_shelter


def test_flood_center_is_high_and_points_east():
    reading = exposure(3.410, -76.490)
    assert reading["hazard"] == "Inundación"
    assert reading["score"] == 100
    assert nearest_shelter(3.410, -76.490)["name"] == "Refugio Oriente"


def test_hill_center_points_to_the_hill_shelter():
    reading = exposure(3.430, -76.570)
    assert reading["hazard"] == "Ladera"
    assert nearest_shelter(3.430, -76.570)["name"] == "Refugio Ladera"


def test_far_point_has_low_exposure():
    reading = exposure(3.90, -76.20)
    assert reading["score"] < 20
