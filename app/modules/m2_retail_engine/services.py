import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from sklearn.metrics.pairwise import cosine_similarity

def analyze_market_basket(df_raw, min_support=0.3, min_confidence=0.6):
    """
    Procesa datos de transacciones para encontrar reglas de asociación.
    Asume que el CSV tiene una columna de texto con productos separados por comas,
    O que ya está en formato one-hot (0s y 1s).
    """
    # Caso 1: Detectar si es formato texto (ej. columna 'Items' con "leche,pan")
    if df_raw.shape[1] == 1 or df_raw.select_dtypes(include=['object']).shape[1] == df_raw.shape[1]:
        # Tomar la primera columna y convertirla en lista de listas
        transactions = df_raw.iloc[:, 0].astype(str).apply(lambda x: [item.strip() for item in x.split(',')]).tolist()
        
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    else:
        # Caso 2: Ya viene en formato one-hot numérico
        df_encoded = df_raw.applymap(lambda x: True if x == 1 or x == True else False)

    # Ejecutar Apriori
    frequent_items = apriori(df_encoded, min_support=min_support, use_colnames=True)
    
    if frequent_items.empty:
        return pd.DataFrame() # No se encontraron patrones
    
    # Generar Reglas
    rules = association_rules(frequent_items, metric="confidence", min_threshold=min_confidence)
    
    # Formatear para la tabla de Dash (convertir frozensets a strings legibles)
    if not rules.empty:
        rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
        rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
        # Seleccionar y renombrar columnas clave
        rules = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
        rules.columns = ['Si compra (A)', 'También compra (B)', 'Soporte', 'Confianza', 'Lift']
        rules = rules.sort_values(by='Lift', ascending=False).reset_index(drop=True)
        
    return rules

def get_recommendations(df_raw, user_id, top_n=3):
    """
    Genera recomendaciones basadas en filtrado colaborativo de usuarios.
    Espera un CSV con columnas: User_ID, Item_ID, Rating.
    """
    # Crear matriz pivote (Filas=Usuarios, Columnas=Items, Valores=Rating)
    df_pivot = df_raw.pivot_table(index='User_ID', columns='Item_ID', values='Rating')
    
    # Rellenar NaN con 0 para calcular similitud
    df_pivot_filled = df_pivot.fillna(0)
    
    # Calcular similitud del coseno entre usuarios
    similarity_matrix = cosine_similarity(df_pivot_filled)
    sim_df = pd.DataFrame(similarity_matrix, index=df_pivot.index, columns=df_pivot.index)
    
    if user_id not in sim_df.index:
        return [], "Usuario no encontrado en los datos."
    
    # Obtener usuarios más similares (excluyendo al propio usuario)
    similar_users = sim_df[user_id].sort_values(ascending=False).index[1:top_n+2]
    
    # Calcular puntajes ponderados para items que el usuario NO ha valorado
    user_rated = df_pivot.loc[user_id].dropna().index
    scores = pd.Series(dtype=float)
    
    for sim_user in similar_users:
        sim_score = sim_df[user_id][sim_user]
        # Items valorados por el usuario similar que el target no ha visto
        items_to_rec = df_pivot.loc[sim_user].drop(index=user_rated).dropna()
        scores = pd.concat([scores, items_to_rec * sim_score])
    
    # Agrupar por item y obtener el promedio ponderado
    top_items = scores.groupby(scores.index).mean().sort_values(ascending=False).head(top_n)
    
    return list(top_items.items()), "Éxito"