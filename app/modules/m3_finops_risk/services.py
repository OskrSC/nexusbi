import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from prophet import Prophet

def forecast_sales(df_raw, periods=30):
    """
    Usa Prophet para predecir ventas futuras.
    Espera columnas 'Date' (o 'ds') y 'Sales' (o 'y').
    """
    # Estandarizar nombres de columna para Prophet (requiere 'ds' y 'y')
    df = df_raw.copy()
    if 'Date' in df.columns: df.rename(columns={'Date': 'ds'}, inplace=True)
    if 'Sales' in df.columns: df.rename(columns={'Sales': 'y'}, inplace=True)
    
    # Asegurar formato de fecha
    df['ds'] = pd.to_datetime(df['ds'])
    
    # Inicializar y entrenar Prophet (desactivamos logs para no llenar la consola)
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
    model.fit(df)
    
    # Generar fechas futuras
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    
    # Retornar histórico, predicción y el modelo (por si queremos métricas después)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], df

def optimize_price(price_range, demand_range):
    """
    Calcula la curva de elasticidad de precio-demanda y encuentra el óptimo.
    """
    # Simular datos si no hay (para que la pestaña funcione sin subir CSV)
    if price_range is None or demand_range is None:
        prices = np.linspace(10, 25, 50)
        demands = 250 - 8 * prices + np.random.normal(0, 5, 50) # Demanda con ruido
    else:
        prices = np.array(price_range)
        demands = np.array(demand_range)
    
    revenue = prices * demands
    
    # Ajuste polinomial (grado 2 para formar la parábola de ingresos)
    coeffs = np.polyfit(prices, revenue, 2)
    poly_eq = np.poly1d(coeffs)
    
    # Encontrar el precio óptimo (derivada = 0)
    optimal_price = -coeffs[1] / (2 * coeffs[0])
    max_revenue = poly_eq(optimal_price)
    
    # Generar curva suave para graficar
    x_smooth = np.linspace(min(prices), max(prices), 100)
    y_smooth = poly_eq(x_smooth)
    
    return x_smooth, y_smooth, optimal_price, max_revenue

def train_fraud_model_and_predict(df_raw, new_transaction):
    """
    Entrena Random Forest y predice una nueva transacción.
    Espera: Amount, Frequency, IsForeignTransaction, IsHighRiskCountry, IsWeekend, Fraud
    """
    # Separar X e y
    feature_cols = ['Amount', 'Frequency', 'IsForeignTransaction', 'IsHighRiskCountry', 'IsWeekend']
    if not all(col in df_raw.columns for col in feature_cols + ['Fraud']):
        return None, "Error: Faltan columnas requeridas."
        
    X = df_raw[feature_cols]
    y = df_raw['Fraud']
    
    # Entrenar modelo rápido
    model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=3)
    model.fit(X, y)
    
    # Predecir nueva transacción
    df_new = pd.DataFrame([new_transaction])
    prob = model.predict_proba(df_new)[0][1] # Probabilidad de la clase 1 (Fraude)
    
    return prob, "Éxito"