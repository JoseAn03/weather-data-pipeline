#!/usr/bin/env python3
"""
Weather Data Pipeline — Dashboard interactivo con Plotly
"""

import pandas as pd
import plotly.express as px
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
    },
    color_continuous_scale="RdYlBu_r",
    size_max=30,
    projection="natural earth",
    title="Temperatura Media por Ciudad"
)
fig1.update_layout(
    geo=dict(showframe=True, showcoastlines=True, coastlinecolor="gray"),
    height=550,
    paper_bgcolor="#1a2a3a",
    font=dict(color="#e0e0e0"),
    title=dict(font=dict(size=18, color="#e0e0e0"))
)
fig1.write_html(os.path.join(OUTPUT_DIR, "01_geo_map.html"), include_plotlyjs="cdn")
print("✅ Mapa guardado")

# ─── 2. Timeline: Temperatura a lo largo del año ───────────────────────
key_cities = ["San Jose", "New York", "London", "Tokyo", "Sydney"]
# Normalizar nombre de San José para el filtro
df["city_key"] = df["city"].str.replace("ó", "o").str.replace("í", "i")
plot_df = df[df["city_key"].isin([c.lower() for c in key_cities])]

fig2 = px.line(
    plot_df,
    x="date",
    y="temperature_2m_mean",
    color="city",
    title="Evolucion de Temperatura por Ciudad (12 meses)",
    labels={"temperature_2m_mean": "Temperatura Media (C)", "date": "Fecha"},
    line_shape="spline",
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig2.update_layout(
    height=550,
    hovermode="x unified",
    paper_bgcolor="#1a2a3a",
    plot_bgcolor="#0f1923",
    font=dict(color="#e0e0e0"),
    title=dict(font=dict(size=18, color="#e0e0e0")),
    legend=dict(font=dict(color="#e0e0e0")),
    xaxis=dict(gridcolor="#2a3a4a"),
    yaxis=dict(gridcolor="#2a3a4a"),
)
fig2.write_html(os.path.join(OUTPUT_DIR, "02_timeline.html"), include_plotlyjs="cdn")
print("✅ Timeline guardado")

# ─── 3. Boxplot: Distribucion de temperatura por ciudad ───────────────
fig3 = px.box(
    df,
    x="city",
    y="temperature_2m_mean",
    color="city",
    title="Distribucion de Temperatura por Ciudad",
    labels={"temperature_2m_mean": "Temperatura Media (C)", "city": ""},
    notched=True,
    color_discrete_sequence=px.colors.qualitative.Set2,
)
fig3.update_layout(
    height=550,
    showlegend=False,
    xaxis_tickangle=-45,
    paper_bgcolor="#1a2a3a",
    plot_bgcolor="#0f1923",
    font=dict(color="#e0e0e0"),
    title=dict(font=dict(size=18, color="#e0e0e0")),
    xaxis=dict(gridcolor="#2a3a4a"),
    yaxis=dict(gridcolor="#2a3a4a"),
)
fig3.write_html(os.path.join(OUTPUT_DIR, "03_boxplot.html"), include_plotlyjs="cdn")
print("✅ Boxplot guardado")

# ─── 4. Dashboard combinado (lightweight) ──────────────────────────────
dashboard = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Data Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f1923;
            color: #e0e0e0;
        }
        .header {
            background: linear-gradient(135deg, #1a2a3a, #0f1923);
            padding: 3rem 2rem;
            text-align: center;
            border-bottom: 2px solid #2a3a4a;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .header h1 span { color: #4fc3f7; }
        .header p { color: #8899aa; font-size: 1.1rem; }
        .stats-row {
            display: flex;
            justify-content: center;
            gap: 2rem;
            padding: 2rem;
            flex-wrap: wrap;
        }
        .stat-card {
            background: #1a2a3a;
            border: 1px solid #2a3a4a;
            border-radius: 12px;
            padding: 1.5rem 2rem;
            text-align: center;
            min-width: 150px;
            transition: transform 0.2s;
        }
        .stat-card:hover { transform: translateY(-3px); border-color: #4fc3f7; }
        .stat-card .number { font-size: 2rem; font-weight: bold; color: #4fc3f7; }
        .stat-card .label { font-size: 0.9rem; color: #8899aa; margin-top: 0.3rem; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 1.5rem;
            padding: 1.5rem;
        }
        .card {
            background: #1a2a3a;
            border: 1px solid #2a3a4a;
            border-radius: 12px;
            overflow: hidden;
            transition: border-color 0.2s;
        }
        .card:hover { border-color: #4fc3f7; }
        .card iframe { width: 100%; height: 560px; border: none; }
        .footer {
            text-align: center;
            padding: 2rem;
            color: #556677;
            font-size: 0.9rem;
            border-top: 1px solid #2a3a4a;
        }
        .footer a { color: #4fc3f7; text-decoration: none; }
        .footer a:hover { text-decoration: underline; }
        .btn {
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
            transition: background 0.2s;
        }
        .btn:hover { background: #81d4fa; }
        @media (max-width: 550px) {
            .grid { grid-template-columns: 1fr; }
            .header h1 { font-size: 1.8rem; }
            .stat-card { min-width: 100px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Weather <span>Data Dashboard</span></h1>
        <p>Analisis climatico global con datos de Open-Meteo API</p>
        <p style="margin-top:0.5rem;color:#4fc3f7;">
            """ + str(len(df)) + """ registros · """ + str(df['city'].nunique()) + """ ciudades · """ + str(df['date'].nunique()) + """ dias
        </p>
        <a href="https://github.com/JoseAn03/weather-data-pipeline" class="btn" target="_blank">
            Ver en GitHub
        </a>
    </div>

    <div class="stats-row">
        <div class="stat-card">
            <div class="number">""" + str(df['city'].nunique()) + """</div>
            <div class="label">Ciudades Analizadas</div>
        </div>
        <div class="stat-card">
            <div class="number">""" + f"{len(df):,}" + """</div>
            <div class="label">Registros Diarios</div>
        </div>
        <div class="stat-card">
            <div class="number">""" + f"{df['temperature_2m_mean'].mean():.1f}" + """C</div>
            <div class="label">Temp. Promedio Global</div>
        </div>
        <div class="stat-card">
            <div class="number">""" + f"{df['precipitation_sum'].sum():,.0f}" + """</div>
            <div class="label">mm de Precipitacion Total</div>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <div style="padding:1rem 1rem 0;color:#8899aa;font-size:0.85rem;">Mapa Global - Temperatura Media</div>
            <iframe src="01_geo_map.html" loading="lazy"></iframe>
        </div>
        <div class="card">
            <div style="padding:1rem 1rem 0;color:#8899aa;font-size:0.85rem;">Timeline - Evolucion de Temperatura</div>
            <iframe src="02_timeline.html" loading="lazy"></iframe>
        </div>
        <div class="card">
            <div style="padding:1rem 1rem 0;color:#8899aa;font-size:0.85rem;">Boxplot - Distribucion por Ciudad</div>
            <iframe src="03_boxplot.html" loading="lazy"></iframe>
        </div>
    </div>

    <div class="footer">
        <p>Datos via <a href="https://open-meteo.com/" target="_blank">Open-Meteo API</a> (gratis, sin API key)</p>
        <p>Proyecto de portafolio - <a href="https://github.com/JoseAn03">Jose Andres Sequeira</a> · Data Analyst</p>
    </div>
</body>
</html>"""

# Recalcular KPIs
n_cities = df['city'].nunique()
n_records = len(df)
n_days = df['date'].nunique()
avg_temp = df['temperature_2m_mean'].mean()
total_precip = df['precipitation_sum'].sum()

dashboard = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather Data Dashboard</title>
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
            transition: transform 0.2s;
        }}
        .stat-card:hover {{ transform: translateY(-3px); border-color: #4fc3f7; }}
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
            transition: border-color 0.2s;
        }}
        .card:hover {{ border-color: #4fc3f7; }}
        .card iframe {{ width: 100%; height: 560px; border: none; }}
        .card-label {{
            padding: 0.8rem 1.2rem 0;
            color: #8899aa;
            font-size: 0.85rem;
        }}
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #556677;
            font-size: 0.9rem;
            border-top: 1px solid #2a3a4a;
        }}
        .footer a {{ color: #4fc3f7; text-decoration: none; }}
        .footer a:hover {{ text-decoration: underline; }}
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
            transition: background 0.2s;
        }}
        .btn:hover {{ background: #81d4fa; }}
        @media (max-width: 550px) {{
            .grid {{ grid-template-columns: 1fr; }}
            .header h1 {{ font-size: 1.8rem; }}
            .stat-card {{ min-width: 100px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Weather <span>Data Dashboard</span></h1>
        <p>Analisis climatico global con datos de Open-Meteo API</p>
        <p style="margin-top:0.5rem;color:#4fc3f7;">
            {n_records:,} registros &middot; {n_cities} ciudades &middot; {n_days} dias
        </p>
        <a href="https://github.com/JoseAn03/weather-data-pipeline" class="btn" target="_blank">
            Ver en GitHub
        </a>
    </div>

    <div class="stats-row">
        <div class="stat-card">
            <div class="number">{n_cities}</div>
            <div class="label">Ciudades Analizadas</div>
        </div>
        <div class="stat-card">
            <div class="number">{n_records:,}</div>
            <div class="label">Registros Diarios</div>
        </div>
        <div class="stat-card">
            <div class="number">{avg_temp:.1f} C</div>
            <div class="label">Temp. Promedio Global</div>
        </div>
        <div class="stat-card">
            <div class="number">{total_precip:,.0f}</div>
            <div class="label">mm de Precipitacion Total</div>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-label">Mapa Global &mdash; Temperatura Media</div>
            <iframe src="01_geo_map.html" loading="lazy"></iframe>
        </div>
        <div class="card">
            <div class="card-label">Timeline &mdash; Evolucion de Temperatura</div>
            <iframe src="02_timeline.html" loading="lazy"></iframe>
        </div>
        <div class="card">
            <div class="card-label">Boxplot &mdash; Distribucion por Ciudad</div>
            <iframe src="03_boxplot.html" loading="lazy"></iframe>
        </div>
    </div>

    <div class="footer">
        <p>Datos via <a href="https://open-meteo.com/" target="_blank">Open-Meteo API</a> (gratis, sin API key)</p>
        <p>Proyecto de portafolio &mdash; <a href="https://github.com/JoseAn03">Jose Andres Sequeira</a> &middot; Data Analyst</p>
    </div>
</body>
</html>"""

dashboard_path = os.path.join(OUTPUT_DIR, "index.html")
with open(dashboard_path, "w") as f:
    f.write(dashboard)
print(f"Dashboard guardado: {dashboard_path}")
print(f"Tamano: {os.path.getsize(dashboard_path) / 1024:.1f} KB")
