import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

def process_customer_data(df_raw, n_clusters=3):
    """
    Limpia, escala y agrupa clientes usando K-Means.
    Es agnóstico a los nombres de las columnas (busca las numéricas).
    """
    # 1. Seleccionar solo columnas numéricas
    df_numeric = df_raw.select_dtypes(include=[np.number])
    
    if df_numeric.shape[1] < 2:
        raise ValueError("Se necesitan al menos 2 columnas numéricas para hacer clustering.")

    # 2. Manejar datos faltantes (imputación con la media)
    imputer = SimpleImputer(strategy='mean')
    data_imputed = imputer.fit_transform(df_numeric)
    
    # 3. Escalar los datos (Crucial para K-Means)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_imputed)
    
    # 4. Entrenar modelo K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(data_scaled)
    
    # 5. Preparar el DataFrame de resultados
    df_result = df_raw.copy()
    df_result['Cluster'] = clusters
    
    # 6. Calcular centroides en la escala original (para graficar)
    centers_original = scaler.inverse_transform(kmeans.cluster_centers_)
    centers_df = pd.DataFrame(centers_original, columns=df_numeric.columns)
    centers_df['Cluster'] = 'Centroide'
    centers_df['is_centroid'] = True
    df_result['is_centroid'] = False
    
    # Combinar para graficar todo junto
    df_plot = pd.concat([df_result, centers_df], ignore_index=True)
    
    # 7. Calcular métricas de negocio simuladas por clúster (Para la UI)
    cluster_metrics = df_result.groupby('Cluster').size().reset_index(name='Count')
    
    return df_plot, cluster_metrics, df_numeric.columns.tolist()

def calculate_mock_clv_churn(cluster_metrics):
    """
    Simula cálculos de CLV y Churn basados en el tamaño del clúster 
    (Solo para demostrar la inyección de múltiples modelos en la misma vista).
    En un caso real, aquí irían los modelos de Regresión (CLV) y Logístico (Churn).
    """
    total_customers = cluster_metrics['Count'].sum()
    
    # Lógica simulada: El clúster más grande tiene CLV medio, el más pequeño es "Premium"
    results = []
    for _, row in cluster_metrics.iterrows():
        count = row['Count']
        ratio = count / total_customers
        
        if ratio > 0.4:
            results.append({"cluster": row['Cluster'], "clv": f"${np.random.randint(400, 800)}", "churn": "18%"})
        elif ratio < 0.2:
            results.append({"cluster": row['Cluster'], "clv": f"${np.random.randint(1500, 2500)}", "churn": "5%"})
        else:
            results.append({"cluster": row['Cluster'], "clv": f"${np.random.randint(800, 1200)}", "churn": "12%"})
            
    return results