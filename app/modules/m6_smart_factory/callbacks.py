import dash
from dash import Input, Output, html
import plotly.graph_objects as go

from app.modules.m6_smart_factory.services import generate_quality_data_and_detect_anomalies, predict_time_to_failure, optimize_energy
from app.modules.m6_smart_factory.layout import layout_quality, layout_maint, layout_energy

# 1. Navegación
@dash.callback(Output('m6-tab-content', 'children'), Input('m6-tabs', 'value'))
def render_tab(tab):
    if tab == 'tab-quality': return layout_quality()
    elif tab == 'tab-maint': return layout_maint()
    elif tab == 'tab-energy': return layout_energy()

# 2. Gráfico de Control de Calidad
@dash.callback(
    [Output('m6-quality-graph', 'figure'), Output('m6-quality-stats', 'children')],
    Input('m6-tabs', 'value')
)
def update_quality(tab):
    if tab != 'tab-quality': return dash.no_update, dash.no_update
    
    df, mean_val, ucl, lcl = generate_quality_data_and_detect_anomalies()
    
    # Separamos normales de anomalías para colores
    df_norm = df[df['Anomaly'] == 'Normal']
    df_anom = df[df['Anomaly'] == 'Anomalía']
    
    fig = go.Figure()
    
    # Límites de control
    fig.add_hline(y=ucl, line_dash="dash", line_color="red", annotation_text="UCL")
    fig.add_hline(y=lcl, line_dash="dash", line_color="red", annotation_text="LCL")
    fig.add_hline(y=mean_val, line_color="green", annotation_text="Media")
    
    # Puntos normales
    fig.add_trace(go.Scatter(x=df_norm['Sample'], y=df_norm['Measurement'], mode='markers+lines', name='Normal', line=dict(color='cyan'), marker=dict(size=6)))
    # Puntos anómalos (más grandes y rojos)
    fig.add_trace(go.Scatter(x=df_anom['Sample'], y=df_anom['Measurement'], mode='markers', name='Anomalía Detectada', marker=dict(color='red', size=10, symbol='x')))
    
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20))
    
    # Estadísticas
    num_anom = len(df_anom)
    alert_class = "text-danger" if num_anom > 0 else "text-success"
    stats_html = html.Div([
        html.H5(f"Anomalías: {num_anom}", className=alert_class),
        html.P(f"Media: {mean_val:.2f}", className="text-light"),
        html.P(f"Límites: [{lcl:.2f}, {ucl:.2f}]", className="text-muted")
    ])
    return fig, stats_html

# 3. EL GAUGE DE MANTENIMIENTO PREDICTIVO
@dash.callback(
    [Output('m6-ttf-gauge', 'figure'), Output('m6-ttf-alert', 'children')],
    [Input('m6-temp', 'value'), Input('m6-vib', 'value'), Input('m6-pres', 'value')]
)
def update_gauge(temp, vib, pres):
    if not temp: return dash.no_update, dash.no_update
    
    ttf = predict_time_to_failure(float(temp), float(vib), float(pres))
    ttf_clamped = min(max(ttf, 0), 100) # Asegurar que esté entre 0 y 100
    
    # Lógica de colores del Gauge
    if ttf_clamped > 60: color, text = "#00ff00", "ESTADO SALUDABLE"
    elif ttf_clamped > 30: color, text = "#ffff00", "PRECAUCIÓN - REVISAR"
    else: color, text = "#ff0000", "PELIGRO - FALLO INMINENTE"
        
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = ttf_clamped,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Horas de Vida Restantes (TTF)", 'font': {'color': 'white'}},
        number = {'font': {'size': 60, 'color': color}},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': 'white', 'tickfont': {'color': 'white'}},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(255, 0, 0, 0.2)'},
                {'range': [30, 60], 'color': 'rgba(255, 255, 0, 0.2)'},
                {'range': [60, 100], 'color': 'rgba(0, 255, 0, 0.2)'}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=60, b=20))
    
    return fig, html.Span(text, className=f"text-{color.replace('#','')} fs-5")

# 4. Optimizador de Energía
@dash.callback(
    Output('m6-energy-graph', 'figure'),
    [Input('m6-work', 'value'), Input('m6-m1cap', 'value'), Input('m6-m1eff', 'value'),
     Input('m6-m2cap', 'value'), Input('m6-m2eff', 'value')]
)
def update_energy(work, m1c, m1e, m2c, m2e):
    if not work: return dash.no_update
    # Hardcodeamos M3 para no saturar de inputs el layout
    results = optimize_energy(float(work), float(m1e), float(m2e), 6.0, float(m1c), float(m2c), 50.0)
    if not results: return dash.no_update
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[r['Machine'] for r in results], 
        y=[r['kWh_Consumed'] for r in results],
        text=[f"Carga: {r['Load_Assigned']}u" for r in results], 
        textposition='auto',
        marker=dict(color=['#008ffc', '#00e396', '#feb019'])
    ))
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20), yaxis_title="kWh Consumidos")
    return fig