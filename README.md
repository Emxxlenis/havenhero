# HavenHero

Estimación de exposición y refugio más cercano para un punto en Cali.

La demo deja elegir un lugar, muestra si pesa más la ladera o la inundación, y señala el refugio de demostración más cercano.

**Demo:** https://emxxlenis.github.io/havenhero/

El índice no es un mapa oficial de riesgo y no es el modelo de 2024. Es la decisión del proyecto, con zonas y refugios de ejemplo, para poder abrirla sin el catálogo original.

## Regla

La exposición de un punto es la cercanía a dos zonas ilustrativas. Gana la zona con mayor puntaje, de 0 a 100. El refugio es el de menor distancia en kilómetros.

`src/risk.py` y `docs/logic.js` implementan la misma regla. Los tests cubren el centro de cada zona.

## Run

```bash
python3 -m pytest -q tests/test_risk.py
node tests/logic.test.js
```
