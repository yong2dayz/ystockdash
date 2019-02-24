import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.offline as pyo
import plotly.graph_objs as go

from dash.dependencies import Input, Output, State
import pandas as pd
import  os, sys
from pandas_datareader import data as web
import requests
from datetime import datetime as dt



app = dash.Dash()
server = app.server
nsdq = pd.read_csv('data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label': '{} {}'.format(tic, nsdq.loc[tic]['Name']), 'value':tic})

app.layout = html.Div([
    html.H1('Yong Stock Dashboard'),
    html.Div([
        html.H3('Select stock symbols:', style={'paddingRight':'30px'}),
        dcc.Dropdown(
            id='my_stock',
            options=options,
            value=['TSLA'],
            multi=True
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}),
     html.Div([
        html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id='datepicker',
            min_date_allowed=dt(2015, 1, 1),
            max_date_allowed=dt.today(),
            start_date= dt(2018,1,1),
            end_date=dt.today()
        )

     ], style={'display': 'inline-block', 'marginLeft':'30px'}),
    html.Div([
        html.Button(id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontsize': 36, 'marginLeft': '30px'}
            ),
            ], style={'display':'inline-block'}),
    dcc.Graph(
        id='stock-graph',
        figure={'data':[{'x': [1,2], 'y': [3,1]}],
        'layout': go.Layout({'title':'Stocks'},
        xaxis={'title':'Date'},
        yaxis={'title': 'Closing Prices'},
        hovermode='closest')
        }
    )

    ])

@app.callback(Output('stock-graph', 'figure'),
                [Input('submit-button', 'n_clicks')],
                [State('my_stock', 'value'),
                State('datepicker', 'start_date'),
                State('datepicker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = dt.strptime(start_date[:10], '%Y-%m-%d')
    end = dt.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, 'iex', start, end)
        traces.append({'x': df.index, 'y': df['close'], 'name':tic})
    fig = {
        'data':traces,
        'layout': go.Layout(
            {'title': ', '.join(stock_ticker) + ' Closing Prices'},
            xaxis={'title':'Date'},
            yaxis={'title': 'Closing Prices'},
            hovermode='closest')
            }
    return fig

if __name__ == '__main__':
    app.run_server()
