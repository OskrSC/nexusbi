import pandas as pd
import numpy as np
import pulp

# Coordenadas simuladas (Latitud, Longitud) para el mapa
GEO_COORDS = {
    'Warehouse A': {'lat': 40.7128, 'lon': -74.0060}, # Nueva York
    'Warehouse B': {'lat': 41.8781, 'lon': -87.6298}, # Chicago
    'Store X': {'lat': 25.7617, 'lon': -80.1918},     # Miami
    'Store Y': {'lat': 32.7767, 'lon': -96.7970},     # Dallas
    'Store Z': {'lat': 42.3601, 'lon': -71.0589}      # Boston
}

def optimize_transport(supply_a, supply_b):
    warehouses = ['Warehouse A', 'Warehouse B']
    stores = ['Store X', 'Store Y', 'Store Z']
    
    supply = {'Warehouse A': supply_a, 'Warehouse B': supply_b}
    demand = {'Store X': 80, 'Store Y': 120, 'Store Z': 50} 
    
    costs = {
        ('Warehouse A', 'Store X'): 4, ('Warehouse A', 'Store Y'): 5, ('Warehouse A', 'Store Z'): 2,
        ('Warehouse B', 'Store X'): 6, ('Warehouse B', 'Store Y'): 3, ('Warehouse B', 'Store Z'): 7
    }
    
    prob = pulp.LpProblem("Supply_Chain_Optimization", pulp.LpMinimize)
    routes = pulp.LpVariable.dicts("Route", (warehouses, stores), lowBound=0, cat='Continuous')
    
    prob += pulp.lpSum([routes[w][s] * costs[(w, s)] for w in warehouses for s in stores])
    
    for w in warehouses:
        prob += pulp.lpSum([routes[w][s] for s in stores]) <= supply[w]
    for s in stores:
        prob += pulp.lpSum([routes[w][s] for w in warehouses]) == demand[s]
        
    # Silenciar los logs enormes de PuLP en consola
    prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    # --- LA SOLUCIÓN AL CONGELAMIENTO ---
    # Verificamos si el problema tiene solución real
    status = pulp.LpStatus[prob.status]
    if status != 'Optimal':
        # Si es infactible, devolvemos estructuras vacías y un mensaje de error
        return pd.DataFrame(), f"⚠️ ERROR: {status} (Oferta insuficiente)", []
        
    results = []
    map_routes = []
    total_cost = 0
    
    for w in warehouses:
        for s in stores:
            amount = routes[w][s].varValue
            if amount and amount > 0:
                cost_incurred = amount * costs[(w, s)]
                total_cost += cost_incurred
                results.append({
                    'Origen': w, 'Destino': s, 'Unidades': int(amount), 
                    'Costo/Unidad': costs[(w,s)], 'Costo Total': cost_incurred
                })
                map_routes.append({
                    'start_lat': GEO_COORDS[w]['lat'], 'start_lon': GEO_COORDS[w]['lon'],
                    'end_lat': GEO_COORDS[s]['lat'], 'end_lon': GEO_COORDS[s]['lon'],
                    'amount': amount
                })
                
    return pd.DataFrame(results), total_cost, map_routes

def calculate_eoq(annual_demand, ordering_cost, holding_cost):
    if not annual_demand or not ordering_cost or not holding_cost or holding_cost == 0: return 0,0,0,0,0
    eoq = np.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
    num_orders = annual_demand / eoq
    total_order_cost = num_orders * ordering_cost
    total_hold_cost = (eoq / 2) * holding_cost
    total_cost = total_order_cost + total_hold_cost
    return eoq, num_orders, total_order_cost, total_hold_cost, total_cost

def optimize_resources(labor_available, profit_a, profit_b, profit_c):
    prob = pulp.LpProblem("Resource_Allocation", pulp.LpMaximize)
    hours = pulp.LpVariable.dicts("Hours", ['A', 'B', 'C'], lowBound=0)
    prob += hours['A'] * profit_a + hours['B'] * profit_b + hours['C'] * profit_c
    prob += hours['A'] + hours['B'] + hours['C'] <= labor_available
    prob += hours['A'] <= 40
    prob += hours['B'] <= 50
    prob += hours['C'] <= 30
    prob.solve(pulp.PULP_CBC_CMD(msg=False)) # Silenciar logs
    
    if pulp.LpStatus[prob.status] != 'Optimal':
        return []
        
    return [
        {'Proyecto': p, 'Horas Asignadas': int(hours[p].varValue), 'Ganancia': int(hours[p].varValue * profit)}
        for p, profit in zip(['A', 'B', 'C'], [profit_a, profit_b, profit_c])
    ]