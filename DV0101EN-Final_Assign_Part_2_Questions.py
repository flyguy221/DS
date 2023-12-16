#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics Report', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'left', 'color': '#503D36', 'font-size':24}),
    # Dropdown for the report type
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'},
            ],
            value=None,
            placeholder='Select a Report Type',
            style={'width':'80%','padding':'3px','font-size':'20px','textAlign':'center'}
        )
    ], style={'width':'100%', 'padding':'10px'}),
    # Dropdown for the year
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=None,
            placeholder='Select Year',
            style={'width':'80%','padding':'3px','font-size':'20px','textAlign':'center'}
        )
    ], style={'width':'100%', 'padding':'10px'}),
    # Division for displaying graphs
    html.Div([html.Div(
        id='output-container',
        className='chart-grid',
        style={'display': 'flex', 'flexWrap':'wrap'}),
    ])    
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')])


def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
#TASK 2.5: Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        # Create Plotly Figure
        fig = go.Figure()
        #Add line plot to the figure
        fig.add_trace(
            go.Scatter(
                x=yearly_rec['Year'],
                y=yearly_rec['Automobile_Sales'],
                mode='lines+markers',
                name = 'Average Sales',
                line=dict(color='blue')
            )
        )
        # Add labels and title
        fig.update_layout(
            title='Fluctuation of Average Auto Sales During Recession'
            xaxis_title='Year',
            yaxis_title='Average Automobile Sales'
            template='plotly_white'
        )
        # Customize Grid Lines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='grey')
        # Embed Figure in dcc.Graph
        R_chart1 = dcc.Graph(figure=fig)

#Plot 2 Calculate the average number of vehicles sold by vehicle type
        # Correct typo in Small Family Car & Super Mini Car
        recession_data = recession_data['Vehicle_Type'].replace({'Smallfamiliycar':'Smallfamilycar', 'Supperminicar': 'Superminicar'}) 
        # use groupby to create relevant data for plotting
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        # Create Plotly Figure
        fig = go.Figure()
        # Add Lines for each Vehicle Type
        for Vehicle_Type in average_sales['Vehicle_Type'].unique():
            df = average_sales[average_sales['Vehicle_Type'] = Vehicle_Type]
            fig.add_trace(
                go.Scatter(
                    x = df['Year'],
                    y = df['Automobile_Sales'],
                    mode='lines+markers',
                    name=Vehicle_Type
                )
            )
        # Add labels and title
        fig.update_layout(
            title ='Average Vehicles Sold by Vehicle Type',
            xaxis_title = 'Year',
            yaxis_title = 'Average Vehicles Sold',
            xaxis = dict(
                tickmode = 'array',
                tickvals = recession_data['Year'],
                ticktext = recession_data['Year'],
                tickangle = 45),
            template = 'plotly_white'
        )
        # Customize Grid Lines
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='grey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='grey')          
        # Embed Figure in dcc.Graph                 
        R_chart2  = dcc.Graph(figure=fig)
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
                figure=px.pie(exp_rec,
                values='Advertising Expenditure',
            names='Vehicle Type',
            title="Total Expenditure Share per Vehicle Type"
            )
        )

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        unemployment_rate = recession_data.groupby


        return [
            html.Div(className='..........', children=[html.Div(children=R_chart1),html.Div(children=.....)],style={.....}),
            html.Div(className='chart-item', children=[html.Div(children=...........),html.Div(.............)],style={....})
            ]

# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots                             
    elif (input_year and selected_statistics=='...............') :
        yearly_data = data[data['Year'] == ......]
                              
#TASK 2.5: Creating Graphs Yearly data
                              
#plot 1 Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(.................))
            
# Plot 2 Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph(................)

            # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby........................
        Y_chart3 = dcc.Graph( figure.................,title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

            # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data=yearly_data.groupby(..................
        Y_chart4 = dcc.Graph(...............)

#TASK 2.6: Returning the graphs for displaying Yearly data
        return [
                html.Div(className='.........', children=[html.Div(....,html.Div(....)],style={...}),
                html.Div(className='.........', children=[html.Div(....),html.Div(....)],style={...})
                ]
        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

