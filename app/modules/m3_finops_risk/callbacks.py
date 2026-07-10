import dash
from dash import Input, Output, State, html
import pandas as pd
import plotly.graph_objects as go
import base64, io

from app.modules.m3_finops_risk.services import forecast_sales, optimize_price, train_fraud_model_and_predict
from app.modules.m3_finops_risk.layout import layout_forecast, layout_pricing, layout_fraud

# 1. Navegación de Pestañas
@dash.callback(Output('m3-tab-content', 'children'), Input('m3-tabs', 'value'))
def render_tab(tab):
    if tab == 'tab-forecast': return layout_forecast()
    elif tab == 'tab-price': return layout_pricing()
    elif tab == 'tab-fraud': return layout_fraud()

# 2. Forecasting (Prophet) - VERSIÓN VISUAL MEJORADA (ÚNICA)
@dash.callback(
    [Output('m3-forecast-store', 'data'), Output('m3-forecast-graph', 'figure')],
    [Input('m3-forecast-upload', 'contents'), Input('m3-periods', 'value')],
    prevent_initial_call=True
)
def update_forecast(contents, periods):
    if contents is None:
        return dash.no_update, dash.no_update
        
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        forecast_df, hist_df = forecast_sales(df, periods=periods)
        
        fig = go.Figure()
        
        # 1. Intervalo de Confianza (Sombreado)
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'], y=forecast_df['yhat_upper'], 
            mode='lines', line=dict(width=0), showlegend=True, name='Margen de Error'
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'], y=forecast_df['yhat_lower'], 
            mode='lines', fill='tonexty', fillcolor='rgba(0, 255, 255, 0.1)', 
            line=dict(width=0), showlegend=False
        ))

        # 2. Línea de Predicción
        fig.add_trace(go.Scatter(
            x=forecast_df['ds'], y=forecast_df['yhat'], 
            mode='lines', name='Tendencia (Prophet)', 
            line=dict(color='cyan', width=2.5)
        ))
        
        # 3. Datos Reales (Puntos)
        fig.add_trace(go.Scatter(
            x=hist_df['ds'], y=hist_df['y'], 
            mode='markers+text', 
            name='Ventas Reales', 
            marker=dict(color='white', size=8, symbol='circle'),
            textposition="top center",
            text=hist_df['y'].apply(lambda x: f"{x:,.0f}"), 
            textfont=dict(color="white", size=9)
        ))

        fig.update_layout(
            template='plotly_dark', 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            margin=dict(l=40, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode='x unified'
        )
        fig.update_yaxes(tickformat=",.0f")
        
        return contents, fig
    except Exception as e:
        print(f"Error Forecast: {e}")
        return dash.no_update, dash.no_update

# 3. Price Optimizer
@dash.callback(
    [Output('m3-price-graph', 'figure'), Output('m3-optimal-price', 'children'), Output('m3-max-revenue', 'children')],
    Input('m3-tabs', 'value'),
    prevent_initial_call=False
)
def update_pricing(tab):
    if tab != 'tab-price':
        return dash.no_update, dash.no_update, dash.no_update
        
    x_smooth, y_smooth, opt_price, max_rev = optimize_price(None, None)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', name='Ingresos Proyectados', line=dict(color='#00ff88', width=3)))
    fig.add_trace(go.Scatter(x=[opt_price], y=[max_rev], mode='markers', name='Punto Óptimo', marker=dict(color='red', size=12)))
    
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=20, r=20, t=30, b=20),
                     yaxis_title="Ingresos ($)", xaxis_title="Precio ($)")

    return fig, f"${opt_price:.2f}", f"Ingresos Máximos Estimados: ${max_rev:.2f}"

# 4. Fraud Simulator
@dash.callback(
    Output('m3-fraud-result', 'children'),
    [Input('m3-fraud-store', 'data'), Input('f-amount', 'value'), Input('f-freq', 'value'), 
     Input('f-foreign', 'value'), Input('f-risk', 'value'), Input('f-weekend', 'value')],
    prevent_initial_call=True
)
def evaluate_fraud(contents, amount, freq, foreign, risk, weekend):
    if contents is None:
        return html.H4("⚠️ Sube un archivo CSV histórico para activar el simulador.", className="text-warning mt-5")
        
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        new_tx = {
            'Amount': float(amount), 'Frequency': float(freq), 
            'IsForeignTransaction': float(foreign), 'IsHighRiskCountry': float(risk), 
            'IsWeekend': float(weekend)
        }
        
        prob, status = train_fraud_model_and_predict(df, new_tx)
        
        prob_pct = prob * 100
        if prob_pct > 70:
            color, text, icon = "danger", "ALERTA DE FRAUDE", "🚨"
        elif prob_pct > 40:
            color, text, icon = "warning", "TRANSACCIÓN SOSPECHOSA", "⚠️"
        else:
            color, text, icon = "success", "TRANSACCIÓN SEGURA", "✅"
            
        return html.Div([
            html.H1(f"{icon} {prob_pct:.1f}%", className=f"text-{color} mt-5"),
            html.H3(text, className=f"text-{color}")
        ])
    except Exception as e:
        return html.P(f"Error: {str(e)}", className="text-danger")

# Guardar archivo de fraude en Store
@dash.callback(Output('m3-fraud-store', 'data'), Input('m3-fraud-upload', 'contents'), prevent_initial_call=True)
def store_fraud(contents): 
    return contents