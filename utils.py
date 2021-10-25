import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.NavbarSimple(
    [
        dbc.Row(
                [
                dbc.Col(html.Img(src="/assets/policart_logo.png", height="40px"),style={'position':'absolute','left':'150px'}),
                dbc.Col(dbc.NavItem(dbc.NavLink(id='user-status')))
                ]
        )


    ],
    color="#252e3f",
    dark=True,
)
