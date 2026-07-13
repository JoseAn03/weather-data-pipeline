# 🌤️ Weather Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://python.org)
[![Open-Meteo API](https://img.shields.io/badge/API-OpenMeteo-green)](https://open-meteo.com)
[![Pandas](https://img.shields.io/badge/Pandas-EDA-orange?logo=pandas)](https://pandas.pydata.org)
[![Plotly](https://img.shields.io/badge/Plotly-Dashboard-blueviolet?logo=plotly)](https://plotly.com)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-lightgrey)](LICENSE)

Pipeline completo de extracción, análisis y visualización de datos climáticos globales usando la API pública de **Open-Meteo** (sin API key requerida).

```
📊 10 ciudades · 📅 365 días · 🌡️ 8 variables climáticas
```

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Dashboard](#-dashboard-interactivo)
- [Resultados Clave](#-resultados-clave)
- [Tecnologías](#-tecnologías)
- [Próximos Pasos](#-próximos-pasos)

---

## 📖 Descripción

Este proyecto demuestra un **pipeline completo de datos**:

1. **Extraer** → Consulta la API de Open-Meteo para datos climáticos históricos de 10 ciudades globales
2. **Transformar** → Limpieza, estructuración, feature engineering (estaciones, rangos térmicos, etc.)
3. **Analizar** → Estadísticas descriptivas, comparaciones, correlaciones, insights
4. **Visualizar** → 5 gráficos estáticos + dashboard interactivo con Plotly
5. **Publicar** → Dashboard HTML interactivo listo para GitHub Pages

Las ciudades analizadas incluyen: **San José (CR)** 🇨🇷, New York, London, Tokyo, Sydney, Paris, Madrid, Miami, São Paulo y Mumbai.

---

## 📁 Estructura del Proyecto

```
weather-data-pipeline/
├── run_all.py                 # 🚀 Pipeline completo (un solo comando)
├── requirements.txt           # Dependencias
├── README.md                  # 🏠 Este archivo
│
├── scripts/
│   ├── fetch_weather.py       # 🌐 Extracción de datos desde API
│   ├── analysis.py            # 📊 EDA + visualizaciones estáticas
│   └── build_dashboard.py     # 📈 Dashboard interactivo Plotly
│
├── data/
│   └── weather_data.csv       # 💾 Datos crudos extraídos
│
├── outputs/
│   ├── 01_temp_comparison.png      # Temperatura media por ciudad
│   ├── 02_precip_heatmap.png       # Precipitación por ciudad/mes
│   ├── 03_seasonal_patterns.png    # Patrones estacionales
│   ├── 04_wind_max.png             # Vientos máximos
│   ├── 05_rain_vs_temp.png         # Relación lluvia vs temperatura
│   └── insights.txt                # Conclusiones clave
│
├── dashboard/
│   ├── index.html              # 🖥️ Dashboard completo (GitHub Pages)
│   ├── 01_geo_map.html         # Mapa global interactivo
│   ├── 02_timeline.html        # Timeline de temperaturas
│   └── 03_boxplot.html         # Distribuciones por ciudad
│
└── notebooks/                  # 🧪 (futuro) Jupyter Notebooks
```

---

## ⚙️ Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/JoseAn03/weather-data-pipeline.git
cd weather-data-pipeline

# 2. Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt
```

---

## 🚀 Uso

### ▶️ Pipeline completo

```bash
python run_all.py
```

Esto ejecuta los 3 pasos:

| Paso | Script | Descripción | Tiempo |
|------|--------|-------------|--------|
| 1️⃣ | `fetch_weather.py` | Extrae datos climáticos de la API | ~10-15s |
| 2️⃣ | `analysis.py` | EDA + 5 gráficos + insights | ~10s |
| 3️⃣ | `build_dashboard.py` | Dashboard interactivo HTML | ~5s |

### ▶️ Pasos individuales

```bash
# Solo extraer datos
python scripts/fetch_weather.py

# Solo analizar (requiere data/weather_data.csv)
python scripts/analysis.py

# Solo construir dashboard (requiere data/weather_data.csv)
python scripts/build_dashboard.py
```

---

## 🖥️ Dashboard Interactivo

El dashboard incluye:

- 🌍 **Mapa global** con temperaturas medias por ciudad
- 📈 **Timeline** de evolución de temperatura (12 meses)
- 📊 **Boxplots** de distribución por ciudad
- 🎯 **KPIs** en tiempo real (ciudades, registros, promedios)
- 🎨 Diseño oscuro profesional
- 📱 Responsivo

Para verlo, abrí `dashboard/index.html` en tu navegador, o visitá:
**[🔗 Ver Dashboard](https://JoseAn03.github.io/weather-data-pipeline/dashboard/)**

---

## 📊 Resultados Clave

| Ciudad | Temp Media | Precip. Anual | Días Lluvia |
|--------|:----------:|:-------------:|:-----------:|
| **San José** 🇨🇷 | ~21°C | ~1,900 mm | ~60% |
| **Miami** 🇺🇸 | ~25°C | ~1,500 mm | ~55% |
| **London** 🇬🇧 | ~11°C | ~600 mm | ~45% |
| **Tokyo** 🇯🇵 | ~16°C | ~1,500 mm | ~50% |
| **Sydney** 🇦🇺 | ~18°C | ~1,200 mm | ~40% |

> 💡 **Insight destacado:** San José mantiene una temperatura notablemente estable todo el año (variación < 5°C), mientras que Nueva York experimenta un rango estacional de más de 25°C entre invierno y verano.

---

## 🛠️ Tecnologías

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python 3.8+ |
| **API** | [Open-Meteo](https://open-meteo.com/) (gratis, sin key) |
| **Procesamiento** | Pandas, NumPy |
| **Visualización** | Matplotlib, Seaborn, Plotly |
| **Dashboard** | HTML + Plotly.js |

---

## 🔮 Próximos Pasos

- [ ] Añadir más ciudades (Latinoamérica, África, Medio Oriente)
- [ ] Feature engineering: heat index, humedad, UV index
- [ ] Notebook Jupyter con storytelling
- [ ] Conexión con SQL (DuckDB) para queries analíticas
- [ ] Correlación clima ↔ demanda turística / alquiler de autos
- [ ] Deployment: GitHub Actions para actualización automática semanal

---

## 📬 Contacto

**José Andrés Sequeira**  
📧 chomita0317@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/jose-andres-sequeira-hernandez-3aaa03285)  
💻 [GitHub](https://github.com/JoseAn03)

---

<p align="center">
  ⭐ Si te sirve este proyecto, ¡dale una estrella!
</p>
