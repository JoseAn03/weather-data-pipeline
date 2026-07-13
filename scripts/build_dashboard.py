#!/usr/bin/env python3
"""
Weather Data Pipeline — Dashboard interactivo con Plotly
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "weather_data.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "dashboard")
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH, parse_dates=["date"])

# Features derivadas
df["is_rainy"] = df["precipitation_sum"] > 0
df["month_name"] = df["date"].dt.strftime("%B")

# ─── 1. Mapa de calor: Temperatura media global ───────────────────────
city_avg = df.groupby(["city", "latitude", "longitude"]).agg(
    temp_mean=("temperature_2m_mean", "mean"),
    precip_total=("precipitation_sum", "sum"),
    rainy_days=("is_rainy", "mean"),
).reset_index()

fig1 = px.scatter_geo(
    city_avg,
    lat="latitude",
    lon="longitude",
    size="temp_mean",
    color="temp_mean",
    hover_name="city",
    hover_data={
        "temp_mean": ":.1f",
        "precip_total": ":.0f",
        "rainy_days": ":.0%",
        "latitude": False,
        "longitude": False,
    },
    color_continuous_scale="RdYlBu_r",
    size_max=30,
    projection="natural earth",
    title="🌍 Temperatura Media por Ciudad"
)
fig1.update_layout(
    geo=dict(showframe=True, showcoastlines=True, coastlinecolor="gray"),
    height=500
)
fig1.write_html(os.path.join(OUTPUT_DIR, "01_geo_map.html"))
print("✅ Mapa guardado")

# ─── 2. Timeline: Temperatura a lo largo del año ───────────────────────
key_cities = ["San José", "New York", "London", "Tokyo", "Sydney"]
plot_df = df[df["city"].isin(key_cities)]

fig2 = px.line(
    plot_df,
    x="date",
    y="temperature_2m_mean",
    color="city",
    title="📈 Evolución de Temperatura Media por Ciudad (12 meses)",
    labels={"temperature_2m_mean": "Temperatura Media (°C)", "date": "Fecha"},
    line_shape="spline",
)
fig2.update_layout(height=500, hovermode="x unified")
fig2.write_html(os.path.join(OUTPUT_DIR, "02_timeline.html"))
print("✅ Timeline guardado")

# ─── 3. Boxplot: Distribución de temperatura por ciudad ───────────────
fig3 = px.box(
    df,
    x="city",
    y="temperature_2m_mean",
    color="city",
    title="📊 Distribución de Temperatura por Ciudad",
    labels={"temperature_2m_mean": "Temperatura Media (°C)", "city": ""},
    notched=True,
)
fig3.update_layout(height=500, showlegend=False, xaxis_tickangle=-45)
fig3.write_html(os.path.join(OUTPUT_DIR, "03_boxplot.html"))
print("✅ Boxplot guardado")

# ─── 4. Dashboard combinado ───────────────────────────────────────────
dashboard = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Data Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f1923;
            color: #e0e0e0;
        }}
        .header {{
            background: linear-gradient(135deg, #1a2a3a, #0f1923);
            padding: 3rem 2rem;
            text-align: center;
            border-bottom: 2px solid #2a3a4a;
        }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .header h1 span {{ color: #4fc3f7; }}
        .header p {{ color: #8899aa; font-size: 1.1rem; }}
        .stats-row {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            padding: 2rem;
            flex-wrap: wrap;
        }}
        .stat-card {{
            background: #1a2a3a;
            border: 1px solid #2a3a4a;
            border-radius: 12px;
            padding: 1.5rem 2rem;
            text-align: center;
            min-width: 150px;
        }}
        .stat-card .number {{ font-size: 2rem; font-weight: bold; color: #4fc3f7; }}
        .stat-card .label {{ font-size: 0.9rem; color: #8899aa; margin-top: 0.3rem; }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 1.5rem;
            padding: 1.5rem;
        }}
        .card {{
            background: #1a2a3a;
            border: 1px solid #2a3a4a;
            border-radius: 12px;
            overflow: hidden;
        }}
        .card iframe {{ width: 100%; height: 520px; border: none; }}
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #556677;
            font-size: 0.9rem;
            border-top: 1px solid #2a3a4a;
        }}
        .footer a {{ color: #4fc3f7; text-decoration: none; }}
        .btn {{
            display: inline-block;
            padding: 0.8rem 1.5rem;
            background: #4fc3f7;
            color: #0f1923;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            margin-top: 1rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌤️ Weather <span>Data Dashboard</span></h1>
        <p>Análisis climático global con datos de Open-Meteo API</p>
        <p style="margin-top:0.5rem;color:#4fc3f7;">
            📊 {len(df):,} registros · 🏙️ {df['city'].nunique()} ciudades · 📅 {df['date'].nunique()} días
        </p>
        <a href="https://github.com/JoseAn03/weather-data-pipeline" class="btn">
            📂 Ver en GitHub
        </a>
    </div>

    <div class="stats-row">
        <div class="stat-card">
            <div class="number">{df['city'].nunique()}</div>
            <div class="label">Ciudades Analizadas</div>
        </div>
        <div class="stat-card">
            <div class="number">{len(df):,}</div>
            <div class="label">Registros Diarios</div>
        </div>
        <div class="stat-card">
            <div class="number">{df['temperature_2m_mean'].mean():.1f}°C</div>
            <div class="label">Temp. Promedio Global</div>
        </div>
        <div class="stat-card">
            <div class="number">{df['precipitation_sum'].sum():,.0f}</div>
            <div class="label">mm de Precipitación Total</div>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <iframe srcdoc='{open(os.path.join(OUTPUT_DIR, "01_geo_map.html")).read().replace(chr(39), "&#39;").replace("'", "&#39;")}'></iframe>
        </div>
        <div class="card">
            <iframe srcdoc='{open(os.path.join(OUTPUT_DIR, "02_timeline.html")).read().replace(chr(39), "&#39;").replace("'", "&#39;")}'></iframe>
        </div>
        <div class="card">
            <iframe srcdoc='{open(os.path.join(OUTPUT_DIR, "03_boxplot.html")).read().replace(chr(39), "&#39;").replace("'", "&#39;")}'></iframe>
        </div>
    </div>

    <div class="footer">
        <p>🔗 <a href="https://open-meteo.com/">Open-Meteo API</a> · Datos climatológicos históricos</p>
        <p>Proyecto de portafolio — José Andrés Sequeira · Data Analyst</p>
    </div>
</body>
</html>
"""

dashboard_path = os.path.join(OUTPUT_DIR, "index.html")
with open(dashboard_path, "w") as f:
    f.write(dashboard)
print(f"✅ Dashboard guardado: {dashboard_path}")
