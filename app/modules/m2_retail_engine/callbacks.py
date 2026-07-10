import dash
from dash import Input, Output, State, html
import pandas as pd
import base64
import io

from app.modules.m2_retail_engine.services import analyze_market_basket, get_recommendations
from app.modules.m2_retail_engine.layout import layout_basket, layout_recommender

# 1. Callback para cambiar el contenido de las pestañas
@dash.callback(
    Output('m2-tab-content', 'children'),
    Input('m2-tabs', 'value')
)
def render_tab(tab):
    if tab == 'tab-basket':
        return layout_basket()
    elif tab == 'tab-rec':
        return layout_recommender()

# 2. Callback para Análisis de Canasta (CORREGIDO)
@dash.callback(
    Output('m2-rules-table', 'data'),
    [Input('m2-support', 'value'), Input('m2-confidence', 'value'), Input('m2-basket-upload', 'contents')],
    State('m2-basket-upload', 'filename'),
    prevent_initial_call=True  # <-- CAMBIO CRÍTICO AQUÍ
)
def update_basket(support, confidence, contents, filename):
    # Si no hay archivo, no hace nada
    if contents is None:
        return dash.no_update
    
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        rules_df = analyze_market_basket(df, min_support=support, min_confidence=confidence)
        
        # Si el dataframe está vacío, devuelve una lista vacía para limpiar la tabla
        if rules_df.empty:
            return []
            
        return rules_df.to_dict('records')
    except Exception as e:
        print(f"Error en Basket: {e}")
        return []

# 3. Callback para poblar el Dropdown de Usuarios
@dash.callback(
    [Output('m2-dropdown-container', 'style'), Output('m2-user-dropdown', 'options'), Output('m2-user-dropdown', 'value')],
    Input('m2-rec-upload', 'contents'),
    State('m2-rec-upload', 'filename'),
    prevent_initial_call=True
)
def populate_users(contents, filename):
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        users = df['User_ID'].unique()
        options = [{'label': str(u), 'value': u} for u in users]
        
        return {'display': 'block'}, options, users[0]
    except Exception as e:
        print(f"Error cargando usuarios: {e}")
        return {'display': 'none'}, dash.no_update, dash.no_update

# 4. Callback para obtener Recomendaciones
@dash.callback(
    Output('m2-rec-list', 'children'),
    [Input('m2-user-dropdown', 'value'), Input('m2-rec-upload', 'contents')],
    prevent_initial_call=True
)
def update_recommendations(user_id, contents):
    if user_id is None or contents is None:
        return dash.no_update
        
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        recs, status = get_recommendations(df, user_id, top_n=4)
        
        if not recs:
            return html.Li("No se encontraron recomendaciones suficientes para este usuario.", className="list-group-item bg-dark text-white border-secondary")
            
        rec_items = []
        for item, score in recs:
            rec_items.append(html.Li([
                html.Div([
                    html.Strong(f"Producto: {item}"),
                    html.Br(),
                    html.Small(f"Puntuación estimada: {score:.2f}", className="text-muted")
                ], className="ms-2 me-auto")
            ], className="list-group-item bg-dark text-white border-secondary d-flex justify-content-between align-items-center"))
            
        return rec_items
    except Exception as e:
        return html.Li(f"Error al procesar recomendaciones: {str(e)}", className="list-group-item bg-danger text-white")