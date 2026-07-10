from dash import html
import dash_bootstrap_components as dbc

# Definición del catálogo de módulos
# Esto es útil porque más adelante podemos usar esta lista para generar permisos o rutas dinámicamente
MODULES_CATALOG = [
    {"id": "m1", "name": "CRM & Marketing", "icon": "bi-people-fill", "href": "/m1-customer"},
    {"id": "m2", "name": "Retail Engine", "icon": "bi-cart-check-fill", "href": "/m2-retail"},
    {"id": "m3", "name": "FinOps & Riesgo", "icon": "bi-cash-stack", "href": "/m3-finops"},
    {"id": "m4", "name": "Supply Chain", "icon": "bi-truck", "href": "/m4-supply"},
    {"id": "m5", "name": "Workforce & PMO", "icon": "bi-person-badge-fill", "href": "/m5-workforce"},
    {"id": "m6", "name": "Smart Factory", "icon": "bi-gear-wide-connected", "href": "/m6-factory"},
    {"id": "m7", "name": "Process & Quality", "icon": "bi-diagram-3-fill", "href": "/m7-process"},
]

def create_sidebar():
    """
    Crea el menú lateral con los 7 módulos de inteligencia de negocio.
    """
    nav_items = []
    for mod in MODULES_CATALOG:
        nav_items.append(
            dbc.NavLink(
                [
                    html.I(className=f"bi {mod['icon']} me-2"),
                    mod["name"]
                ],
                href=mod["href"],
                id=f"link-{mod['id']}",
                active=False, # Se actualizará dinámicamente con callbacks
                className="text-white py-2 px-3 rounded mb-1 sidebar-link"
            )
        )

    return html.Div(
        [
            html.H5("Módulos", className="text-white-50 mb-3 px-3 small fw-bold"),
            dbc.Nav(nav_items, vertical=True, pills=True)
        ],
        className="bg-dark h-100 p-3 shadow",
        style={"minHeight": "calc(100vh - 60px)"} # Calcula la altura exacta restante
    )