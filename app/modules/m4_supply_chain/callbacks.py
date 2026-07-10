import dash
from dash import Input, Output, html
import plotly.graph_objects as go
import numpy as np

from app.modules.m4_supply_chain.services import optimize_transport, calculate_eoq, optimize_resources, GEO_COORDS
from app.modules.m4_supply_chain.layout import layout_transport, layout_eoq, layout_labor

@dash.callback(Output('m4-tab-content', 'children'), Input('m4-tabs', 'value'))
def render_tab(tab):
    if tab == 'tab-transport': return layout_transport()
    elif tab == 'tab-eoq': return layout_eoq()
    elif tab == 'tab-labor': return layout_labor()

@dash.callback(
    [Output('m4-map-graph', 'figure'), Output('m4-routes-table', 'data'), Output('m4-total-cost', 'children')],
    [Input('m4-sup-a', 'value'), Input('m4-sup-b', 'value')]
)
def update_map(sup_a, sup_b):
    df_routes, total_cost, map_data = optimize_transport(sup_a, sup_b)
    
    fig = go.Figure()
    
    # Dibujar nodos siempre
    for name, coords in GEO_COORDS.items():
        color = 'blue' if 'Warehouse' in name else 'red'
        fig.add_trace(go.Scattergeo(
            lon=[coords['lon']], lat=[coords['lat']],
            mode='markers+text', text=[name.split()[1]], textposition="bottom center",
            marker=dict(size=15, color=color), showlegend=False, textfont=dict(color="white")
        ))
            
    # MANEJO DE ERRORES: Si total_cost es un string, hubo infactibilidad
    if isinstance(total_cost, str):
        fig.update_layout(
            mapbox_style="carto-darkmatter", geo=dict(scope='usa', projection_type='albers usa', showland=True, landcolor="#222"),
            margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
        return fig, [], html.Span(total_cost, className="text-danger fs-4") # Muestra el error en rojo

    # Si todo es óptimo, dibujar las rutas
    lons, lats = [], []
    for route in map_data:
        lons.extend([route['start_lon'], route['end_lon'], None])
        lats.extend([route['start_lat'], route['end_lat'], None])
        
    if lons:
        fig.add_trace(go.Scattergeo(lon=lons, lat=lats, mode='lines', line=dict(width=2, color='cyan'), opacity=0.7, showlegend=False))

    fig.update_layout(
        mapbox_style="carto-darkmatter", geo=dict(scope='usa', projection_type='albers usa', showland=True, landcolor="#222"),
        margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)')
        
    return fig, df_routes.to_dict('records'), f"${total_cost:,.2f}"

@dash.callback(
    [Output('m4-eoq-graph', 'figure'), Output('m4-eoq-result', 'children')],
    [Input('m4-demanda', 'value'), Input('m4-costo-pedido', 'value'), Input('m4-costo-mant', 'value')]
)
def update_eoq(d, s, h):
    if not d or not s or not h or h==0: return dash.no_update, dash.no_update
    eoq, num_ord, cost_ord, cost_mant, cost_tot = calculate_eoq(float(d), float(s), float(h))
    if eoq == 0: return dash.no_update, dash.no_update
    
    cycle_days = 365 / num_ord
    time = np.linspace(0, 365, 1000)
    inventory = eoq - (eoq / cycle_days) * (time % cycle_days)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=inventory, mode='lines', line=dict(color='#00ff88')))
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20), yaxis_title="Unidades", xaxis_title="Días")
    
    result_text = f"EOQ: {eoq:,.0f} uds<br>Pedidos/Año: {num_ord:,.1f}<br>Costo Total: ${cost_tot:,.2f}"
    return fig, html.P(result_text, className="text-light")

@dash.callback(
    Output('m4-labor-graph', 'figure'),
    [Input('m4-labor', 'value'), Input('m4-prof-a', 'value'), Input('m4-prof-b', 'value'), Input('m4-prof-c', 'value')]
)
def update_labor(labor, pa, pb, pc):
    if not labor: return dash.no_update
    results = optimize_resources(float(labor), float(pa), float(pb), float(pc))
    if not results: return dash.no_update
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[r['Proyecto'] for r in results], y=[r['Horas Asignadas'] for r in results],
        text=[f"${r['Ganancia']}" for r in results], textposition='auto',
        marker=dict(color=['#008ffc', '#00e396', '#feb019'])
    ))
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20), yaxis_title="Horas Asignadas")
    return fig