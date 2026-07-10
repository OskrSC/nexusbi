from dash import html, dcc
import dash_bootstrap_components as dbc

def layout():
    return dbc.Container([
        html.H2("Módulo 5: Workforce & PMO", className="mt-4 mb-4 text-light"),
        
        dcc.Tabs(id='m5-tabs', value='tab-cpm', className="mb-4 text-light", style={"fontWeight": "bold"}, children=[
            dcc.Tab(label='🔗 Camino Crítico (CPM)', value='tab-cpm', className="text-light"),
            dcc.Tab(label='⚠️ Matriz de Riesgos', value='tab-risk', className="text-light")
        ]),
        
        # Le inyectamos el layout por defecto directamente al contenedor
        html.Div(id='m5-tab-content', children=layout_cpm())
    ], fluid=True)

def layout_cpm():
    return dbc.Card([
        dbc.CardHeader("Análisis de Camino Crítico (Project 814)", className="bg-secondary text-light"),
        dbc.CardBody([
            html.P("Visualización del flujo de tareas de un proyecto de software. Los nodos rojos representan el camino crítico (cualquier retraso aquí retrasa todo el proyecto).", className="text-light mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.H5("Diagrama de Red:", className="text-light"),
                    dcc.Graph(id='m5-cpm-graph', config={'displayModeBar': False}, style={'height': '50vh'})
                ], width=8),
                dbc.Col([
                    html.H5("Resumen del Proyecto:", className="text-light"),
                    html.H3(id='m5-cpm-duration', className="text-success mb-4"),
                    html.Hr(className="border-secondary"),
                    html.P("Tareas en el Camino Crítico:", className="text-light mt-3"),
                    html.Ul(id='m5-cpm-tasks', className="list-group")
                ], width=4)
            ])
        ], className="bg-dark")
    ], color="dark")

def layout_risk():
    # Generamos controles dinámicos para 5 riesgos de ejemplo
    risk_inputs = []
    default_risks = [
        {'name': 'Falta de Personal', 'p': 4, 'i': 5},
        {'name': 'Presuesto Insuficiente', 'p': 3, 'i': 4},
        {'name': 'Fallo de Servidor', 'p': 2, 'i': 5},
        {'name': 'Retraso Proveedor', 'p': 3, 'i': 3},
        {'name': 'Cambio de Requisitos', 'p': 5, 'i': 2}
    ]
    
    for r in default_risks:
        risk_inputs.append(
            html.Div([
                html.Span(r['name'], className="text-light me-2", style={"width": "180px", "display": "inline-block"}),
                html.Span("Prob:", className="text-muted me-1"),
                dcc.Input(id=f'risk-p-{r["name"]}', type='number', value=r['p'], min=1, max=5, style={'width': '40px', 'display': 'inline-block', 'marginRight': '10px'}),
                html.Span("Imp:", className="text-muted me-1"),
                dcc.Input(id=f'risk-i-{r["name"]}', type='number', value=r['i'], min=1, max=5, style={'width': '40px', 'display': 'inline-block'})
            ], className="mb-2")
        )

    return dbc.Card([
        dbc.CardHeader("Matriz de Riesgos (Project 815)", className="bg-secondary text-light"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P("Ajusta la Probabilidad (1-5) y el Impacto (1-5) para ver cómo se mueven los riesgos en la matriz.", className="text-light mb-4"),
                    *risk_inputs # Desempaqueta los inputs
                ], width=4),
                dbc.Col([
                    dcc.Graph(id='m5-risk-matrix', config={'displayModeBar': False}, style={'height': '60vh'})
                ], width=8)
            ])
        ], className="bg-dark")
    ], color="dark")