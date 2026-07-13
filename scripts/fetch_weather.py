#!/usr/bin/env python3
"""
Weather Data Pipeline — Extracción de datos climáticos históricos
API: Open-Meteo (gratis, sin API key)
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import os
import sys

# ─── Ciudades para analizar ───────────────────────────────────────────
# (lat, lon, nombre, país)
CIUDADES = [
    (9.9281, -84.0907, "San José", "Costa Rica"),
    (40.4168, -3.7038, "Madrid", "España"),
    (48.8566, 2.3522, "Paris", "Francia"),
    (51.5074, -0.1278, "London", "Reino Unido"),
    (40.7128, -74.0060, "New York", "EE.UU."),
    (25.7617, -80.1918, "Miami", "EE.UU."),
    (-23.5505, -46.6333, "São Paulo", "Brasil"),
    (19.0760, 72.8777, "Mumbai", "India"),
    (35.6762, 139.6503, "Tokyo", "Japón"),
    (-33.8688, 151.2093, "Sydney", "Australia"),
]

# Variables climáticas a extraer
VARS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "precipitation_sum",
    "rain_sum",
    "precipitation_hours",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
]

# Rango de fechas: últimos 12 meses
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=365)

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch_city(lat, lon, name, country):
    """Extrae datos climáticos históricos para una ciudad."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE.strftime("%Y-%m-%d"),
        "end_date": END_DATE.strftime("%Y-%m-%d"),
        "daily": ",".join(VARS),
        "timezone": "auto",
    }

    print(f"  → Extrayendo: {name}, {country}...", end=" ")
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        print("✅ OK")
        return data
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def parse_to_df(raw_data, city_name, country):
    """Convierte la respuesta JSON a DataFrame."""
    if not raw_data or "daily" not in raw_data:
        return None

    daily = raw_data["daily"]
    dates = daily.get("time", [])

    records = []
    for i, date in enumerate(dates):
        record = {
            "date": date,
            "city": city_name,
            "country": country,
            "latitude": raw_data["latitude"],
            "longitude": raw_data["longitude"],
            "elevation": raw_data.get("elevation", 0),
        }
        for var in VARS:
            values = daily.get(var, [])
            record[var] = values[i] if i < len(values) else None
        records.append(record)

    return pd.DataFrame(records)


def main():
    print(f"\n{'='*60}")
    print("🌤️  WEATHER DATA PIPELINE — Extracción de datos")
    print(f"📅 Rango: {START_DATE.strftime('%Y-%m-%d')} → {END_DATE.strftime('%Y-%m-%d')}")
    print(f"🌍 Ciudades: {len(CIUDADES)}")
    print(f"{'='*60}\n")

    all_dfs = []
    for lat, lon, name, country in CIUDADES:
        raw = fetch_city(lat, lon, name, country)
        df = parse_to_df(raw, name, country)
        if df is not None:
            all_dfs.append(df)

    if not all_dfs:
        print("\n❌ No se pudieron extraer datos. Revisá conexión.")
        sys.exit(1)

    # Combinar todo
    final_df = pd.concat(all_dfs, ignore_index=True)
    final_df["date"] = pd.to_datetime(final_df["date"])
    final_df["month"] = final_df["date"].dt.month
    final_df["year"] = final_df["date"].dt.year
    final_df["season"] = final_df["month"].apply(
        lambda m: "Verano" if m in [12, 1, 2] else
                  "Primavera" if m in [3, 4, 5] else
                  "Verano (NH)" if m in [6, 7, 8] else "Otoño"
    )

    # Guardar
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "weather_data.csv")
    final_df.to_csv(output_path, index=False)
    print(f"\n💾 Datos guardados: {output_path}")
    print(f"📊 Registros: {len(final_df):,}")
    print(f"🏙️  Ciudades: {final_df['city'].nunique()}")
    print(f"📅 Días únicos: {final_df['date'].nunique()}")
    print(f"\n✅ Extracción completada exitosamente.\n")

    # Mostrar resumen rápido
    print("📋 Primeras filas:")
    print(final_df.head(10).to_string(index=False))

    return final_df


if __name__ == "__main__":
    main()
