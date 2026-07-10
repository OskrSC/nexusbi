from dash import html
import dash_bootstrap_components as dbc

def create_navbar():
    """
    Crea la barra de navegación superior fija.
    """
    return dbc.Navbar(
        dbc.Container(
            [
                # Logo y Nombre de la App
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Span("⬡", className="fs-3 text-primary")),
                            dbc.Col(
                                dbc.NavbarBrand("NexusBI", className="ms-2 fw-bold")
                            ),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none", "color": "inherit"},
                ),
                
                # Espacioador para empujar el contenido a la derecha
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("GitHub", href="#", external_link=True)),
                            dbc.NavItem(
                                html.Span(
                                    "v1.0 Beta", 
                                    className="badge bg-light text-dark ms-2 mt-1"
                                )
                            )
                        ],
                        className="ms-auto", # Alineación a la derecha
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    is_open=False,
                    navbar=True,
                ),
            ]
        ),
        color="dark", # Fondo oscuro profesional
        dark=True,
        className="shadow-sm p-0",
        style={"height": "60px"}
    )