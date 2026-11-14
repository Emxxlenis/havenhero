// Casos de negocio compartidos (tests/casos.json) contra la regla de la demo.
// Correr con: node --test tests/regla.test.js
"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const regla = require("../docs/regla.js");
const { evaluarTrabajo } = require("./paridad_runner.js");
const { casos } = JSON.parse(fs.readFileSync(path.join(__dirname, "casos.json"), "utf8"));

// Igual que conftest.contiene: lo esperado es un subconjunto del resultado.
function contiene(real, esperado) {
  if (Array.isArray(esperado)) {
    return Array.isArray(real) && real.length === esperado.length && esperado.every((e, i) => contiene(real[i], e));
  }
  if (esperado !== null && typeof esperado === "object") {
    return real !== null && typeof real === "object" && Object.keys(esperado).every((k) => k in real && contiene(real[k], esperado[k]));
  }
  return real === esperado;
}

for (const caso of casos) {
  test(caso.nombre, () => {
    const salida = evaluarTrabajo(caso);
    if (caso.espera_error) {
      assert.deepEqual(salida, { error: true });
      return;
    }
    assert.ok("ok" in salida, JSON.stringify(salida));
    assert.ok(contiene(salida.ok, caso.espera), JSON.stringify(salida.ok));
  });
}

test("el redondeo lleva las mitades hacia arriba", () => {
  assert.deepEqual([0, 0.49, 0.5, 1.5, 2.5, 99.5].map(regla.redondear), [0, 0, 1, 2, 3, 100]);
});

test("coordenadas no numéricas se rechazan", () => {
  for (const [lat, lon] of [[NaN, 0], [0, Infinity], ["3.4", -76.5], [null, 0], [undefined, 0], [true, 0]]) {
    assert.throws(() => regla.validarPunto(lat, lon), RangeError);
  }
});
