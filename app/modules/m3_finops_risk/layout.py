from dash import html, dcc
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container([
        html.H2("Módulo 3: FinOps & Riesgo", className="mt-4 mb-4 text-light"),
        
        dcc.Tabs(id='m3-tabs', value='tab-forecast', className="mb-4 text-light", style={"fontWeight": "bold"}, children=[
            dcc.Tab(label='📈 Forecasting (Prophet)', value='tab-forecast', className="text-light"),
            dcc.Tab(label='💲 Price Optimizer', value='tab-price', className="text-light"),
            dcc.Tab(label='🛡️ Fraud Simulator', value='tab-fraud', className="text-light")
        ]),
        
        html.Div(id='m3-tab-content'),
        dcc.Store(id='m3-forecast-store'),
        dcc.Store(id='m3-fraud-store')
    ], fluid=True)

def layout_forecast():
    return dbc.Card([
        dbc.CardHeader("Pronóstico de Ventas con Prophet", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P([
                        "Sube un CSV con una columna de 'Date' y otra de 'Sales' o ",
                        html.A("descarga el historial de ventas de prueba aquí", 
                               href="https://raw.githubusercontent.com/OskrSC/nexusbi/main/data/ventas.csv", 
                               target="_blank", 
                               className="text-info font-weight-bold"),
                        "."
                    ], className="text-light"),
                    dcc.Upload(
                        id='m3-forecast-upload', 
                        children=html.Div(['Arrastra o ', html.A('Selecciona CSV', className="text-info")]),
                        style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderColor': '#555', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px 0', 'backgroundColor': '#333', 'color': 'white'}
                    ),
                    html.Hr(className="border-secondary"),
                    html.Label("Días a predecir:", className="text-light"),
                    dcc.Slider(id='m3-periods', min=7, max=90, step=1, value=30, marks={i: str(i) for i in [7, 30, 60, 90]})
                ], width=3),
                dbc.Col([
                    dcc.Graph(id='m3-forecast-graph', config={'displayModeBar': False})
                ], width=9)
            ])
        ], className="bg-dark")
    ], color="dark")

def layout_pricing():
    return dbc.Card([
        dbc.CardHeader("Optimización de Precios (Curva de Elasticidad)", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P("Calcula el precio exacto para maximizar ingresos. (Usa datos de ejemplo por defecto).", className="text-light"),
                    html.Hr(className="border-secondary"),
                    html.H4("Resultado Óptimo:", className="text-light mt-4"),
                    html.H2(id='m3-optimal-price', className="text-success"), 
                    html.P(id='m3-max-revenue', className="text-muted")
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='m3-price-graph', config={'displayModeBar': False})
                ], width=8)
            ])
        ], className="bg-dark")
    ], color="dark")

def layout_fraud():
    return dbc.Card([
        dbc.CardHeader("Simulador de Detección de Fraude", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P([
                        "Sube un CSV histórico con 'Amount', 'Frequency', 'IsForeignTransaction', 'IsHighRiskCountry', 'IsWeekend', 'Fraud' o ",
                        html.A("descarga el set de transacciones de prueba aquí", 
                               href="https://raw.githubusercontent.com/OskrSC/nexusbi/main/data/fraude.csv", 
                               target="_blank", 
                               className="text-info font-weight-bold"),
                        "."
                    ], className="text-light mb-3"),
                    dcc.Upload(
                        id='m3-fraud-upload', 
                        children=html.Div(['Arrastra o ', html.A('Selecciona CSV', className="text-info")]),
                        style={'width': '100%', 'height': '50px', 'lineHeight': '50px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderColor': '#555', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px 0', 'backgroundColor': '#333', 'color': 'white'}
                    ),
                    
                    html.Hr(className="border-secondary"),
                    html.H5("Simular Nueva Transacción:", className="text-light mt-3"),
                    
                    dbc.Label("Monto ($):", className="text-light"), 
                    dcc.Input(id='f-amount', type='number', value=500, min=0, step=100, className="mb-2 form-control bg-dark text-light border-secondary"),
                    
                    dbc.Label("Frecuencia (Diaria):", className="text-light"), 
                    dcc.Input(id='f-freq', type='number', value=1, min=0, step=1, className="mb-2 form-control bg-dark text-light border-secondary"),
                    
                    dbc.Label("Transacción Extranjera (1=Sí, 0=No):", className="text-light"), 
                    dcc.Input(id='f-foreign', type='number', value=0, min=0, max=1, step=1, className="mb-2 form-control bg-dark text-light border-secondary"),
                    
                    dbc.Label("País de Alto Riesgo (1=Sí, 0=No):", className="text-light"), 
                    dcc.Input(id='f-risk', type='number', value=0, min=0, max=1, step=1, className="mb-2 form-control bg-dark text-light border-secondary"),
                    
                    dbc.Label("Fin de Semana (1=Sí, 0=No):", className="text-light"), 
                    dcc.Input(id='f-weekend', type='number', value=0, min=0, max=1, step=1, className="form-control bg-dark text-light border-secondary"),
                    
                ], width=4),
                dbc.Col([
                    html.Div(id='m3-fraud-result', className="text-center mt-5")
                ], width=8)
            ])
        ], className="bg-dark")
    ], color="dark")