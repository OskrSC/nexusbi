import dash
from dash import Input, Output, html
import plotly.graph_objects as go

from app.modules.m5_workforce_pmo.services import calculate_cpm, evaluate_risks, PROJECT_TASKS
from app.modules.m5_workforce_pmo.layout import layout_cpm, layout_risk

# 1. Navegación
@dash.callback(Output('m5-tab-content', 'children'), Input('m5-tabs', 'value'))
def render_tab(tab):
    if tab == 'tab-cpm': return layout_cpm()
    elif tab == 'tab-risk': return layout_risk()

# 2. Dibujo del Grafo del Camino Crítico
@dash.callback(
    [Output('m5-cpm-graph', 'figure'), Output('m5-cpm-duration', 'children'), Output('m5-cpm-tasks', 'children')],
    Input('m5-tabs', 'value')
)
def update_cpm(tab):
    if tab != 'tab-cpm': return dash.no_update, dash.no_update, dash.no_update
    
    pos, critical_path, edges_data, duration = calculate_cpm(PROJECT_TASKS)
    
    # Separar nodos críticos y no críticos
    node_x, node_y, node_text, node_color = [], [], [], []
    for node, (x, y) in pos.items():
        node_x.append(x)
        node_y.append(y)
        dur = PROJECT_TASKS[node]['duration']
        node_text.append(f"{node}<br>({dur}d)")
        # Rojo si está en el camino crítico, gris si no
        node_color.append('red' if node in critical_path else '#6c757d')
        
    # Crear flechas (edges)
    edge_trace = go.Scatter(
        x=edges_data[0], y=edges_data[1],
        line=dict(width=1, color='#444'), hoverinfo='none', mode='lines'
    )
    
    # Crear nodos
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text', text=node_text,
        textposition="bottom center", marker=dict(color=node_color, size=30, line_width=2, line_color='white'),
        textfont=dict(color='white', size=10)
    )
    
    fig = go.Figure(data=[edge_trace, node_trace])
    # Quitar ejes para que parezca un diagrama de red real
    fig.update_layout(showlegend=False, template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', 
                      paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20),
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    
    # Generar lista HTML de tareas críticas
    tasks_html = [html.Li(task, className="list-group-item bg-dark text-danger border-secondary") for task in critical_path]
    
    return fig, f"Duración Mínima: {duration} días", tasks_html

# 3. Matriz de Riesgos Dinámica
@dash.callback(
    Output('m5-risk-matrix', 'figure'),
    [Input(f'risk-p-{r["name"]}', 'value') for r in [{'name': 'Falta de Personal'}, {'name': 'Presuesto Insuficiente'}, {'name': 'Fallo de Servidor'}, {'name': 'Retraso Proveedor'}, {'name': 'Cambio de Requisitos'}]] +
    [Input(f'risk-i-{r["name"]}', 'value') for r in [{'name': 'Falta de Personal'}, {'name': 'Presuesto Insuficiente'}, {'name': 'Fallo de Servidor'}, {'name': 'Retraso Proveedor'}, {'name': 'Cambio de Requisitos'}]]
)
def update_risk_matrix(*args):
    # Reconstruir el diccionario de riesgos desde los inputs
    names = ['Falta de Personal', 'Presuesto Insuficiente', 'Fallo de Servidor', 'Retraso Proveedor', 'Cambio de Requisitos']
    risk_data = []
    
    for i, name in enumerate(names):
        risk_data.append({
            'Risk': name,
            'Probability': args[i] if args[i] else 1,
            'Impact': args[i+5] if args[i+5] else 1 # Los últimos 5 inputs son el Impacto
        })
        
    df = evaluate_risks(risk_data)
    
    # Colores por cuadrante
    color_map = {'Crítico': '#ff0000', 'Alto': '#ff8c00', 'Medio': '#ffff00', 'Bajo': '#00ff00'}
    colors = [color_map[q] for q in df['Quadrant']]
    
    fig = go.Figure()
    
    # Dibujar cuadrantes de fondo (shapes)
    fig.add_shape(type="rect", x0=0.5, y0=3.5, x1=2.5, y1=5.5, fillcolor="green", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=2.5, y0=3.5, x1=5.5, y1=5.5, fillcolor="orange", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=0.5, y0=0.5, x1=2.5, y1=3.5, fillcolor="yellow", opacity=0.1, line_width=0)
    fig.add_shape(type="rect", x0=2.5, y0=0.5, x1=5.5, y1=3.5, fillcolor="red", opacity=0.1, line_width=0)
    
    # Dibujar riesgos como burbujas
    fig.add_trace(go.Scatter(
        x=df['Probability'], y=df['Impact'], 
        mode='markers+text', text=df['Risk'], textposition="top center",
        marker=dict(size=df['Risk_Score']*3, color=colors, opacity=0.8, line=dict(width=1, color='white')),
        textfont=dict(color='white', size=10)
    ))
    
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                      margin=dict(l=20, r=20, t=20, b=20),
                      xaxis=dict(title="Probabilidad", range=[0.5, 5.5], dtick=1, gridcolor='#444'),
                      yaxis=dict(title="Impacto", range=[0.5, 5.5], dtick=1, gridcolor='#444'))
    return fig