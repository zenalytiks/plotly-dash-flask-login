import dash
from flask import Flask
import dash_bootstrap_components as dbc


server = Flask(__name__)

app = dash.Dash(
    __name__,server=server,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP]
)
