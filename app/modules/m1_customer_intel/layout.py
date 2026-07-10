from dash import html, dcc
import dash_bootstrap_components as dbc

def layout():
    """
    Layout del Módulo 1: Customer Intelligence & Marketing.
    """
    return dbc.Container([
        html.H2("Módulo 1: Customer Intelligence & Marketing", className="mt-4 mb-4 text-light"),
        
        dbc.Row([
            # Panel de Control Izquierdo
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Configuración del Modelo", className="bg-secondary text-light"),
                    dbc.CardBody([
                        html.P([
                            "Sube un archivo CSV de clientes (conteniendo Edad, Ingresos, Puntuación de Gasto, etc.) o ",
                            html.A("descarga el archivo de prueba aquí", 
                                   href="https://raw.githubusercontent.com/OskrSC/nexusbi/main/data/clientes_test.csv", 
                                   target="_blank", 
                                   className="text-info font-weight-bold"),
                            "."
                        ], className="text-light"),
                        
                        # <-- EL COMPONENTE DE SUBIDA QUE FALTABA -->
                        dcc.Upload(
                            id='m1-upload-data',
                            children=html.Div(['Arrastra y suelta o ', html.A('Selecciona Archivo', className="text-info")]),
                            style={
                                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                                'borderWidth': '1px', 'borderStyle': 'dashed',
                                'borderRadius': '5px', 'textAlign': 'center', 
                                'margin': '10px 0',
                                'backgroundColor': '#333', 'color': 'white',
                                'borderColor': '#555'
                            }
                        ),
                        # ---------------------------------------- -->

                        html.Hr(className="border-secondary"),
                        html.Label("Número de Clusters (K-Means):", className="text-light"),
                        dcc.Slider(id='m1-k-clusters', min=2, max=8, step=1, value=3),
                        html.Div(id='m1-data-status', className="text-muted small mt-2")
                    ], className="bg-dark")
                ], color="dark")
            ], width=4),
            
            # Panel de Visualización Derecho
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Segmentación de Clientes (K-Means)", className="bg-secondary text-light"),
                    dbc.CardBody([
                        dcc.Graph(id='m1-clustering-graph', config={'displayModeBar': False})
                    ], className="bg-dark")
                ], color="dark", className="mb-3"),
                
                dbc.Card([
                    dbc.CardHeader("Métricas de Cliente (CLV & Churn)", className="bg-secondary text-light"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([html.H5("CLV Promedio", className="text-light"), html.P("Cargando...", id='m1-clv-value', className="text-info")], width=6),
                            dbc.Col([html.H5("Riesgo Churn", className="text-light"), html.P("Cargando...", id='m1-churn-value', className="text-warning")], width=6)
                        ])
                    ], className="bg-dark")
                ], color="dark")
            ], width=8)
        ])
    ], fluid=True)