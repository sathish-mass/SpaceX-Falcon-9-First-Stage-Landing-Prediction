# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                ],
                                                value='ALL',
                                                placeholder="place select here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                #marks={0: '0',
                                                 #   100: '1000'},
                                                value=[0, 1000]),
                                
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Outcome For All Launch Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(values=(spacex_df[spacex_df['Launch Site']==entered_site]['class'].value_counts().to_list()),names=spacex_df[spacex_df['Launch Site']==entered_site]['class'].value_counts().index.to_list(),title='Outcome For Launch site {}'.format(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site,payload_slide):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fill_df=spacex_df[(spacex_df['Payload Mass (kg)']>payload_slide[0]) & (spacex_df['Payload Mass (kg)']<payload_slide[1])]
        fig1 = px.scatter(fill_df, y='class', 
        x='Payload Mass (kg)',color='Booster Version',
        title='Correlation between payload and All Launch Sites')
        return fig1
    else:
        # return the outcomes piechart for a selected site
        fill_df=spacex_df[(spacex_df['Launch Site']==entered_site) & (spacex_df['Payload Mass (kg)']>payload_slide[0]) & (spacex_df['Payload Mass (kg)']<payload_slide[1])]
        fig1 = px.scatter(fill_df, y='class', 
        x='Payload Mass (kg)',color='Booster Version',
        title='Correlation between payload and Launch Site {}'.format(entered_site))
        return fig1
# Run the app
if __name__ == '__main__':
    app.run_server()
