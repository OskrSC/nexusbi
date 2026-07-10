from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import dash_table

def layout():
    return dbc.Container([
        html.H2("Módulo 4: Supply Chain & Logística", className="mt-4 mb-4 text-light"),
        
        dcc.Tabs(id='m4-tabs', value='tab-transport', className="mb-4 text-light", style={"fontWeight": "bold"}, children=[
            dcc.Tab(label='🗺️ Optimizador de Rutas', value='tab-transport', className="text-light"),
            dcc.Tab(label='📦 Inventario (EOQ)', value='tab-eoq', className="text-light"),
            dcc.Tab(label='👷 Asignación de Recursos', value='tab-labor', className="text-light")
        ]),
        
        html.Div(id='m4-tab-content')
    ], fluid=True)

def layout_transport():
    return dbc.Card([
        dbc.CardHeader("Optimización de Red de Transporte (PuLP)", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P("Ajusta la capacidad de los almacenes. El sistema recalcula la ruta más barata y la dibuja en el mapa.", className="text-light mb-4"),
                    
                    html.Label("Capacidad Almacén A (NY):", className="text-light"), 
                    dcc.Slider(id='m4-sup-a', min=50, max=200, step=10, value=150, className="mb-4"),
                    
                    html.Label("Capacidad Almacén B (CHI):", className="text-light"), 
                    dcc.Slider(id='m4-sup-b', min=50, max=200, step=10, value=150, className="mb-4"),
                    
                    html.Hr(className="border-secondary"),
                    html.H5("Costo Total Mínimo:", className="text-light"),
                    html.H2(id='m4-total-cost', className="text-success"),
                    html.P("Tabla de Envíos:", className="text-light mt-3"),
                    dash_table.DataTable(id='m4-routes-table', page_size=5, 
                        style_table={'overflowX': 'auto', 'backgroundColor': '#2b2b2b'}, 
                        style_header={'backgroundColor': '#444', 'color': 'white', 'border': '1px solid #555'}, 
                        style_cell={'backgroundColor': '#2b2b2b', 'color': 'white', 'border': '1px solid #444', 'textAlign': 'center'})
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='m4-map-graph', config={'displayModeBar': False}, style={'height': '60vh'})
                ], width=8)
            ])
        ], className="bg-dark")
    ], color="dark")

def layout_eoq():
    return dbc.Card([
        dbc.CardHeader("Modelo de Cantidad Económica de Pedido (EOQ)", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Demanda Anual (unidades):", className="text-light"), 
                    dcc.Input(id='m4-demanda', type='number', value=1200, className="mb-3 form-control bg-dark text-light border-secondary"),
                    html.Label("Costo por Pedido ($):", className="text-light"), 
                    dcc.Input(id='m4-costo-pedido', type='number', value=100, className="mb-3 form-control bg-dark text-light border-secondary"),
                    html.Label("Costo de Mantenimiento ($/unidad/año):", className="text-light"), 
                    dcc.Input(id='m4-costo-mant', type='number', value=2, className="mb-3 form-control bg-dark text-light border-secondary"),
                    
                    html.Hr(className="border-secondary"),
                    html.H4(id='m4-eoq-result', className="text-info")
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='m4-eoq-graph', config={'displayModeBar': False})
                ], width=8)
            ])
        ], className="bg-dark")
    ], color="dark")

def layout_labor():
    return dbc.Card([
        dbc.CardHeader("Asignación Óptima de Recursos", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P("Maximiza la ganancia asignando horas limitadas a 3 proyectos.", className="text-light mb-3"),
                    html.Label("Horas de Labor Disponibles:", className="text-light"), 
                    dcc.Input(id='m4-labor', type='number', value=100, className="mb-3 form-control bg-dark text-light border-secondary"),
                    html.Label("Ganancia Proyecto A ($/h):", className="text-light"), 
                    dcc.Input(id='m4-prof-a', type='number', value=50, className="mb-2 form-control bg-dark text-light border-secondary"),
                    html.Label("Ganancia Proyecto B ($/h):", className="text-light"), 
                    dcc.Input(id='m4-prof-b', type='number', value=40, className="mb-2 form-control bg-dark text-light border-secondary"),
                    html.Label("Ganancia Proyecto C ($/h):", className="text-light"), 
                    dcc.Input(id='m4-prof-c', type='number', value=70, className="form-control bg-dark text-light border-secondary"),
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='m4-labor-graph', config={'displayModeBar': False})
                ], width=8)
            ])
        ], className="bg-dark")
    ], color="dark")