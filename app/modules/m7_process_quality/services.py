import pandas as pd
import networkx as nx
from textblob import TextBlob
import pm4py
from pm4py.objects.conversion.log import converter as log_converter

def discover_process_map(df_raw):
    """
    Descubre el mapa de procesos real a partir de un log de eventos.
    Espera columnas: 'CaseID', 'Activity' (y opcionalmente 'Timestamp').
    """
    # Estandarizar nombres para PM4Py
    df = df_raw.copy()
    if 'CaseID' in df.columns: df.rename(columns={'CaseID': 'case:concept:name'}, inplace=True)
    if 'Activity' in df.columns: df.rename(columns={'Activity': 'concept:name'}, inplace=True)
    
    # Asegurar que sea un Event Log válido para PM4Py
    log = log_converter.apply(df)
    
    # Descubrir el Grafo de Seguimiento Directo (Directly-Follows Graph)
    dfg, start_activities, end_activities = pm4py.discover_dfg(log)
    
    # Usar NetworkX para calcular las coordenadas (X, Y) del diagrama
    G = nx.DiGraph()
    
    # Añadir nodos (Actividades)
    for act in dfg.keys():
        G.add_node(act[0])
        G.add_node(act[1])
        
    # Añadir aristas (Transiciones) con el peso (frecuencia)
    for (act1, act2), freq in dfg.items():
        G.add_edge(act1, act2, weight=freq)
        
    # Calcular posición jerárquica (de arriba hacia abajo)
    try:
        pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
    except:
        pos = nx.random_layout(G, seed=42)
        
    # Preparar datos para Plotly
    edge_x, edge_y, edge_weights = [], [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_weights.append(G.edges[edge]['weight'])
        
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_names = list(G.nodes())
    
    return node_x, node_y, node_names, edge_x, edge_y, edge_weights

def analyze_support_ticket(text):
    """
    Analiza un ticket de soporte usando NLP.
    Incluye corrección para texto en español cuando TextBlob falla.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    # --- SOLUCIÓN AL PROBLEMA DEL ESPAÑOL ---
    # Si TextBlob devuelve 0.0, probablemente no entendió el idioma.
    # Activamos nuestro diccionario léxico en español.
    if polarity == 0.0:
        text_lower = text.lower()
        
        # Léxicos básicos de demostración
        negative_words = ["malo", "feo", "horrible", "fallo", "falla", "roto", "harto", "basura", 
                          "lento", "peor", "reembolso", "queja", "error", "inaceptable", 
                          "dañado", "no funciona", "pierdo", "perder", "estafa", "harto"]
        positive_words = ["bueno", "bonito", "excelente", "rápido", "genial", "feliz", 
                          "agradezco", "perfecto", "gracias", "funciona bien"]
        
        neg_count = sum(1 for word in negative_words if word in text_lower)
        pos_count = sum(1 for word in positive_words if word in text_lower)
        
        # Ajustamos la polaridad basándonos en las palabras encontradas (-1.0 a 1.0)
        if neg_count > 0 or pos_count > 0:
            polarity = (pos_count - neg_count) / max(neg_count, pos_count, 1)
            polarity = max(-1.0, min(1.0, polarity)) # Limitar entre -1 y 1

    # Clasificación de Sentimiento (con el polarity ya corregido)
    if polarity > 0.2: sentiment = "Positivo"
    elif polarity < -0.2: sentiment = "Negativo"
    else: sentiment = "Neutral"
    
    # Extracción de Intención
    text_lower = text.lower()
    if any(word in text_lower for word in ["reembolso", "devolución", "dinero", "cargo"]):
        intent = "💸 Finanzas / Devoluciones"
    elif any(word in text_lower for word in ["error", "fallo", "falla", "no funciona", "roto", "bug"]):
        intent = "🔧 Soporte Técnico"
    elif any(word in text_lower for word in ["demora", "dónde está", "llegada", "envío"]):
        intent = "📦 Logística / Envíos"
    else:
        intent = "❓ Consulta General"
        
    return sentiment, intent, polarity