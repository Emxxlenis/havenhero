// ARCHIVO GENERADO. No editar a mano.
// Fuente: datos/*.json. Regenerar con: python3 -m havenhero generar-demo
// Todo el contenido es de demostración: zonas, refugios, umbrales y área.
var HAVENHERO_DATOS = {
  "tipos": {
    "inundacion": "Inundación",
    "ladera": "Ladera"
  },
  "zonas": [
    {
      "id": "inundacion-oriente",
      "tipo": "inundacion",
      "nombre": "Zona de demostración de inundación (oriente)",
      "lat": 3.41,
      "lon": -76.49,
      "alcance_km": 9.0
    },
    {
      "id": "ladera-occidente",
      "tipo": "ladera",
      "nombre": "Zona de demostración de ladera (occidente)",
      "lat": 3.43,
      "lon": -76.57,
      "alcance_km": 7.0
    }
  ],
  "refugios": [
    {
      "id": "refugio-centro",
      "nombre": "Refugio de demostración Centro",
      "lat": 3.452,
      "lon": -76.532
    },
    {
      "id": "refugio-norte",
      "nombre": "Refugio de demostración Norte",
      "lat": 3.478,
      "lon": -76.527
    },
    {
      "id": "refugio-sur",
      "nombre": "Refugio de demostración Sur",
      "lat": 3.395,
      "lon": -76.54
    },
    {
      "id": "refugio-oriente",
      "nombre": "Refugio de demostración Oriente",
      "lat": 3.408,
      "lon": -76.485
    },
    {
      "id": "refugio-ladera",
      "nombre": "Refugio de demostración Ladera",
      "lat": 3.428,
      "lon": -76.568
    }
  ],
  "regla": {
    "radio_tierra_km": 6371.0,
    "niveles": [
      {
        "id": "alto",
        "etiqueta": "Alto",
        "desde": 67
      },
      {
        "id": "medio",
        "etiqueta": "Medio",
        "desde": 34
      },
      {
        "id": "bajo",
        "etiqueta": "Bajo",
        "desde": 1
      },
      {
        "id": "fuera_de_alcance",
        "etiqueta": "Fuera del alcance de las zonas",
        "desde": 0
      }
    ],
    "area_de_estudio": {
      "lat_min": 3.3,
      "lat_max": 3.52,
      "lon_min": -76.62,
      "lon_max": -76.44
    }
  },
  "puntos_referencia": [
    {
      "id": "aguablanca",
      "nombre": "Aguablanca",
      "lat": 3.408,
      "lon": -76.49
    },
    {
      "id": "centro",
      "nombre": "Centro",
      "lat": 3.452,
      "lon": -76.532
    },
    {
      "id": "siloe",
      "nombre": "Siloé",
      "lat": 3.428,
      "lon": -76.568
    },
    {
      "id": "norte",
      "nombre": "Norte",
      "lat": 3.478,
      "lon": -76.527
    }
  ]
};
if (typeof module === "object" && module.exports) {
  module.exports = HAVENHERO_DATOS;
}
