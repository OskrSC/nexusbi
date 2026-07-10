import networkx as nx
import pandas as pd

# Datos estáticos de un proyecto de ejemplo (Proyecto 814)
PROJECT_TASKS = {
    'Inicio': {'duration': 0, 'deps': []},
    'Diseño UI': {'duration': 3, 'deps': ['Inicio']},
    'Backend DB': {'duration': 4, 'deps': ['Inicio']},
    'Frontend Dev': {'duration': 5, 'deps': ['Diseño UI']},
    'API Dev': {'duration': 6, 'deps': ['Backend DB']},
    'Testing QA': {'duration': 3, 'deps': ['Frontend Dev', 'API Dev']},
    'Despliegue': {'duration': 1, 'deps': ['Testing QA']}
}

def calculate_cpm(tasks):
    """Calcula el Camino Crítico y genera posiciones para el gráfico."""
    G = nx.DiGraph()
    
    for task, info in tasks.items():
        G.add_node(task, duration=info['duration'])
        for dep in info['deps']:
            G.add_edge(dep, task, weight=info['duration'])
            
    # Calcular el camino más largo (Camino Crítico)
    try:
        critical_path = nx.dag_longest_path(G, weight='weight')
        critical_duration = nx.dag_longest_path_length(G, weight='weight')
    except nx.NetworkXUnfeasible:
        return None, None, None, "El grafo tiene ciclos (imposible)"
        
    # Generar coordenadas (X, Y) para dibujar en Plotly de izquierda a derecha
    pos = {}
    # Asignar X basado en la distancia desde el inicio (topológica)
    lengths = nx.single_source_shortest_path_length(G, 'Inicio')
    max_len = max(lengths.values()) if lengths else 1
    
    y_counters = {}
    for node, dist in lengths.items():
        x = dist * 2 # Escalar en X
        if dist not in y_counters:
            y_counters[dist] = 0
        else:
            y_counters[dist] -= 1.5 # Separar en Y
        pos[node] = (x, y_counters[dist])
        
    # Preparar datos para las flechas (edges)
    edge_x, edge_y, edge_text = [], [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
    return pos, critical_path, (edge_x, edge_y), critical_duration

def evaluate_risks(risk_data):
    """Evalúa la matriz de riesgos y clasifica."""
    df = pd.DataFrame(risk_data)
    df['Risk_Score'] = df['Probability'] * df['Impact']
    
    # Lógica de cuadrantes
    def get_quadrant(row):
        if row['Probability'] >= 3 and row['Impact'] >= 4: return 'Crítico'
        if row['Probability'] >= 3 or row['Impact'] >= 4: return 'Alto'
        if row['Probability'] >= 2 and row['Impact'] >= 2: return 'Medio'
        return 'Bajo'
        
    df['Quadrant'] = df.apply(get_quadrant, axis=1)
    return df