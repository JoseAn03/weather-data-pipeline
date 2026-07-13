#!/usr/bin/env python3
"""
Weather Data Pipeline — Ejecución completa
1. Extraer datos de la API
2. Analizar y generar visualizaciones
3. Construir dashboard

Uso: python run_all.py
"""

import os
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DASHBOARD_DIR, exist_ok=True)


def run_step(script_name, label):
    """Ejecuta un script del pipeline."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    print(f"\n{'='*60}")
    print(f"🚀 PASO: {label}")
    print(f"{'='*60}")

    result = subprocess.run(
        [sys.executable, script_path],
        capture_output=False,
        cwd=BASE_DIR
    )
    return result.returncode == 0


def main():
    print(f"\n{'='*60}")
    print("🌤️  WEATHER DATA PIPELINE — Pipeline Completo")
    print(f"{'='*60}")

    steps = [
        ("fetch_weather.py", "Extracción de datos desde Open-Meteo API"),
        ("analysis.py", "Análisis exploratorio y visualizaciones"),
        ("build_dashboard.py", "Dashboard interactivo"),
    ]

    success = True
    for script, label in steps:
        if not run_step(script, label):
            print(f"\n❌ Error en: {label}")
            success = False
            break

    if success:
        print(f"\n{'='*60}")
        print("🎉 PIPELINE COMPLETADO EXITOSAMENTE")
        print(f"{'='*60}")
        print(f"\n📂 Estructura del proyecto:")
        print(f"   📊 data/weather_data.csv — Datos crudos")
        print(f"   📈 outputs/ — 5 gráficos + insights")
        print(f"   📊 dashboard/index.html — Dashboard interactivo")
        print(f"\n🚀 Para ver el dashboard:")
        print(f"   Abrí: dashboard/index.html en tu navegador")
    else:
        print("\n❌ Pipeline falló. Revisá los errores arriba.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
