import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
from app import app
from datetime import date
from utils import navbar
import pandas as pd


df = pd.read_excel('pawc_data.xlsx')

locations = []
for i in df['Location'].unique():
    locations.append(i)
location_options = [{'label':i,'value':i} for i in locations]


def create_layout(app):
    return dbc.Container(
                         [
                         navbar,
                         dbc.Alert(
                                "No data available for entered parameters!",
                                id="alert-main",
                                is_open=True,
                                duration=4000,
                                color="danger"
                         ),
                         dcc.Store(id='data-accessable', storage_type='session'),
                         dbc.Row(
                                 [
                                 dbc.Col(
                                         [
                                         dbc.Label("Select Location:"),
                                         dcc.Dropdown(id='location-dropdown',options=location_options),
                                         dbc.Label("Select Machine:"),
                                         dcc.Dropdown(id='machine-dropdown'),
                                         ],md=6
                                 ),
                                 dbc.Col(
                                         [
                                         dcc.DatePickerSingle(id='date-picker',style={'margin-top':'30px'}),
                                         ],md=2
                                 ),
                                 dbc.Col(
                                         [
                                         dbc.Button(id="submit-btn", n_clicks=0,children="Submit", color="primary", className="mr-1",style={'margin-top':'30px'}),
                                         ],md=4
                                 )
                                 ],style={'padding':'25px'}
                         ),
                         dbc.Row(
                                 [
                                 dbc.Col(id="graph-col",
                                         children=[
                                         dcc.Graph(id='graph')

                                         ],style={'visibility':'hidden','margin-bottom':'20px'},md=6
                                 ),
                                 dbc.Col(id = "table-col",
                                         children=[
                                         dash_table.DataTable(
                                                id='table',
                                                style_data_conditional=[
                                                               {
                                                                   'if': {'row_index': 'odd'},
                                                                   'backgroundColor': '#3a4252'
                                                               }
                                                ],

                                                style_header={
                                                          'backgroundColor': '#252E3F',
                                                           'fontWeight': 'bold',
                                                           'fontSize': 20
                                                },
                                                style_cell={'font-family':'BrandonGrotesqueRegular','fontSize':16,'background-color':'#505765'}

                                                )
                                         ],style={'visibility':'hidden','margin-top':'20px'},md=6

                                 )
                                 ],style={'padding':'25px'}
                         )

                         ],fluid=True,style={'padding-left':0,'padding-right':0}
        )
