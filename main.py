from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv('GBD_2019_data.csv')
df = df[df['metric_name'] == 'Rate']
df = df.sort_values(by='age_name')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Prevalence of Sexually-Transmitted Infections in Males by Age Group'),
    dcc.Dropdown(options=df['location_name'].unique(), value='United States of America', id='location-selection', clearable=False),
    dcc.Dropdown(options=np.sort(df['cause_name'].unique()), value='Chlamydial infection', id='cause-selection', clearable=False),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('location-selection', 'value'),
    Input('cause-selection', 'value')
)
def update_graph(location, cause):
    dff = df[(df['location_name'] == location) & (df['cause_name'] == cause)]
    return px.bar(dff, x='age_name', y='val', barmode='group')

app.run_server()
