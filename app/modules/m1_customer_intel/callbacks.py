import dash
from dash import Input, Output, State, html
import pandas as pd
import plotly.express as px
import base64
import io

# Importamos nuestros servicios puros
from app.modules.m1_customer_intel.services import process_customer_data, calculate_mock_clv_churn

@dash.callback(
    [
        Output('m1-clustering-graph', 'figure'),
        Output('m1-data-status', 'children'),
        Output('m1-clv-value', 'children'),
        Output('m1-churn-value', 'children')
    ],
    [
        Input('m1-upload-data', 'contents'),
        Input('m1-k-clusters', 'value')
    ],
    prevent_initial_call=True # Evita que se ejecute al abrir la página sin datos
)
def update_clustering(contents, n_clusters):
    """
    Se ejecuta cuando el usuario sube un archivo O cambia el slider de clusters.
    """
    # 1. Verificar si hay datos subidos
    if contents is None:
        return dash.no_update, "⚠️ Por favor, sube un archivo CSV.", dash.no_update, dash.no_update

    try:
        # 2. Decodificar el archivo subido (lógica estándar de Dash)
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        if df.empty:
            return dash.no_update, "❌ El archivo está vacío.", dash.no_update, dash.no_update

        # 3. Ejecutar la lógica de Data Science
        df_plot, cluster_metrics, feature_cols = process_customer_data(df, n_clusters)
        business_metrics = calculate_mock_clv_churn(cluster_metrics)

        # 4. Construir el Gráfico 3D Interactivo
        # Seleccionamos las primeras 3 columnas numéricas para los ejes X, Y, Z
        x_col, y_col, z_col = feature_cols[0], feature_cols[1], feature_cols[2] if len(feature_cols) > 2 else feature_cols[1]
        
        fig = px.scatter_3d(
            df_plot, 
            x=x_col, y=y_col, z=z_col, 
            color='Cluster',
            symbol='is_centroid',
            title=f"Segmentación 3D (K={n_clusters})",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            height=500
        )
        
        # Estética del gráfico para que combine con el tema oscuro de NexusBI
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            margin=dict(l=0, r=0, t=30, b=0)
        )
        fig.update_traces(marker_size=4)

        # 5. Formatear la salida de métricas de negocio
        clv_text = html.Ul([html.Li(f"Cluster {m['cluster']}: {m['clv']}") for m in business_metrics], className="small")
        churn_text = html.Ul([html.Li(f"Cluster {m['cluster']}: {m['churn']}") for m in business_metrics], className="small")
        
        status_msg = f"✅ {len(df)} clientes procesados correctamente en {n_clusters} grupos."

        return fig, status_msg, clv_text, churn_text

    except Exception as e:
        # Manejo robusto de errores para no crashear la app
        error_msg = f"❌ Error al procesar: {str(e)}"
        return dash.no_update, error_msg, dash.no_update, dash.no_update