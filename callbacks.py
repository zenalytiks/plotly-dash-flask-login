from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
import numpy as np
from datetime import datetime
import dash
from app import app
import plotly.graph_objects as go


def get_machines(df):
    machines = []
    for i in df['Machine'].unique():
        machines.append(i)
    return [{'label':i,'value':i} for i in machines]

def get_dates(df):

    dt_all = pd.date_range(start=df['Reading_date'].iloc[0],end=df['Reading_date'].iloc[-1])

# retrieve the dates that ARE in the original datset
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df['Reading_date'])]

# define dates with missing values
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]

    df['Reading_date'] = df['Reading_date'].astype(str)


    df["Reading_date"] = pd.to_datetime(df["Reading_date"]).dt.strftime('%m/%d/%Y')
    df['Reading_date'] = pd.to_datetime(df['Reading_date'])

    min1 = min(df['Reading_date'].astype(str))
    max1 = max(df['Reading_date'].astype(str))

    min_Reading_date = min1.replace("-",",")
    max_Reading_date = max1.replace("-",",")

    min_y = int(min_Reading_date[:4])
    min_m = int(min_Reading_date[5:7])
    min_d = int(min_Reading_date[8:10])

    max_y = int(max_Reading_date[:4])
    max_m = int(max_Reading_date[5:7])
    max_d = int(max_Reading_date[8:10])




    return min_y,min_m,min_d,max_y,max_m,max_d,dt_breaks


df = pd.read_excel('pawc_data.xlsx')


@app.callback(
        Output("machine-dropdown","options"),
        [Input("location-dropdown","value")]
)

def update_dropdown(location):
    df_filtered = df[df['Location'] == location]
    return get_machines(df_filtered)

@app.callback(
        [Output("date-picker","min_date_allowed"),
        Output("date-picker","max_date_allowed"),
        Output("date-picker","disabled_days")],
        [Input("location-dropdown","value"),
        Input("machine-dropdown","value")]
)

def update_calendar(location,machine):
    df_filtered = df[(df['Location'] == location) & (df['Machine'] == machine)]
    min_y,min_m,min_d,max_y,max_m,max_d,dt_breaks = get_dates(df_filtered)
    min_date = datetime(min_y,min_m,min_d)
    max_date = datetime(max_y,max_m,max_d)
    return [min_date,max_date,dt_breaks]




@app.callback(
        [Output("table","data"),
         Output("table","columns"),
         Output("graph","figure"),
         Output("table-col","style"),
         Output("graph-col","style"),
         Output("alert-main","is_open")
         ],
        [Input("submit-btn","n_clicks")
        ],
        [State("location-dropdown","value"),
         State("machine-dropdown","value"),
         State("date-picker","date"),
         State("table-col","style"),
         State("graph-col","style"),
         State("alert-main","is_open")
         ]
)

def update_dashboard(btn,location_value,machine_value,date_value,table_col_style,graph_col_style,alert):
     button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
     if button_id == "submit-btn":
        date_value = date_value+"T00:00:00"
        df_filtered = df[(df['Location'] == location_value) & (df['Machine'] == machine_value) & (df['Reading_date'] == date_value)]

        if df_filtered.to_dict('records'):
            data_table=df_filtered.loc[:,["Installation_date","Reading_date","Po_code","Average","Low_reading","High_reading"]]

            data_table["Reading_date"] = pd.to_datetime(data_table["Reading_date"]).dt.strftime('%m/%d/%Y')
            data_table["Installation_date"] = pd.to_datetime(data_table["Installation_date"]).dt.strftime('%m/%d/%Y')

            columns=[{"name": i, "id": i} for i in data_table.columns]
            data=data_table.to_dict('records')


            fig = go.Figure()

            fig.add_trace(go.Scatter(x=df_filtered['Anvil_Nr'],
                                     y=df_filtered['Average'],
                                     mode='markers',
                                     marker=dict(
                                         size=14,
                                     ),
                                     name="Average")
            )
            fig.add_trace(go.Scatter(x=df_filtered['Anvil_Nr'],
                                     y=df_filtered['Low_reading'],
                                     mode='markers',
                                     marker=dict(
                                         size=14,
                                     ),
                                     name="Low Reading")
            )
            fig.add_trace(go.Scatter(x=df_filtered['Anvil_Nr'],
                                     y=df_filtered['High_reading'],
                                     mode='markers',
                                     marker=dict(
                                        size=14,
                                     ),

                                     name="High Reading")
            )

            fig.update_layout(
                    paper_bgcolor='#252e3f',
                    plot_bgcolor='#1f2630',
                    font=dict(color='#7fafdf'),
                    margin=dict(
                             l=50,
                             r=0,
                             b=0,
                             t=50,
                    ),
                    xaxis=dict(
                            title="Anvil_Nr",
                    ),
                    yaxis=dict(
                            title="Readings",
                    )
            )

            fig.update_xaxes(showgrid=False,color="#7fafdf")
            fig.update_yaxes(showgrid=False,color="#7fafdf")

            table_col_style = {'visibility':'visible','height':'500px','overflow':'scroll','overflow-x':'hidden'}
            graph_col_style = {'visibility':'visible'}

            return [data,columns,fig,table_col_style,graph_col_style,alert]

        else:
            table_col_style = {'visibility':'hidden','height':'500px','overflow':'scroll','overflow-x':'hidden'}
            graph_col_style = {'visibility':'hidden'}
            return [[],[],{},table_col_style,graph_col_style,not alert]
