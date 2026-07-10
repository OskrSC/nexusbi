from dash import html, dcc
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container([
        html.H2("Módulo 7: Process & Quality", className="mt-4 mb-4 text-light"),
        
        dcc.Tabs(id='m7-tabs', value='tab-mining', className="mb-4 text-light", style={"fontWeight": "bold"}, children=[
            dcc.Tab(label='🗺️ Process Mining (PM4Py)', value='tab-mining', className="text-light"),
            dcc.Tab(label="🎫 Clasificador de Tickets NLP", value='tab-nlp', className="text-light")
        ]),
        
        # Carga el layout por defecto
        html.Div(id='m7-tab-content', children=layout_mining())
    ], fluid=True)

def layout_mining():
    return dbc.Card([
        dbc.CardHeader("Descubrimiento de Procesos ocultos (Project 823)", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P("Sube un CSV con 'CaseID' y 'Activity'. La app descubrirá cómo fluye el proceso REAL (no el teórico).", className="text-light mb-3"),
                    dcc.Upload(id='m7-log-upload', children=html.Div(['Arrastra o ', html.A('Selecciona CSV', className="text-info")]),
                        style={'width': '100%', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderColor': '#555', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px 0', 'backgroundColor': '#333', 'color': 'white'}),
                    html.Div(id='m7-mining-status', className="text-muted mt-2")
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='m7-process-graph', config={'displayModeBar': False}, style={'height': '60vh'})
                ], width=8)
            ])
        ], className="bg-dark")
    ], color="dark")

def layout_nlp():
    return dbc.Card([
        dbc.CardHeader("Análisis Inteligente de Soporte (Project 826)", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P("Pega el texto de un correo de soporte o queja. La IA extraerá la intención y el sentimiento.", className="text-light mb-3"),
                    dcc.Textarea(id='m7-ticket-text', placeholder="Ej: 'El producto llegó roto y quiero mi dinero de vuelta, esto es inaceptable.'", 
                                  style={'width': '100%', 'height': '200px', 'backgroundColor': '#333', 'color': 'white', 'border': '1px solid #555', 'borderRadius': '5px'}),
                    html.Hr(className="border-secondary mt-4"),
                    html.H5("Resultado del Análisis:", className="text-light"),
                    html.Div(id='m7-nlp-result')
                ], width=5),
                dbc.Col([
                    # Un panel visual de retroalimentación para el usuario
                    html.Div([
                        html.H2("🎯", className="text-center"),
                        html.H4(id='m7-intent-display', className="text-center text-light mt-2"),
                        html.Hr(className="border-secondary"),
                        html.H2("❤️", className="text-center"),
                        html.H4(id='m7-sentiment-display', className="text-center mt-2"),
                        html.Hr(className="border-secondary"),
                        html.P("Puntuación de Polaridad:", className="text-muted text-center"),
                        html.H3(id='m7-polarity-display', className="text-center text-info")
                    ], className="p-4 border border-secondary rounded bg-dark", style={'marginTop': '50px'})
                ], width=5, className="offset-2")
            ])
        ], className="bg-dark")
    ], color="dark")