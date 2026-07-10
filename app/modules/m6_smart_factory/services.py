import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pulp

def generate_quality_data_and_detect_anomalies(num_samples=50):
    """
    Simula datos de control de calidad y detecta anomalías con Isolation Forest.
    (Proyectos 816 y 822)
    """
    np.random.seed(42)
    # Simulamos un proceso centrado en 100g con desviación de 2g
    measurements = np.random.normal(loc=100, scale=2, size=num_samples)
    # Inyectamos 3 anomalías a propósito
    measurements[[15, 35, 48]] = [92, 108, 111] 
    
    df = pd.DataFrame({'Sample': np.arange(1, num_samples + 1), 'Measurement': measurements})
    
    # Límites de control estadístico (3 sigma)
    mean_val = np.mean(measurements)
    std_val = np.std(measurements)
    ucl = mean_val + 3 * std_val
    lcl = mean_val - 3 * std_val
    
    # Detección de Anomalías con Machine Learning
    model = IsolationForest(contamination=0.05, random_state=42)
    df['Anomaly'] = model.fit_predict(df[['Measurement']])
    df['Anomaly'] = df['Anomaly'].map({1: 'Normal', -1: 'Anomalía'})
    
    return df, mean_val, ucl, lcl

def predict_time_to_failure(temp, vibration, pressure):
    """
    Predice el tiempo de vida restante (TTF) basado en sensores.
    (Proyecto 819)
    """
    # Simulamos un modelo pre-entrenado (en la vida real cargarías un .pkl)
    # La lógica simulada es: a mayor temp/vibr/presión, menor el tiempo de vida
    ttf = max(0, 100 - (temp * 0.8) - (vibration * 30) - (pressure * 0.5) + np.random.normal(0, 2))
    return round(ttf, 1)

def optimize_energy(total_work, m1_eff, m2_eff, m3_eff, m1_cap, m2_cap, m3_cap):
    """
    Minimiza el consumo de energía (kWh) distribuyendo la carga.
    (Proyecto 820)
    """
    prob = pulp.LpProblem("Energy_Optimization", pulp.LpMinimize)
    
    # Variables: carga asignada a cada máquina
    load = pulp.LpVariable.dicts("Load", ['M1', 'M2', 'M3'], lowBound=0)
    
    # Objetivo: Minimizar kWh (Carga / Eficiencia)
    # Eficiencia es un divisor, pero PuLP no permite divisiones no lineales directas.
    # Transformamos: Minimizar Carga * (1/Eficiencia) = Carga * Costo_kWh
    cost_per_unit = {'M1': 1/m1_eff, 'M2': 1/m2_eff, 'M3': 1/m3_eff}
    prob += pulp.lpSum([load[m] * cost_per_unit[m] for m in ['M1', 'M2', 'M3']])
    
    # Restricciones
    prob += load['M1'] + load['M2'] + load['M3'] == total_work
    prob += load['M1'] <= m1_cap
    prob += load['M2'] <= m2_cap
    prob += load['M3'] <= m3_cap
    
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    if pulp.LpStatus[prob.status] != 'Optimal':
        return []
        
    return [
        {'Machine': m, 'Load_Assigned': int(load[m].varValue), 'kWh_Consumed': round(load[m].varValue * cost_per_unit[m], 2)}
        for m in ['M1', 'M2', 'M3']
    ]