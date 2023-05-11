from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

df = pd.read_csv('GBD_2019_data.csv')
df = df[df['metric_name'] == 'Rate']
df = df.sort_values(by='age_name')

location_names = ['United States of America', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Washington DC', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming', 'Canada']

cause_names = np.sort(df['cause_name'].unique())

app = Dash(__name__)

sidebar = html.Aside([
    html.H2('Options'),
    html.Div([
        html.P('Location'),
        dcc.Dropdown(options=location_names, value=location_names[0], id='loc-select', clearable=False),
    ]),
    html.Div([
        html.P('Cause'),
        dcc.Dropdown(options=cause_names, value=cause_names[0], id='cause-select', clearable=False),
    ])
])

content = html.Main([
    html.H1(children='Prevalence of STIs in Males by Age Group'),
    dcc.Graph(id='graph-content'),
    dcc.Markdown('2019 data from the [IHME Global Burden of Disease](https://www.healthdata.org/gbd) survey.\n\nPrevalence is the total number of cases of a given disease in a specified population at a designated time. It is differentiated from *incidence*, which refers to the number of new cases in the population at a given time.')
])

app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar,
    content,
])

@callback(
    Output('graph-content', 'figure'),
    Input('loc-select', 'value'),
    Input('cause-select', 'value')
)
def update_graph(location, cause):
    dff = df[(df['location_name'] == location) & (df['cause_name'] == cause)]
    return px.bar(dff, x='age_name', y='val', labels={'age_name': 'Age Group', 'val': 'Prevalence (per 100k)'})

app.run_server()
