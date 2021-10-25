import dash_bootstrap_components as dbc
from dash import dcc
from dash import html


def create_layout(app):
    return dbc.Container([
    dbc.Alert(
           "Please enter correct Login Credentials!",
           id="alert-login",
           is_open=True,
           duration=4000,
           color="danger"
    ),
    html.Br(),
    dbc.Row([
    dbc.Col([

                dbc.Row(
                        [
                        html.Img(
                            src='/assets/policart_logo.png',
                            className='center',
                            style={'height':'40%', 'width':'40%'}
                        )

                        ],justify="center"
                ),

                dbc.Row(
                        [
                        dbc.Col(
                                [
                                dbc.InputGroup(
                                    [
                                        dbc.Input(id="input-username",placeholder="Username", type="text")

                                    ]
                                )
                                ],width=6
                        )


                        ],style={'padding':'10px'},justify="center"
                ),
                dbc.Row(
                        [
                        dbc.Col(
                                [
                                dbc.InputGroup(
                                    [
                                        dbc.Input(id="input-password",placeholder="Password", type="password")

                                    ]
                                )

                                ],width=6
                        )
                        ],style={'padding':'10px'},justify="center"
                ),
                dbc.Row(
                        [
                        html.Button(
                            children='Login',
                            n_clicks=0,
                            id='loginButton',
                            className='btn btn-primary btn-lg'
                        )

                        ],style={'padding':'10px'},justify="center"
                )
                ],width=6)
    ],justify="center", className='jumbotron',style={'background-color':'#252e3f'})
])
