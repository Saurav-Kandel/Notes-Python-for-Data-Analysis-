import dash
from dash.dependencies import Input, Output
from dash import html
import dash_pivottable

from Data import data

app = dash.Dash(__name__)
app.title = 'Bike Sharing DataSet'

app.layout = html.Div([
    dash_pivottable.PivotTable(
        id='table',
        data=data,
        cols=['season'],
        colOrder="key_a_to_z",
        rows=['mnth'],
        rowOrder="key_a_to_z",
        rendererName="Grouped Column Chart",
        aggregatorName="Average",
        vals=["cnt"]
        # valueFilter={'Day of Week': {'Thursday': False}}
    ),
    html.Div(
        id='output'
    )
])


@app.callback(Output('output', 'children'),
              [Input('table', 'cols'),
               Input('table', 'rows'),
               Input('table', 'rowOrder'),
               Input('table', 'colOrder'),
               Input('table', 'aggregatorName'),
               Input('table', 'rendererName')])
def display_props(cols, rows, row_order, col_order, aggregator, renderer):
    return [
        html.P(str(cols), id='columns'),
        html.P(str(rows), id='rows'),
        html.P(str(row_order), id='row_order'),
        html.P(str(col_order), id='col_order'),
        html.P(str(aggregator), id='aggregator'),
        html.P(str(renderer), id='renderer'),
    ]


if __name__ == '__main__':
    app.run_server(debug=True)