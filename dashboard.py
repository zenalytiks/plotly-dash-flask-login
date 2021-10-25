import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output, State
from flask_login import login_user, LoginManager, UserMixin, logout_user, current_user
import secrets
from app import (
    app,
    server
)
from pages import (
    main,
    login,
    logout
)
import callbacks

app.title = "PAWC Dashboard"

df_users = pd.read_excel('users.xlsx')



server.config.update(SECRET_KEY=secrets.token_hex(24))


login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/pages/login'

class User(UserMixin):
    def __init__(self, username):
        self.id = username


@ login_manager.user_loader
def load_user(username):
    ''' This function loads the user by user id. Typically this looks up the user from a user database.
        We won't be registering or looking up users in this example, since we'll just login using LDAP server.
        So we'll simply return a User object with the passed in username.
    '''
    return User(username)




app.layout = html.Div(
                     [
                      dcc.Location(id="url", refresh=True),
                      dcc.Location(id='redirect', refresh=True),
                      dcc.Store(id='login-status', storage_type='session'),
                      dcc.Store(id='user-authority', storage_type='session'),
                      html.Div(id="page-content")
                     ]
)



@app.callback([Output('url', 'pathname'),Output('alert-login','is_open'),Output('user-authority','data')],
              [Input('loginButton', 'n_clicks')],
              [State('input-username', 'value'),
               State('input-password', 'value'),
               State('alert-login','is_open')])
def sucess(n_clicks, username, password,alert):
    if n_clicks:
        user_bool = username in df_users['username'].tolist()
        pass_bool = password in df_users['password'].tolist()
        if user_bool & pass_bool:
            user_df = df_users[(df_users['username'] == username) & (df_users['password'] == password)]
            user_df = user_df.reset_index()
            user_authority = user_df['authority'][0]
            if ((user_df['username'][0] == username) & (user_df['password'][0] == password)):
                user = User(username)
                login_user(user)
                return ['/pages/main', alert, user_authority]
            else:
                return ['/pages/login', not alert, None]

        else:
            return ['/pages/login', not alert, None]
    else:
        return ['/pages/login', not alert, None]



@app.callback(Output('user-status', 'children'), Output('login-status', 'data'), [Input('url', 'pathname')])
def login_status(url):
    ''' callback to display login/logout link in the header '''
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated \
            and url != '/pages/logout':
        return dcc.Link('Logout', href='/pages/logout'), current_user.get_id()
    else:
        return dcc.Link('Login', href='/pages/login'), 'loggedout'


# Update page
@app.callback(Output("page-content", "children"),Output('redirect', 'pathname'),
             [Input("url", "pathname")])
def display_page(pathname):
    view = None
    url = dash.no_update
    if pathname == "/pages/login":
        view = login.create_layout(app)
    elif pathname == "/pages/main":
        if current_user.is_authenticated:
            view = main.create_layout(app)
            url = "/pages/main"
        else:
            view = "Redirecting to Login..."
            url = "/pages/login"
    elif pathname == "/pages/logout":
        if current_user.is_authenticated:
            logout_user()
            view = logout.create_layout(app)
        else:
            view = login.create_layout(app)
            url = "/pages/login"
    else:
        view = login.create_layout(app)

    return view, url

if __name__ == '__main__':
    app.run_server(port=8080, debug=False)
