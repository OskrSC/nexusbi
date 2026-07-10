from dash import html, dcc
import dash_bootstrap_components as dbc

def layout():
    """
    Layout del Módulo 1: Customer Intelligence & Marketing.
    """
    return dbc.Container([
        html.H2("Módulo 1: Customer Intelligence & Marketing", className="mt-4 mb-4"),
        
        dbc.Row([
            # Panel de Control Izquierdo (Subida de datos y configuración)
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Configuración del Modelo"),
                    dbc.CardBody([
                        html.P("Sube tu archivo CSV de clientes (conteniendo Edad, Ingresos, Puntuación de Gasto, etc.):"),
                        dcc.Upload(
                            id='m1-upload-data',
                            children=html.Div(['Arrastra y suelta o ', html.A('Selecciona Archivo')]),
                            style={
                                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                                'borderWidth': '1px', 'borderStyle': 'dashed',
                                'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px 0'
                            },
                            multiple=False
                        ),
                        html.Hr(),
                        html.Label("Número de Clusters (K-Means):"),
                        dcc.Slider(id='m1-k-clusters', min=2, max=8, step=1, value=3),
                        html.Div(id='m1-data-status', className="text-muted small mt-2")
                    ])
                ], color="light")
            ], width=4),
            
            # Panel de Visualización Derecho (Resultados)
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Segmentación de Clientes (K-Means)"),
                    dbc.CardBody([
                        # Este dcc.Graph será poblado por el callback del módulo
                        dcc.Graph(id='m1-clustering-graph', config={'displayModeBar': False})
                    ])
                ]),
                
                dbc.Card([
                    dbc.CardHeader("Métricas de Cliente (CLV & Churn)"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([html.H5("CLV Promedio"), html.P("Cargando...", id='m1-clv-value')], width=6),
                            dbc.Col([html.H5("Riesgo Churn"), html.P("Cargando...", id='m1-churn-value')], width=6)
                        ])
                    ])
                ], className="mt-3")
            ], width=8)
        ])
    ], fluid=True)