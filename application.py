import dash
from dash import dcc,html,Input,Output
import builder
import boto3
import pandas as pd
import numpy as np
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
########### Initiate the app
#styling
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#declare the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

s3 = boto3.client('s3')


########### Set up the layout
app.layout = html.Div(children=[
	html.Div('App Testing'),
    dcc.Graph(
            id='plot1',
        ),
	dcc.Interval(id = 'interval-component',
						interval = 1*5000,#milliseconds
						n_intervals = 0
					),
])


@app.callback(
    Output('plot1', 'figure'),
	Input('interval-component','n_intervals')
)
def update_plot1(df):
	bucket='carbonveda-poc-test'
	key='spectra_09-28-39.txt'
	data = builder._s3_np(s3,bucket,key)

	fig = make_subplots()
	fig.add_trace(
		go.Scatter(x = np.arange(0,len(data)), y = data),
	)
	return fig
########### Run the app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=80,debug=True)
    #app.run_server(debug=True)