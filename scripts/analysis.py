#!/usr/bin/env python3
"""
Weather Data Pipeline — Análisis exploratorio de datos (EDA)
Genera tablas, estadísticas y visualizaciones.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuración visual
plt.style.use("seaborn-v0_8-darkgrid")
sns.set_palette("viridis")
plt.rcParams["figure.figsize"] = (14, 8)
plt.rcParams["font.size"] = 12

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "weather_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data():
    """Carga y prepara los datos."""
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    print(f"📂 Datos cargados: {len(df):,} registros, {df['city'].nunique()} ciudades")

    # Métricas derivadas
    df["temp_range"] = df["temperature_2m_max"] - df["temperature_2m_min"]
    df["is_rainy"] = df["precipitation_sum"] > 0
    df["is_hot"] = df["temperature_2m_max"] > 30
    df["is_cold"] = df["temperature_2m_max"] < 10
    df["month_name"] = df["date"].dt.strftime("%B")

    return df


def summary_stats(df):
    """Estadísticas generales."""
    print("\n" + "="*60)
    print("📊 RESUMEN ESTADÍSTICO GLOBAL")
    print("="*60)

    numeric_cols = [
        "temperature_2m_max", "temperature_2m_min", "temperature_2m_mean",
        "precipitation_sum", "rain_sum", "precipitation_hours",
        "wind_speed_10m_max", "wind_gusts_10m_max"
    ]

    print(df[numeric_cols].describe().round(2).to_string())
    return df[numeric_cols].describe()


def by_city_summary(df):
    """Resumen por ciudad."""
    print("\n" + "="*60)
    print("🏙️  RESUMEN POR CIUDAD")
    print("="*60)

    city_stats = df.groupby("city").agg({
        "temperature_2m_mean": ["mean", "std", "min", "max"],
        "precipitation_sum": ["sum", "mean"],
        "rain_sum": "sum",
        "precipitation_hours": "sum",
        "wind_speed_10m_max": "max",
        "is_rainy": "mean",
        "is_hot": "mean",
        "is_cold": "mean",
    }).round(2)

    city_stats.columns = [
        "Temp Media °C", "Temp Std", "Temp Mín", "Temp Máx",
        "Precip Total mm", "Precip Promedio",
        "Lluvia Total mm", "Horas Precip",
        "Viento Máx km/h", "% Días Lluvia", "% Días Calor", "% Días Frío"
    ]

    print(city_stats.to_string())
    return city_stats


def plot_temperature_comparison(df):
    """Gráfico: Comparación de temperaturas por ciudad."""
    fig, ax = plt.subplots(figsize=(14, 7))

    avg_temps = df.groupby("city")["temperature_2m_mean"].mean().sort_values()

    colors = ["#e74c3c" if t > 25 else "#3498db" if t < 15 else "#f39c12"
              for t in avg_temps.values]

    bars = ax.barh(avg_temps.index, avg_temps.values, color=colors, edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, avg_temps.values):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                f"{val:.1f}°C", va="center", fontsize=11, fontweight="bold")

    ax.set_xlabel("Temperatura Media (°C)", fontsize=13)
    ax.set_title("🌡️ Temperatura Media Anual por Ciudad", fontsize=16, fontweight="bold")
    ax.set_xlim(0, avg_temps.max() + 5)
    ax.tick_params(axis="y", labelsize=11)

    # Línea de referencia 20°C
    ax.axvline(x=20, color="gray", linestyle="--", alpha=0.5, label="20°C")
    ax.legend()

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "01_temp_comparison.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Gráfico guardado: {path}")
    return path


def plot_precipitation_heatmap(df):
    """Heatmap: Precipitación por ciudad y mes."""
    pivot = df.pivot_table(
        values="precipitation_sum",
        index="city",
        columns="month_name",
        aggfunc="sum",
        fill_value=0
    )

    # Ordenar meses
    month_order = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    pivot = pivot[[m for m in month_order if m in pivot.columns]]

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues",
                linewidths=0.5, cbar_kws={"label": "Precipitación (mm)"},
                ax=ax)

    ax.set_title("🌧️ Precipitación Total por Ciudad y Mes (mm)", fontsize=16, fontweight="bold")
    ax.set_xlabel("Mes", fontsize=13)
    ax.set_ylabel("Ciudad", fontsize=13)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "02_precip_heatmap.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Gráfico guardado: {path}")
    return path


def plot_seasonal_patterns(df):
    """Gráfico: Patrón estacional de temperatura para ciudades clave."""
    key_cities = ["San José", "New York", "London", "Tokyo", "Sydney"]
    plot_df = df[df["city"].isin(key_cities)]

    monthly = plot_df.groupby(["city", "month_name"])["temperature_2m_mean"].mean().reset_index()
    monthly["month_num"] = monthly["month_name"].apply(
        lambda m: ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"].index(m) + 1
    )
    monthly = monthly.sort_values("month_num")

    fig, ax = plt.subplots(figsize=(16, 8))
    palette = {"San José": "#e74c3c", "New York": "#2ecc71",
               "London": "#3498db", "Tokyo": "#9b59b6", "Sydney": "#f39c12"}

    for city in key_cities:
        city_data = monthly[monthly["city"] == city]
        ax.plot(city_data["month_num"], city_data["temperature_2m_mean"],
                marker="o", linewidth=2.5, markersize=6,
                label=city, color=palette.get(city))

    ax.set_xlabel("Mes", fontsize=13)
    ax.set_ylabel("Temperatura Media (°C)", fontsize=13)
    ax.set_title("📈 Patrón Estacional de Temperatura", fontsize=16, fontweight="bold")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                       "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"])
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "03_seasonal_patterns.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Gráfico guardado: {path}")
    return path


def plot_wind_storm_chart(df):
    """Gráfico: Velocidad máxima de viento por ciudad."""
    wind_max = df.groupby("city")["wind_speed_10m_max"].max().sort_values()

    fig, ax = plt.subplots(figsize=(14, 7))
    colors = plt.cm.YlOrRd(wind_max.values / wind_max.max())

    bars = ax.barh(wind_max.index, wind_max.values, color=colors, edgecolor="white")

    for bar, val in zip(bars, wind_max.values):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f"{val:.0f} km/h", va="center", fontsize=11, fontweight="bold")

    ax.set_xlabel("Velocidad Máxima del Viento (km/h)", fontsize=13)
    ax.set_title("💨 Ráfaga Máxima de Viento por Ciudad", fontsize=16, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "04_wind_max.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Gráfico guardado: {path}")
    return path


def plot_rain_vs_temp(df):
    """Scatter: Relación precipitación vs temperatura."""
    city_avg = df.groupby("city").agg({
        "temperature_2m_mean": "mean",
        "precipitation_sum": "sum",
        "temp_range": "mean",
    }).reset_index()

    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = ax.scatter(
        city_avg["temperature_2m_mean"],
        city_avg["precipitation_sum"],
        s=city_avg["temp_range"] * 30,
        c=city_avg["precipitation_sum"],
        cmap="Blues",
        alpha=0.7,
        edgecolors="white",
        linewidth=1
    )

    # Etiquetas
    for _, row in city_avg.iterrows():
        ax.annotate(
            row["city"],
            (row["temperature_2m_mean"], row["precipitation_sum"]),
            fontsize=10,
            ha="center",
            va="bottom",
            fontweight="bold"
        )

    ax.set_xlabel("Temperatura Media (°C)", fontsize=13)
    ax.set_ylabel("Precipitación Total Anual (mm)", fontsize=13)
    ax.set_title("🌡️🌧️ Relación Temperatura vs Precipitación", fontsize=16, fontweight="bold")

    cbar = plt.colorbar(scatter)
    cbar.set_label("Precipitación (mm)", fontsize=12)

    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "05_rain_vs_temp.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✅ Gráfico guardado: {path}")
    return path


def generate_insights(df):
    """Genera insights clave en texto."""
    print("\n" + "="*60)
    print("💡 INSIGHTS CLAVE")
    print("="*60)

    city_temp = df.groupby("city")["temperature_2m_mean"].mean()
    city_rain = df.groupby("city")["precipitation_sum"].sum()

    hottest = city_temp.idxmax()
    coldest = city_temp.idxmin()
    rainiest = city_rain.idxmax()
    driest = city_rain.idxmin()

    sj_data = df[df["city"] == "San José"]
    sj_mean_temp = sj_data["temperature_2m_mean"].mean()
    sj_total_rain = sj_data["precipitation_sum"].sum()

    insights = [
        f"🔥 Ciudad más cálida: {hottest} ({city_temp.max():.1f}°C)",
        f"❄️ Ciudad más fría: {coldest} ({city_temp.min():.1f}°C)",
        f"🌧️ Ciudad más lluviosa: {rainiest} ({city_rain.max():,.0f} mm)",
        f"☀️ Ciudad más seca: {driest} ({city_rain.min():,.0f} mm)",
        f"",
        f"🇨🇷 San José, Costa Rica:",
        f"   • Temp media: {sj_mean_temp:.1f}°C",
        f"   • Precipitación total: {sj_total_rain:,.0f} mm",
        f"   • Días de lluvia: {sj_data['is_rainy'].mean()*100:.0f}% del año",
        f"   • Días calurosos (>30°C): {sj_data['is_hot'].sum()} días",
    ]

    for insight in insights:
        print(insight)

    # Guardar insights como texto
    insights_path = os.path.join(OUTPUT_DIR, "insights.txt")
    with open(insights_path, "w") as f:
        f.write("WEATHER DATA PIPELINE — INSIGHTS\n")
        f.write("="*40 + "\n\n")
        for line in insights:
            f.write(line + "\n")
    print(f"\n✅ Insights guardados: {insights_path}")

    return insights


def main():
    print(f"\n{'='*60}")
    print("🔬 WEATHER DATA PIPELINE — Análisis Exploratorio")
    print(f"{'='*60}\n")

    # Cargar
    df = load_data()

    # Estadísticas
    summary_stats(df)
    by_city_summary(df)

    # Visualizaciones
    print("\n🎨 Generando visualizaciones...")
    plot_temperature_comparison(df)
    plot_precipitation_heatmap(df)
    plot_seasonal_patterns(df)
    plot_wind_storm_chart(df)
    plot_rain_vs_temp(df)

    # Insights
    generate_insights(df)

    print(f"\n{'='*60}")
    print("✅ ANÁLISIS COMPLETADO")
    print(f"📁 Outputs en: {OUTPUT_DIR}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
