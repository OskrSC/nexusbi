# 🧠 NexusBI: Enterprise Analytics & AI Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Dash-2.14-orange?logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-5.18-636EFA?logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

**NexusBI** es un sistema ERP Analítico modular construido desde cero. Está basada en conceptos teóricos de Ciencia de Datos, es una aplicación web interactiva, lista para producción, utilizando arquitectura de software, ingeniería de datos y modelos predictivos.

## 🏗️ Arquitectura del Sistema

El proyecto utiliza un patrón **"Monolito Modular"** con una arquitectura estrictamente desacoplada, diseñada para ser escalable y ágil:

*   **SPA Routing (Single Page Application):** La interfaz nunca recarga. El enrutamiento dinámico inyecta módulos bajo demanda.
*   **Desacoplamiento Estricto:** Cada módulo sigue la estructura `layout.py` (UI) $\rightarrow$ `callbacks.py` (Lógica de control) $\rightarrow$ `services.py` (Matemáticas puras). Los modelos de ML no saben que existen gráficos.
*   **State Management (`dcc.Store`):** Prevención de bugs de renderizado al manejar subidas de archivos y cálculos pesados.
*   **Lazy Loading & Caché:** Los modelos pesados (ej. Prophet, PM4Py) solo se cargan en memoria cuando el usuario accede a ese módulo específico.

## 🗺️ Módulos de Inteligencia de Negocio

La aplicación contiene 7 módulos independientes que resuelven problemas de negocio reales:

### 1. Customer Intelligence & Marketing
*   **Algoritmos:** K-Means, Regresión Lineal (CLV), Random Forest (Churn).
*   **Característica:** Segmentación 3D interactiva y cálculo automatizado de métricas de retención por clúster.

### 2. Retail Engine
*   **Algoritmos:** Apriori (mlxtend), Filtro Colaborativo (Cosine Similarity).
*   **Característica:** Generación de reglas de asociación transaccional y motor de recomendaciones de productos por similitud de usuarios.

### 3. FinOps & Riesgo
*   **Algoritmos:** Prophet (Meta), Random Forest (Fraude), Ajuste Polinomial.
*   **Característica:** Pronósticos de series de tiempo con intervalos de confianza (Incertidumbre), Optimizador de Elasticidad de Precios y Simulador Transaccional de Fraude con semáforos visuales.

### 4. Supply Chain & Logística
*   **Algoritmos:** Programación Lineal (PuLP), Cálculo EOQ.
*   **Característica:** **Visualización Geo-Espacial.** Resuelve problemas de transporte y dibuja las rutas óptimas en un mapa oscuro de EE.UU. (Plotly Scattergeo).

### 5. Workforce & PMO
*   **Algoritmos:** Camino Crítico (NetworkX), Análisis de Riesgos.
*   **Característica:** Diagramas de red de proyectos donde el Camino Crítico se resalta automáticamente. Matriz de riesgos interactiva con burbujas dinámicas.

### 6. Smart Factory (IoT)
*   **Algoritmos:** Isolation Forest, Regresión Múltiple, Programación Lineal.
*   **Característica:** Detección de anomalías en líneas de producción, **Indicadores Gauges** estilo tablero industrial para mantenimiento predictivo (TTF), y minimización de energía.

### 7. Process & Quality
*   **Algoritmos:** Process Mining (PM4Py), NLP Híbrido (TextBlob + Diccionario Léxico).
*   **Característica:** Descubrimiento automático de flujos de trabajo reales a partir de Event Logs, y Clasificador de Sentimientos/Intenciones con mitigación de errores para idiomas no ingleses.

## 💡 Decisiones de Ingeniería Destacadas

1.  **Manejo de Infactibilidad en PuLP:** Si el usuario reduce la oferta en Supply Chain por debajo de la demanda, en lugar de crashear, la app captura el estado `Infeasible` y muestra una alerta roja en la UI.
2.  **Mitigación de NLP (Idioma Español):** TextBlob falla con polaridad `0.0` en español. Implementé una capa heurística que detecta el fallo del modelo y aplica un diccionario léxico local para recuperar el sentimiento real.
3.  **Truco de Rutas en Mapas:** Para dibujar múltiples líneas de vuelo/transporte no conectadas en Plotly, se inyectan valores `None` en los arrays de coordenadas para "cortar" el lápiz de forma eficiente.

## 🛠️ Tech Stack

*   **Frontend & API:** Dash, Dash Bootstrap Components (Cyborg Theme), Flask.
*   **Data Science:** Scikit-Learn, Pandas, NumPy, Prophet (Meta), TextBlob.
*   **Optimización & Grafos:** PuLP (CBC Solver), NetworkX, PM4Py.
*   **Visualización:** Plotly (Graph Objects, Gauges, Scattergeo).
*   **Despliegue:** Docker, Python dotenv.

## 🚀 Quickstart (Ejecución Local)

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/nexusbi.git
cd nexusbi

# 2. Crear y activar entorno virtual
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python -m app.main
```
Abre tu navegador en `http://localhost:8050`

## 🐳 Ejecución con Docker (Recomendado)

Para evitar problemas de dependencias locales, NexusBI está completamente containerizado.

```bash
# Construir la imagen
docker build -t nexusbi .

# Ejecutar el contenedor
docker run -p 8050:8050 nexusbi
```

## 📂 Estructura del Proyecto

```text
nexusbi/
├── app/
│   ├── main.py               # Punto de entrada, enrutador SPA
│   ├── config.py             # Gestión de rutas y variables de entorno
│   ├── core/                 # Lógica transversal (Caché, DB, ML Utils)
│   ├── components/           # Navbar, Sidebar, DataUploader reutilizables
│   └── modules/              # Los 7 módulos de negocio
│       ├── m1_customer_intel/
│       ├── m2_retail_engine/
│       └── ...               # Cada uno con layout, callbacks, services
├── data/                     # Almacenamiento en tiempo de ejecución
├── Dockerfile                # Configuración de contenedor
└── requirements.txt          # Dependencias
```
