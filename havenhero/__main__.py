"""Línea de comandos: ``python3 -m havenhero evaluar LAT LON`` y ``generar-demo``."""

from __future__ import annotations

import argparse
import json
import sys

from havenhero import demo
from havenhero.evaluacion import evaluar


def main(argumentos: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="havenhero", description="Exposición de demostración y refugio más cercano.")
    comandos = parser.add_subparsers(dest="comando", required=True)
    p_evaluar = comandos.add_parser("evaluar", help="evalúa un punto y escribe el resultado en JSON")
    p_evaluar.add_argument("lat", type=float)
    p_evaluar.add_argument("lon", type=float)
    p_demo = comandos.add_parser("generar-demo", help="regenera docs/datos.js desde datos/")
    p_demo.add_argument("--comprobar", action="store_true", help="no escribe; falla si docs/datos.js quedó viejo")
    args = parser.parse_args(argumentos)

    if args.comando == "evaluar":
        try:
            resultado = evaluar(args.lat, args.lon)
        except ValueError as error:
            print(f"error: {error}", file=sys.stderr)
            return 2
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
        return 0

    if args.comprobar:
        if demo.esta_al_dia():
            print("docs/datos.js está al día")
            return 0
        print("docs/datos.js no coincide con datos/. Corré: python3 -m havenhero generar-demo", file=sys.stderr)
        return 1
    demo.escribir()
    print(f"escrito {demo.RUTA_DATOS_JS.relative_to(demo.RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
