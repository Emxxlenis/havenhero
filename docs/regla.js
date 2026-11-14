// Regla de HavenHero para la demo estática.
//
// Es la misma regla del paquete Python `havenhero/` (distancia.py, indice.py,
// refugio_cercano.py, evaluacion.py). No tiene datos propios: recibe los de
// docs/datos.js, que se genera desde datos/. tests/test_paridad.py compara
// esta implementación con la de Python y falla si alguna cambia sola.
(function (raiz, fabrica) {
  if (typeof module === "object" && module.exports) {
    module.exports = fabrica();
  } else {
    raiz.HavenHeroRegla = fabrica();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // Mitades hacia arriba, para valores >= 0. Igual que distancia.redondear.
  function redondear(valor) {
    return Math.floor(valor + 0.5);
  }

  function validarPunto(lat, lon) {
    [["lat", lat, 90], ["lon", lon, 180]].forEach(function (terna) {
      var valor = terna[1];
      if (typeof valor !== "number" || !Number.isFinite(valor) || Math.abs(valor) > terna[2]) {
        throw new RangeError(terna[0] + " fuera de rango o no numérico: " + String(valor));
      }
    });
  }

  function radianes(grados) {
    return (grados * Math.PI) / 180;
  }

  function haversineKm(lat1, lon1, lat2, lon2, radioKm) {
    var fi1 = radianes(lat1);
    var fi2 = radianes(lat2);
    var dfi = radianes(lat2 - lat1);
    var dlambda = radianes(lon2 - lon1);
    var a = Math.pow(Math.sin(dfi / 2), 2) + Math.cos(fi1) * Math.cos(fi2) * Math.pow(Math.sin(dlambda / 2), 2);
    return 2 * radioKm * Math.asin(Math.sqrt(Math.min(1, a)));
  }

  function distanciaM(lat1, lon1, lat2, lon2, radioKm) {
    return redondear(haversineKm(lat1, lon1, lat2, lon2, radioKm) * 1000);
  }

  function puntajeDeZona(distanciaEnM, alcanceKm) {
    return redondear(Math.max(0, 100 * (1 - distanciaEnM / (alcanceKm * 1000))));
  }

  function nivelDe(puntaje, regla) {
    for (var i = 0; i < regla.niveles.length; i += 1) {
      if (puntaje >= regla.niveles[i].desde) return regla.niveles[i].id;
    }
    throw new RangeError("puntaje sin nivel: " + String(puntaje));
  }

  function compararTexto(a, b) {
    return a < b ? -1 : a > b ? 1 : 0;
  }

  function exposicion(lat, lon, zonas, regla) {
    var detalle = zonas.map(function (zona) {
      var metros = distanciaM(lat, lon, zona.lat, zona.lon, regla.radio_tierra_km);
      return { id: zona.id, tipo: zona.tipo, distancia_m: metros, puntaje: puntajeDeZona(metros, zona.alcance_km) };
    });
    var puntaje = detalle.reduce(function (mayor, z) {
      return Math.max(mayor, z.puntaje);
    }, 0);
    var dominantes = [];
    if (puntaje > 0) {
      dominantes = detalle
        .filter(function (z) {
          return z.puntaje === puntaje;
        })
        .map(function (z) {
          return z.id;
        })
        .sort(compararTexto);
    }
    return { puntaje: puntaje, nivel: nivelDe(puntaje, regla), dominantes: dominantes, zonas: detalle };
  }

  function refugioMasCercano(lat, lon, refugios, regla) {
    if (!refugios.length) return null;
    var medidos = refugios
      .map(function (refugio) {
        return { metros: distanciaM(lat, lon, refugio.lat, refugio.lon, regla.radio_tierra_km), refugio: refugio };
      })
      .sort(function (a, b) {
        return a.metros - b.metros || compararTexto(a.refugio.id, b.refugio.id);
      });
    var elegido = medidos[0];
    return {
      id: elegido.refugio.id,
      nombre: elegido.refugio.nombre,
      lat: elegido.refugio.lat,
      lon: elegido.refugio.lon,
      distancia_m: elegido.metros,
      empatados: medidos
        .slice(1)
        .filter(function (m) {
          return m.metros === elegido.metros;
        })
        .map(function (m) {
          return m.refugio.id;
        }),
    };
  }

  // datos: { zonas, refugios, regla } con la forma de docs/datos.js.
  function evaluar(lat, lon, datos) {
    validarPunto(lat, lon);
    var area = datos.regla.area_de_estudio;
    return {
      punto: { lat: lat, lon: lon },
      dentro_del_area: lat >= area.lat_min && lat <= area.lat_max && lon >= area.lon_min && lon <= area.lon_max,
      exposicion: exposicion(lat, lon, datos.zonas, datos.regla),
      refugio: refugioMasCercano(lat, lon, datos.refugios, datos.regla),
    };
  }

  return {
    redondear: redondear,
    validarPunto: validarPunto,
    haversineKm: haversineKm,
    distanciaM: distanciaM,
    puntajeDeZona: puntajeDeZona,
    nivelDe: nivelDe,
    exposicion: exposicion,
    refugioMasCercano: refugioMasCercano,
    evaluar: evaluar,
  };
});
