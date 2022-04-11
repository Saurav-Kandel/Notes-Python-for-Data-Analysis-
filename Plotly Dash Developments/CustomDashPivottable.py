from pickle import TRUE
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import numpy as np


# Reading the dataset into a DataFrame.
data = pd.read_csv('hour.csv')

layoutStyles = {
    'font' : 'verdana'
}

app = Dash(__name__)
app.title = 'Rex Dash board' # Title / Name of the Dashboard to be displayed in the Tab bar of Browser

#
# | | |  OVERALL LAYOUTS  | | |
# V V V                   V V V
#

app.layout = html.Div(children=[

    # DIV for the Main title in the dashboard
    html.Div(children=[
        html.H1('Custom Dash PivotTable ', style={'textAlign': 'center', 'border-bottom-style': 'solid', 'border-color': 'red', 'background-color':'#9aa1a0'})
        ]),


    # DIV for the Drop Down menu of Chart Type, Content Type and Content Column; and Radio Button to show or hide table
    html.Div(children=[

        html.Div(children=[
            html.Label('Chart Type', style={'font-family':layoutStyles['font']}),
            dcc.Dropdown(['Bar Chart', 'Scatter Chart','Area Chart' , 'Line Chart'],\
                'Bar Chart', id='chartType')
        ], style={'width': '30%', 'margin-top': 0}),

        html.Div([
            dcc.RadioItems(['Show Table', 'Hide Table'], 'Hide Table', inline=True, id='radioButton-1')
        ],style={'margin-left':'18%', 'margin-top':10}),

        html.Div(children=[
            html.Label('Content Type', style={'font-family':layoutStyles['font']}),
            dcc.Dropdown(['Size / Count', 'Mean', 'Sum', 'Median', 'Var (Variance)', 'Std (Standard Deviation)'], 'Mean', style={'width': '40%', 'margin-top': 10}, id='contentType'),
            dcc.Dropdown(data.columns, 'cnt', style={'margin-top': 10, 'margin-left': 20, 'margin-bottom': 10, 'width': '36.5%'}, id='contentColumn', disabled=False),
        ], style={'margin-top': 20, 'margin-left': 20}),
    
    ]),


    # Div for Drop Down menu to Select the Hue
    html.Div([
        html.H3('Select the Hue: ', style={'margin-left':65}),
        dcc.Dropdown(data.columns, 'mnth', style={'margin-top':5, 'width': '50%'}, id='y')
    ], style={'display': 'flex', 'float':'right', 'width':'25%'}),


    # Div for the Title of the Dataset used in the dashboard.
    html.Div([html.H2('Bike Sharing Data Set')], style={'text-align':'center', 'background-color':'white', 'margin-top':70}),
    

    # Div to hold and display the plot/ Graph 
    html.Div([
    dcc.Graph(
        id='graph-1',
        figure= {}
    )
    ],id='Graph_Div', style={}),


    # Div to hold and display the DataTable for the plot
    html.Div([
    dash_table.DataTable(
        id='table',

        style_data={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
        'color': 'black',
        'backgroundColor': 'white',
        'fontSize' : 15
        },

        style_data_conditional=[
        {
            'if': {'row_index': 'even'},
            'backgroundColor': 'rgb(220, 220, 220)',
        }],

        style_cell={'textAlign': 'right', 'border': '1px solid grey'},

        style_header={'border': '1px solid black', 'fontWeight': 'bold', 'fontSize': 18},
    
    )
    
    ],id='Table_Div', style={}),


    # Div for Drop Down menu to Select the X-Coordinate
    html.Div([
        html.H3('Select the X-coordinate: '),
        dcc.Dropdown(data.columns, 'season', style={'flex':0.25, 'margin-top':5}, id='x')
    ], style={'display': 'flex', 'margin-left':550}),


    # Div to Display the Notice on the Dataset being Used
    html.Div([
        html.P('READ ME !', style={'font-family':layoutStyles['font'], 'text-align':'left', 'background-color':'white'}),
        html.P('This is a Bike sharing data set (Hour.csv)')

    ], style={'font-family':'calibri (Body)'}),

    html.Br(),
    html.Br()
], style={'border-style': 'solid', 'border-color': 'black', 'background-color':'#42f5e3'})



#
# | | |   CALL BACK FUNCTIONS   | | |
# V V V                         V V V
#


# Hides/ Unhides the Table as selected in the radio button.
@app.callback(Output('Table_Div', 'style'),
    Input('radioButton-1', 'value'))
def HideDiv(selected_item):
    if selected_item != 'Show Table':
        return {'display': 'none'}


# Hiding the content Column Dropdown Menu when 'Count' is selected on content Type.
@app.callback(Output('contentColumn', 'style'),
    Input('contentType', 'value'))
def hideContentColumn(contentType):
    if contentType == 'Size / Count':
        return {'display':'none'}
    else:
        return {'margin-top': 10, 'margin-left': 20, 'margin-bottom': 10, 'width': '36.5%'}


# Updating dropdown menu of Hue
@app.callback(Output('y', 'options'),
    Input('x', 'value'))
def update_dropdown(selected_item):
    df = data.drop(labels=selected_item, axis=1)
    newDF = df.columns
    return newDF


# Updating dropdown menu of X coordinate
@app.callback(Output('x', 'options'),
    Input('y', 'value'))
def update_dropdown(selected_item):
    df = data.drop(labels=selected_item, axis=1)
    newDF = df.columns
    return newDF
    
# Updates the entire plot/ Graph according to the items selected in drop down menus
@app.callback(Output('graph-1', 'figure'),
    Input('chartType', 'value'),
    Input('contentType', 'value'),
    Input('contentColumn', 'value'),
    Input('x', 'value'),
    Input('y', 'value'))
def PlotUpdate(chartType, contentType, contentColumn, x, y):
    sep = ' '
    chartType = chartType.lower().split(sep, 1)[0]
    contentType = contentType.lower().split(sep, 1)[0] + '()'

    if contentType == 'size()':
        dfExpression = "data.groupby([x, y]).size().reset_index().rename(columns={0:'count'})"
        df2 = eval(dfExpression)
        contentColumn = 'count'
    else:
        dfExpression = f"data.groupby([x, y]).{contentType}.reset_index()"
        df2 = eval(dfExpression)

    plotExpression = f"px.{chartType}(df2, x=x, y=contentColumn, color=y)"
    plot = eval(plotExpression)
    
    return plot

# Generates Tabular data of the plot.
@app.callback(Output('table', 'data'),
    Input('contentType', 'value'),
    Input('contentColumn', 'value'),
    Input('x', 'value'),
    Input('y', 'value'))
def TableUpdate(contentType, contentColumn, x, y):
    sep = ' '
    contentType = contentType.lower().split(sep, 1)[0]
    tableExpression = f"pd.pivot_table(data, values=contentColumn, index=[x], columns=[y], aggfunc=np.{contentType}, fill_value='')"
    table = eval(tableExpression)

    dictdata = table.reset_index().to_dict('records')
    return dictdata


if __name__ == '__main__':
    app.run_server(debug=True)