from dash import dcc
from dash import html

def create_layout(app):
    return html.Div([html.Div(html.H2('You have been logged out - Please login')),
                       html.Br(),
                       dcc.Link('Home', href='/pages/login')
                       ])
