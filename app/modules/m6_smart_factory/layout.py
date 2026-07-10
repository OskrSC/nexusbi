from dash import html, dcc
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container([
        html.H2("Módulo 6: Smart Factory (IoT)", className="mt-4 mb-4 text-light"),
        
        dcc.Tabs(id='m6-tabs', value='tab-quality', className="mb-4 text-light", style={"fontWeight": "bold"}, children=[
            dcc.Tab(label='📊 Control de Calidad', value='tab-quality', className="text-light"),
            dcc.Tab(label='⚙️ Mantenimiento Predictivo', value='tab-maint', className="text-light"),
            dcc.Tab(label='⚡ Optimizador de Energía', value='tab-energy', className="text-light")
        ]),
        
        # Carga el primer layout por defecto para evitar pantallas en blanco
        html.Div(id='m6-tab-content', children=layout_quality())
    ], fluid=True)

def layout_quality():
    return dbc.Card([
        dbc.CardHeader("Monitoreo Estadístico y Detección de Anomalías (Isolation Forest)", className="bg-secondary text-light"),
        dbc.CardBody([
            html.P("El sistema simula 50 muestras de un proceso de manufactura. Los puntos rojos fueron detectados automáticamente como anomalías fuera de control.", className="text-light mb-4"),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='m6-quality-graph', config={'displayModeBar': False})
                ], width=8),
                dbc.Col([
                    html.H5("Resumen del Lote:", className="text-light"),
                    html.Div(id='m6-quality-stats')
                ], width=4)
            ])
        ], className="bg-dark")
    ], color="dark")

def layout_maint():
    return dbc.Card([
        dbc.CardHeader("Simulador de Sensores - Tiempo de Fallo (TTF)", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P("Ingresa las lecturas actuales del equipo para calcular las horas restantes antes del fallo.", className="text-light mb-4"),
                    
                    dbc.Label("Temperatura (°C):", className="text-light"), 
                    dcc.Input(id='m6-temp', type='number', value=75, className="mb-3 form-control bg-dark text-light border-secondary"),
                    dbc.Label("Vibración (mm/s):", className="text-light"), 
                    dcc.Input(id='m6-vib', type='number', value=0.5, className="mb-3 form-control bg-dark text-light border-secondary"),
                    dbc.Label("Presión (PSI):", className="text-light"), 
                    dcc.Input(id='m6-pres', type='number', value=35, className="form-control bg-dark text-light border-secondary"),
                ], width=4),
                dbc.Col([
                    # EL GAUGE (Indicador circular)
                    dcc.Graph(id='m6-ttf-gauge', config={'displayModeBar': False}, style={'height': '50vh'}),
                    html.H3(id='m6-ttf-alert', className="text-center mt-2")
                ], width=8)
            ])
        ], className="bg-dark")
    ], color="dark")

def layout_energy():
    return dbc.Card([
        dbc.CardHeader("Distribución de Carga para Mínimo kWh", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P("Asigna la eficiencia y capacidad de 3 máquinas para completar un trabajo mínimo.", className="text-light mb-3"),
                    html.Hr(className="border-secondary"),
                    html.Label("Trabajo Total Requerido:", className="text-light"), 
                    dcc.Input(id='m6-work', type='number', value=100, className="mb-3 form-control bg-dark text-light border-secondary"),
                    
                    html.Label("Máq 1 - Capacidad / Eficiencia:", className="text-light text-sm"), 
                    dcc.Input(id='m6-m1cap', type='number', value=50, className="me-2 form-control bg-dark text-light border-secondary d-inline-block", style={'width': '45%'}),
                    dcc.Input(id='m6-m1eff', type='number', value=5, className="form-control bg-dark text-light border-secondary d-inline-block", style={'width': '45%'}),

                    html.Label("Máq 2 - Capacidad / Eficiencia:", className="text-light text-sm mt-2"), 
                    dcc.Input(id='m6-m2cap', type='number', value=60, className="me-2 form-control bg-dark text-light border-secondary d-inline-block", style={'width': '45%'}),
                    dcc.Input(id='m6-m2eff', type='number', value=4, className="form-control bg-dark text-light border-secondary d-inline-block", style={'width': '45%'}),
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='m6-energy-graph', config={'displayModeBar': False})
                ], width=8)
            ])
        ], className="bg-dark")
    ], color="dark")