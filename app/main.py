import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Importar configuración e inicializar directorios
from app.config import settings
settings.initialize()

# Importar componentes de UI
from app.components.navbar import create_navbar
from app.components.sidebar import create_sidebar, MODULES_CATALOG

# Importar layouts de los módulos (por ahora solo el M1, los demás serán placeholders)
from app.modules.m1_customer_intel.layout import layout as m1_layout
from app.modules.m2_retail_engine.layout import layout as m2_layout
from app.modules.m3_finops_risk.layout import layout as m3_layout
from app.modules.m4_supply_chain.layout import layout as m4_layout
from app.modules.m5_workforce_pmo.layout import layout as m5_layout
from app.modules.m6_smart_factory.layout import layout as m6_layout
from app.modules.m7_process_quality.layout import layout as m7_layout # <-- NUEVO

# --- INICIALIZACIÓN DE LA APP DASH ---
# Usamos el tema BOOTSTRAP (Cyborg es oscuro y se ve muy SaaS/Enterprise)
server_app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True, 
    title="NexusBI - Enterprise Analytics"
)
# Exponemos el servidor Flask subyacente (útil para Docker/FastAPI futuro)
server = server_app.server 

# --- LAYOUT PRINCIPAL (El Esqueleto) ---
server_app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False), # Escucha los cambios en la URL de forma invisible
        create_navbar(),                       # Barra superior fija
        
        dbc.Container(
            [
                dbc.Row(
                    [
                        # Columna izquierda para el Sidebar
                        dbc.Col(
                            create_sidebar(),
                            width=2, 
                            className="p-0 m-0 d-none d-md-block" # Se oculta en móviles pequeños
                        ),
                        # Columna derecha para el Contenido Dinámico
                        dbc.Col(
                            html.Div(id='page-content', className="p-4"),
                            width=10
                        )
                    ],
                    className="g-0" # Sin gutters (espaciado) para que el sidebar pegue a la derecha
                )
            ],
            fluid=True,
            className="p-0 m-0",
            style={"backgroundColor": "#2b2b2b"} # Fondo que combina con Cyborg theme
        )
    ],
    style={"height": "100vh", "display": "flex", "flexDirection": "column"}
)

# --- CALLBACKS GLOBALES ---

# 1. Enrutador de Páginas (El Motor SPA)
@server_app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """
    Este callback intercepta los clicks del sidebar y renderiza
    el layout del módulo correspondiente sin recargar la página web.
    """
    if pathname == '/' or pathname is None:
        # Página de inicio (Dashboard por defecto)
        return html.Div([
            html.H1("Bienvenido a NexusBI", className="text-center mt-5"),
            html.P("Selecciona un módulo en el menú lateral para comenzar.", className="text-center text-muted")
        ])
    elif pathname == '/m1-customer':
        return m1_layout()
    
    # --- PLACEHOLDERS PARA LOS OTROS 6 MÓDULOS ---
    # (Los iremos reemplazando en los siguientes pasos)
    elif pathname == '/m2-retail':
        return m2_layout()
    elif pathname == '/m3-finops':
        return m3_layout()
    elif pathname == '/m4-supply':
        return m4_layout()
    elif pathname == '/m5-workforce':
        return m5_layout()
    elif pathname == '/m6-factory':
        return m6_layout()
    elif pathname == '/m7-process':
        return m7_layout()
    
    return html.Div([html.H1("404: Página no encontrada"), dcc.Link("Volver al inicio", href="/")])

# 2. Resaltado del Sidebar (UX Profesional)
@server_app.callback(
    [Output(f"link-{mod['id']}", "active") for mod in MODULES_CATALOG],
    Input('url', 'pathname')
)
def update_active_nav_link(pathname):
    """
    Ilumina el botón del sidebar correspondiente a la página actual.
    Devuelve una lista de booleanos (True para el activo, False para los demás).
    """
    return [pathname == mod["href"] for mod in MODULES_CATALOG]


# --- UTILIDADES ---
def generate_placeholder(title, projects_text):
    """Genera una tarjeta visual para los módulos que aún no están construidos."""
    return dbc.Card(
        dbc.CardBody([
            html.H2(f"🚧 {title}", className="text-warning mb-3"),
            html.P(f"Módulo en desarrollo. Integrará los proyectos: {projects_text}."),
            html.P("El enrutamiento, la base de datos y la caché ya están listos para este módulo.", 
                   className="text-muted")
        ]),
        color="dark", 
        className="mt-4 border border-warning"
    )

# --- REGISTRO DE MÓDULOS ---
# Al importar los callbacks, Dash registra automáticamente las interacciones de ese módulo
import app.modules.m1_customer_intel.callbacks
import app.modules.m2_retail_engine.callbacks
import app.modules.m3_finops_risk.callbacks
import app.modules.m4_supply_chain.callbacks
import app.modules.m5_workforce_pmo.callbacks
import app.modules.m6_smart_factory.callbacks
import app.modules.m7_process_quality.callbacks # <-- NUEVO
# --- PUNTO DE ENTRADA ---
if __name__ == '__main__':
    # Inicia el servidor en el puerto configurado
    server_app.run(
        host=settings.HOST, 
        port=settings.PORT, 
        debug=settings.DEBUG
    )