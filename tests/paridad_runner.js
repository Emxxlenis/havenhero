// Evalúa una lista de trabajos con la regla y los datos que usa la demo
// (docs/regla.js + docs/datos.js). Lee JSON por stdin y escribe JSON por stdout.
// Lo usan tests/test_paridad.py y tests/regla.test.js.
"use strict";

const path = require("node:path");
const regla = require(path.join(__dirname, "..", "docs", "regla.js"));
const datos = require(path.join(__dirname, "..", "docs", "datos.js"));

function evaluarTrabajo(trabajo) {
  const propios = {
    zonas: "zonas" in trabajo ? trabajo.zonas : datos.zonas,
    refugios: "refugios" in trabajo ? trabajo.refugios : datos.refugios,
    regla: datos.regla,
  };
  try {
    return { ok: regla.evaluar(trabajo.lat, trabajo.lon, propios) };
  } catch (error) {
    if (error instanceof RangeError) return { error: true };
    throw error;
  }
}

module.exports = { evaluarTrabajo };

if (require.main === module) {
  let entrada = "";
  process.stdin.setEncoding("utf8");
  process.stdin.on("data", (trozo) => (entrada += trozo));
  process.stdin.on("end", () => {
    process.stdout.write(JSON.stringify(JSON.parse(entrada).map(evaluarTrabajo)));
  });
}
