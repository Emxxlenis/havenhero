// Interfaz de la demo. No contiene regla ni datos: usa HavenHeroRegla
// (regla.js) y HAVENHERO_DATOS (datos.js, generado desde datos/).
(function () {
  "use strict";

  var datos = window.HAVENHERO_DATOS;
  var regla = window.HavenHeroRegla;
  var COLORES = { inundacion: "#2b6fd6", ladera: "#b46a1b", refugio: "#0f6b5c", punto: "#c2255c" };
  var PUNTO_INICIAL = datos.puntos_referencia[0];

  function el(id) {
    return document.getElementById(id);
  }

  function porId(lista, id) {
    return lista.filter(function (item) {
      return item.id === id;
    })[0];
  }

  function textoDistancia(metros) {
    if (metros < 1000) return metros + " m";
    return (metros / 1000).toFixed(2).replace(".", ",") + " km";
  }

  function etiquetaTipo(tipo) {
    return datos.tipos[tipo] || tipo;
  }

  // Acepta coma o punto decimal. Devuelve NaN si el texto no es un número.
  function leerNumero(texto) {
    var limpio = String(texto).trim().replace(",", ".");
    return /^-?\d+(\.\d+)?$/.test(limpio) ? Number(limpio) : NaN;
  }

  // --- Mapa (opcional: sin Leaflet la página sigue funcionando con el formulario)
  var mapa = null;
  var capaSeleccion = null;

  function iniciarMapa() {
    if (typeof L === "undefined") {
      var caja = el("mapa");
      caja.classList.add("mapa-sin-conexion");
      caja.textContent = "No se pudo cargar el mapa. Podés evaluar un punto con el formulario de coordenadas.";
      return;
    }
    var area = datos.regla.area_de_estudio;
    var limites = [
      [area.lat_min, area.lon_min],
      [area.lat_max, area.lon_max],
    ];
    mapa = L.map("mapa").fitBounds(limites);
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(mapa);
    L.rectangle(limites, { color: "#55636e", weight: 1, dashArray: "4 4", fill: false, interactive: false }).addTo(mapa);

    datos.zonas.forEach(function (zona) {
      L.circle([zona.lat, zona.lon], {
        radius: zona.alcance_km * 1000,
        color: COLORES[zona.tipo] || "#55636e",
        weight: 1.5,
        fillOpacity: 0.06,
        interactive: false,
      }).addTo(mapa);
      L.circleMarker([zona.lat, zona.lon], { radius: 4, color: COLORES[zona.tipo] || "#55636e", fillOpacity: 1 })
        .addTo(mapa)
        .bindTooltip(zona.nombre + " (centro)");
    });

    datos.refugios.forEach(function (refugio) {
      L.circleMarker([refugio.lat, refugio.lon], { radius: 7, color: COLORES.refugio, fillOpacity: 0.85 })
        .addTo(mapa)
        .bindTooltip(refugio.nombre);
    });

    capaSeleccion = L.layerGroup().addTo(mapa);
    mapa.on("click", function (evento) {
      mostrar(evento.latlng.lat, evento.latlng.lng);
    });
  }

  function dibujarSeleccion(resultado) {
    if (!mapa) return;
    var punto = [resultado.punto.lat, resultado.punto.lon];
    capaSeleccion.clearLayers();
    if (resultado.refugio) {
      L.polyline([punto, [resultado.refugio.lat, resultado.refugio.lon]], {
        color: COLORES.refugio,
        weight: 2,
        dashArray: "6 6",
      }).addTo(capaSeleccion);
    }
    L.circleMarker(punto, { radius: 8, color: COLORES.punto, fillOpacity: 1 }).addTo(capaSeleccion);
    if (!mapa.getBounds().contains(punto)) mapa.panTo(punto);
  }

  // --- Resultado
  function escribirExposicion(exposicion) {
    var nivel = porId(datos.regla.niveles, exposicion.nivel);
    el("puntaje").textContent = String(exposicion.puntaje);
    el("nivel").textContent = "Nivel del índice de demostración: " + (nivel ? nivel.etiqueta : exposicion.nivel);

    var nombres = exposicion.dominantes.map(function (id) {
      return etiquetaTipo(porId(datos.zonas, id).tipo);
    });
    if (!nombres.length) {
      el("amenaza").textContent = "Ninguna zona de demostración alcanza este punto. Eso no significa que el lugar sea seguro.";
    } else if (nombres.length === 1) {
      el("amenaza").textContent = "Pesa más: " + nombres[0] + ".";
    } else {
      el("amenaza").textContent = "Empate entre zonas: " + nombres.join(" y ") + ".";
    }

    var cuerpo = el("detalle-zonas");
    cuerpo.textContent = "";
    exposicion.zonas.forEach(function (zona) {
      var fila = document.createElement("tr");
      [porId(datos.zonas, zona.id).nombre, textoDistancia(zona.distancia_m), String(zona.puntaje)].forEach(function (texto) {
        var celda = document.createElement("td");
        celda.textContent = texto;
        fila.appendChild(celda);
      });
      cuerpo.appendChild(fila);
    });
  }

  function escribirRefugio(refugio) {
    if (!refugio) {
      el("refugio-nombre").textContent = "Sin refugios cargados";
      el("refugio-distancia").textContent = "No hay ningún refugio en los datos, así que no se puede sugerir uno.";
      el("refugio-empate").textContent = "";
      return;
    }
    el("refugio-nombre").textContent = refugio.nombre;
    el("refugio-distancia").textContent = "A " + textoDistancia(refugio.distancia_m) + " en línea recta.";
    var otros = refugio.empatados.map(function (id) {
      return porId(datos.refugios, id).nombre;
    });
    el("refugio-empate").textContent = otros.length ? "A la misma distancia: " + otros.join(", ") + "." : "";
  }

  function mostrarError(mensaje) {
    el("error").textContent = mensaje;
    el("error").hidden = !mensaje;
  }

  function mostrar(lat, lon) {
    var resultado;
    try {
      resultado = regla.evaluar(lat, lon, datos);
    } catch (error) {
      mostrarError("Coordenadas no válidas. La latitud va de -90 a 90 y la longitud de -180 a 180.");
      return;
    }
    mostrarError("");
    el("lat").value = lat.toFixed(5);
    el("lon").value = lon.toFixed(5);
    escribirExposicion(resultado.exposicion);
    escribirRefugio(resultado.refugio);
    el("fuera-del-area").hidden = resultado.dentro_del_area;
    dibujarSeleccion(resultado);
  }

  // --- Controles
  el("formulario").addEventListener("submit", function (evento) {
    evento.preventDefault();
    mostrar(leerNumero(el("lat").value), leerNumero(el("lon").value));
  });

  datos.puntos_referencia.forEach(function (punto) {
    var boton = document.createElement("button");
    boton.type = "button";
    boton.textContent = punto.nombre;
    boton.addEventListener("click", function () {
      mostrar(punto.lat, punto.lon);
    });
    el("puntos-referencia").appendChild(boton);
  });

  iniciarMapa();
  mostrar(PUNTO_INICIAL.lat, PUNTO_INICIAL.lon);
})();
