from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table

def layout():
    return dbc.Container([
        html.H2("Módulo 2: Retail Engine", className="mt-4 mb-4 text-light"),
        
        # AQUÍ ESTABA EL ERROR: Faltaban los dcc.Tab dentro de dcc.Tabs
        dcc.Tabs(id='m2-tabs', value='tab-basket', className="mb-4 text-light", style={"fontWeight": "bold"}, children=[
            dcc.Tab(label='Análisis de Canasta (Apriori)', value='tab-basket', className="text-light"),
            dcc.Tab(label='Sistema de Recomendación', value='tab-rec', className="text-light")
        ]),
        
        html.Div(id='m2-tab-content'),
        
        # MEMORIAS OCULTAS PARA GUARDAR LOS ARCHIVOS CSV
        dcc.Store(id='m2-basket-store'),
        dcc.Store(id='m2-rec-store')
    ], fluid=True)

def layout_basket():
    return dbc.Card([
        dbc.CardHeader("Análisis de Canasta (Apriori) - Proyecto 802", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    # Se añadió 'text-light' a los textos
                    html.P("Sube un CSV con transacciones. Puede ser una sola columna con productos separados por comas (ej: 'leche,pan,huevos').", className="text-light"),
                    dcc.Upload(
                        id='m2-basket-upload', 
                        children=html.Div(['Arrastra o ', html.A('Selecciona CSV', className="text-info")]),
                        # Estilo mejorado para cuadrar con el tema oscuro
                        style={
                            'width': '100%', 'height': '60px', 'lineHeight': '60px', 
                            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderColor': '#555',
                            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px 0',
                            'backgroundColor': '#333', 'color': 'white'
                        }
                    ),
                    html.Hr(className="border-secondary"),
                    html.Label("Soporte Mínimo:", className="text-light"),
                    dcc.Slider(id='m2-support', min=0.1, max=0.9, step=0.05, value=0.3, marks={i: str(i) for i in [0.1, 0.3, 0.5, 0.7, 0.9]}),
                    html.Label("Confianza Mínima:", className="mt-2 text-light"),
                    dcc.Slider(id='m2-confidence', min=0.1, max=1.0, step=0.05, value=0.6)
                ], width=4),
                dbc.Col([
                    dash_table.DataTable(
                        id='m2-rules-table', 
                        page_size=8, 
                        style_table={'overflowX': 'auto', 'backgroundColor': '#2b2b2b'}, 
                        style_header={'backgroundColor': '#444', 'color': 'white', 'border': '1px solid #555', 'fontWeight': 'bold'}, 
                        style_cell={'backgroundColor': '#2b2b2b', 'color': 'white', 'border': '1px solid #444', 'textAlign': 'left'}
                    )
                ], width=8)
            ])
        ], className="bg-dark") # Fondo oscuro explícito para la tarjeta
    ], color="dark")

def layout_recommender():
    return dbc.Card([
        dbc.CardHeader("Sistema de Recomendación (Filtro Colaborativo) - Proyecto 825", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P("Sube un CSV con tres columnas exactas: 'User_ID', 'Item_ID', 'Rating' (1-5).", className="text-light"),
                    dcc.Upload(
                        id='m2-rec-upload', 
                        children=html.Div(['Arrastra o ', html.A('Selecciona CSV', className="text-info")]),
                        style={
                            'width': '100%', 'height': '60px', 'lineHeight': '60px', 
                            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderColor': '#555',
                            'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px 0',
                            'backgroundColor': '#333', 'color': 'white'
                        }
                    ),
                    html.Hr(className="border-secondary"),
                    html.Div([
                        html.Label("Selecciona un Usuario:", className="text-light"),
                        dcc.Dropdown(id='m2-user-dropdown', clearable=False, className="bg-dark text-light")
                    ], id='m2-dropdown-container', style={'display': 'none'})
                ], width=4),
                dbc.Col([
                    html.H5("Productos Recomendados:", className="text-light mt-3"),
                    html.Ul(id='m2-rec-list', className="list-group")
                ], width=8)
            ])
        ], className="bg-dark")
    ], color="dark")