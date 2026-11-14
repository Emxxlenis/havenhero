# HavenHero

Para un punto en Cali, HavenHero estima qué exposición pesa más, ladera o inundación, y señala el refugio más cercano.

**Demo:** https://emxxlenis.github.io/havenhero/

Los datos que trae este repositorio son de demostración. La regla es real y está probada; las zonas, los refugios y los umbrales son ejemplos. La sección [Qué es demostración y qué no](#qué-es-demostración-y-qué-no) lo detalla.

## Problema

Cuando llueve fuerte en Cali, quien coordina una respuesta (una junta de acción comunal, un organismo de socorro, una línea de atención) recibe una ubicación y tiene que resolver dos cosas rápido: qué tipo de exposición pesa más según dónde está, y a qué refugio remitirla. Hacerlo de memoria o buscando en varios mapas a la vez es lento y cambia según quién atienda.

## Decisión que responde

Dado un punto (latitud y longitud), HavenHero entrega:

1. **Exposición**: un índice de 0 a 100, su nivel (alto, medio, bajo o fuera de alcance) y qué zona lo explica, ladera o inundación. Incluye el desglose por zona.
2. **Refugio más cercano**: nombre y distancia en línea recta. Si hay otros refugios a la misma distancia, los lista.
3. **Avisos que cambian la decisión**: si el punto queda fuera del área cubierta, si ninguna zona lo alcanza, o si no hay refugios cargados.

Es un apoyo para decidir. No reemplaza a quien decide ni a las autoridades de gestión del riesgo.

## Qué es demostración y qué no

| Parte | Estado |
|---|---|
| Zonas (`datos/zonas.json`) | **Demostración.** Dos círculos trazados a mano. No vienen de un mapa de amenaza ni de un estudio técnico. |
| Refugios (`datos/refugios.json`) | **Demostración.** Nombres y coordenadas ficticios. No son albergues reales. |
| Umbrales de nivel y rectángulo del área (`datos/regla.json`) | **Demostración.** Elecciones para que la demo sea legible; no son criterios técnicos ni el límite del municipio. |
| Puntos de referencia (`datos/puntos_referencia.json`) | **Demostración.** Coordenadas aproximadas para moverse por el mapa. |
| Forma del índice (caída lineal con la distancia al centro de la zona) | **Demostración.** Es un índice de cercanía. No es una probabilidad, no usa lluvia, pendiente, suelos ni registros de eventos, y no predice nada. |
| Distancia (haversine, metros enteros), elección del refugio y desempate | **Real.** Es la regla del producto y está cubierta por pruebas. |
| Validación de entradas y de archivos de datos | **Real.** |
| Mapa base | OpenStreetMap, servido por sus teselas públicas. |

HavenHero no es un mapa oficial del IDEAM, de la UNGRD ni de la Alcaldía de Cali, y no usa datos de esas entidades. El repositorio no contiene ningún modelo entrenado ni datos históricos de eventos o víctimas. Un índice de 0 significa que el punto queda fuera del alcance de las zonas de ejemplo, no que el lugar sea seguro.

Para usarlo en una operación real hay que reemplazar los archivos de `datos/` por información validada por quien tenga la competencia, y revisar si la forma del índice sirve para esa información. El código no cambia.

## La regla

Hay una sola regla y está escrita así:

- **Distancia.** Haversine con el radio terrestre de `datos/regla.json`, redondeada a metros enteros. Toda la regla trabaja con esa distancia en metros.
- **Puntaje de una zona.** `100 * (1 - distancia / alcance)`, con piso en 0, redondeado al entero más cercano con las mitades hacia arriba. Vale 100 en el centro de la zona y 0 desde el borde de su alcance hacia afuera.
- **Exposición del punto.** El puntaje más alto entre las zonas. Las zonas que lo alcanzan son las dominantes; si empatan, se informan todas en orden alfabético de id. Con puntaje 0 no hay zona dominante.
- **Nivel.** El primer nivel de `datos/regla.json` cuyo umbral alcanza el puntaje.
- **Refugio más cercano.** El de menor distancia en metros. Dos refugios empatan cuando quedan a los mismos metros enteros; gana el de id alfabéticamente menor, para que el resultado no dependa del orden del archivo, y los demás se listan como empatados. Sin refugios, el resultado es vacío y no se inventa uno.
- **Área.** Si el punto cae fuera del rectángulo de `datos/regla.json`, se calcula igual y se marca como fuera del área.
- **Entradas.** Latitud y longitud deben ser números finitos dentro de rango; si no, se rechaza el punto.

## Arquitectura

```
datos/                    Fuente de los datos (JSON). Se edita acá y solo acá.
  zonas.json
  refugios.json
  regla.json
  puntos_referencia.json
havenhero/                Regla en Python.
  zonas.py                Carga y valida zonas.
  refugios.py             Carga y valida refugios.
  regla.py                Carga y valida parámetros: radio, niveles, área.
  distancia.py            Haversine, metros enteros, redondeo, validación del punto.
  indice.py               Puntaje por zona, exposición y nivel.
  refugio_cercano.py      Refugio más cercano y desempate.
  evaluacion.py           evaluar(lat, lon): junta lo anterior.
  demo.py                 Genera docs/datos.js desde datos/.
  __main__.py             Línea de comandos.
docs/                     Demo estática (GitHub Pages).
  index.html, estilos.css
  datos.js                GENERADO desde datos/. No se edita a mano.
  regla.js                La misma regla, en JS, sin datos propios.
  app.js                  Interfaz y mapa Leaflet. Sin regla ni datos.
tests/
  casos.json              Casos de negocio compartidos por Python y JS.
  test_*.py               Pruebas de Python, paridad y demo.
  regla.test.js           Los mismos casos contra docs/regla.js.
  paridad_runner.js       Evalúa puntos con la regla y los datos de la demo.
```

### Por qué hay dos implementaciones y cómo se mantienen iguales

La demo se publica como página estática y también se abre con doble clic, sin servidor. Eso obliga a que la regla corra en el navegador, así que existe en Python (`havenhero/`) y en JS (`docs/regla.js`). Para que no diverjan:

- **Los datos tienen una sola fuente.** `docs/datos.js` se genera desde `datos/` con `python3 -m havenhero generar-demo`. Una prueba falla si el archivo publicado no coincide byte a byte con lo que se generaría hoy.
- **La regla se compara resultado contra resultado.** `tests/test_paridad.py` evalúa 1458 puntos (una grilla sobre Cali, puntos al azar con semilla fija en la ciudad y en todo el planeta, extremos del rango y todos los casos borde) con Python y con `docs/regla.js`, y exige que los resultados completos sean idénticos. Si no hay `node`, la prueba falla en vez de saltarse.
- **Los casos de negocio son compartidos.** `tests/casos.json` lo corren pytest y node contra la misma expectativa.
- **La interfaz no puede esconder regla.** Una prueba revisa que `docs/app.js` no tenga coordenadas, alcances ni trigonometría propios.

Las dos implementaciones redondean con la misma función explícita (mitades hacia arriba), porque el `round` de Python y el `Math.round` de JS no coinciden en las mitades. La regla opera sobre metros enteros para que una diferencia en el último bit de una función trigonométrica entre lenguajes no cambie el resultado.

## Cómo correr las pruebas

Hace falta Python 3.10 o posterior con `pytest`, y Node 18 o posterior. No hay más dependencias.

```bash
python3 -m pytest -q                # regla, datos, casos borde, paridad Python/JS y demo
node --test tests/regla.test.js     # casos borde contra la regla de la demo
```

`pytest` invoca a `node` para la prueba de paridad, así que el primer comando ya cubre los dos lenguajes. El segundo sirve para trabajar solo sobre el JS.

Casos borde cubiertos: punto lejos de las zonas, punto en otra ciudad, punto encima del centro de una zona, punto encima de un refugio, empate de distancia entre dos y tres refugios, empate de puntaje entre zonas, borde del alcance, sin refugios, sin zonas y coordenadas inválidas.

## Cómo usarlo desde Python

```bash
python3 -m havenhero evaluar 3.408 -76.49
```

```python
from havenhero import evaluar

resultado = evaluar(3.408, -76.49)
resultado["exposicion"]["puntaje"]   # 98
resultado["refugio"]["id"]           # "refugio-oriente"
```

## Cómo correr la demo

Abrir `docs/index.html` en el navegador alcanza. Si se prefiere un servidor local:

```bash
python3 -m http.server --directory docs 8000
```

y abrir http://localhost:8000. La demo no usa claves ni cuentas: el mapa es Leaflet con teselas de OpenStreetMap, y necesita conexión para dibujarlo. Sin conexión, el formulario de coordenadas sigue funcionando.

GitHub Pages publica la carpeta `docs/` tal cual.

## Cómo cambiar los datos

1. Editar el JSON correspondiente en `datos/`.
2. Regenerar el archivo de la demo: `python3 -m havenhero generar-demo`.
3. Correr `python3 -m pytest -q`.

Si se omite el paso 2, las pruebas fallan. `python3 -m havenhero generar-demo --comprobar` hace solo esa verificación.

## Límites conocidos

- La distancia es en línea recta. No considera vías, pendiente, ríos, puentes ni si el camino está transitable durante el evento.
- Los refugios no tienen capacidad, horario ni estado. El más cercano puede estar lleno o cerrado.
- Las zonas son círculos. Una amenaza real no tiene esa forma.
- El refugio se elige solo por distancia; no se descarta uno que esté dentro de una zona de alta exposición.
