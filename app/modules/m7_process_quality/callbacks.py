import dash
from dash import Input, Output, State, html
import plotly.graph_objects as go
import base64, io
import pandas as pd

from app.modules.m7_process_quality.services import discover_process_map, analyze_support_ticket
from app.modules.m7_process_quality.layout import layout_mining, layout_nlp

# 1. Navegación
@dash.callback(Output('m7-tab-content', 'children'), Input('m7-tabs', 'value'))
def render_tab(tab):
    if tab == 'tab-mining': return layout_mining()
    elif tab == 'tab-nlp': return layout_nlp()

# 2. Dibujo del Grafo de Procesos
@dash.callback(
    [Output('m7-process-graph', 'figure'), Output('m7-mining-status', 'children')],
    Input('m7-log-upload', 'contents'),
    State('m7-log-upload', 'filename'),
    prevent_initial_call=True
)
def update_process_map(contents, filename):
    if not contents: return dash.no_update, dash.no_update
    
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        node_x, node_y, node_names, edge_x, edge_y, edge_weights = discover_process_map(df)
        
        # Dibujar Flechas (Aristas)
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y, mode='lines',
            line=dict(width=2, color='#00ff88'), hoverinfo='text',
            text=[f"Pasó {w} veces" for w in edge_weights]
        )
        
        # Dibujar Nodos (Actividades)
        node_trace = go.Scatter(
            x=node_x, y=node_y, mode='markers+text',
            text=node_names, textposition="bottom center",
            marker=dict(color='#008ffc', size=25, line_width=2, line_color='white'),
            textfont=dict(color='white', size=10)
        )
        
        fig = go.Figure(data=[edge_trace, node_trace])
        fig.update_layout(showlegend=False, template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', 
                          paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=20, b=20),
                          xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                          yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                          
        return fig, html.Span(f"✅ Proceso descubierto: {len(node_names)} actividades encontradas.", className="text-success")
        
    except Exception as e:
        return dash.no_update, html.Span(f"❌ Error: Asegúrate de tener columnas 'CaseID' y 'Activity'. ({str(e)})", className="text-danger")

# 3. Clasificador NLP
@dash.callback(
    [Output('m7-intent-display', 'children'), Output('m7-sentiment-display', 'children'), Output('m7-polarity-display', 'children')],
    Input('m7-ticket-text', 'value')
)
def analyze_ticket(text):
    if not text or len(text) < 5:
        return "Esperando texto...", "-", "0.0"
        
    sentiment, intent, polarity = analyze_support_ticket(text)
    
    # Colores según sentimiento
    color_map = {"Positivo": "text-success", "Negativo": "text-danger", "Neutral": "text-warning"}
    sent_class = color_map.get(sentiment, "text-light")
    
    return intent, html.Span(sentiment, className=sent_class), f"{polarity:.2f}"