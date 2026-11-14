const ZONES = [
  { id: "flood", name: "Inundación", lat: 3.41, lon: -76.49, reachKm: 9 },
  { id: "hill", name: "Ladera", lat: 3.43, lon: -76.57, reachKm: 7 },
];

const SHELTERS = [
  { name: "Refugio Centro", lat: 3.452, lon: -76.532 },
  { name: "Refugio Norte", lat: 3.478, lon: -76.527 },
  { name: "Refugio Sur", lat: 3.395, lon: -76.54 },
  { name: "Refugio Oriente", lat: 3.408, lon: -76.485 },
  { name: "Refugio Ladera", lat: 3.428, lon: -76.568 },
];

function haversineKm(lat1, lon1, lat2, lon2) {
  const radius = 6371;
  const p1 = (lat1 * Math.PI) / 180;
  const p2 = (lat2 * Math.PI) / 180;
  const dphi = ((lat2 - lat1) * Math.PI) / 180;
  const dlmb = ((lon2 - lon1) * Math.PI) / 180;
  const a = Math.sin(dphi / 2) ** 2 + Math.cos(p1) * Math.cos(p2) * Math.sin(dlmb / 2) ** 2;
  return 2 * radius * Math.asin(Math.sqrt(a));
}

function exposure(lat, lon) {
  const parts = ZONES.map((zone) => {
    const distance = haversineKm(lat, lon, zone.lat, zone.lon);
    const score = Math.round(Math.max(0, 100 * (1 - distance / zone.reachKm)));
    return { id: zone.id, name: zone.name, km: Math.round(distance * 100) / 100, score };
  });
  const dominant = parts.reduce((best, item) => (item.score > best.score ? item : best));
  return { score: dominant.score, hazard: dominant.name, parts };
}

function nearestShelter(lat, lon) {
  return SHELTERS.map((shelter) => ({
    ...shelter,
    km: Math.round(haversineKm(lat, lon, shelter.lat, shelter.lon) * 100) / 100,
  })).sort((a, b) => a.km - b.km)[0];
}

if (typeof module !== "undefined") {
  module.exports = { exposure, nearestShelter, ZONES, SHELTERS };
}
