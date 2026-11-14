const { exposure, nearestShelter } = require("../docs/logic");

const flood = exposure(3.41, -76.49);
if (flood.hazard !== "Inundación" || flood.score !== 100) {
  throw new Error("flood center " + JSON.stringify(flood));
}
if (nearestShelter(3.41, -76.49).name !== "Refugio Oriente") {
  throw new Error("nearest flood");
}
const hill = exposure(3.43, -76.57);
if (hill.hazard !== "Ladera" || nearestShelter(3.43, -76.57).name !== "Refugio Ladera") {
  throw new Error("hill");
}
if (exposure(3.9, -76.2).score >= 20) throw new Error("far point");
console.log("haven logic ok");
