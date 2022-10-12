import dash
from dash import dcc,html,Input,Output
import builder
import boto3
import datetime
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
    dcc.Graph(
            id='plot2',
        ),
	dcc.Interval(id = 'interval-component',
						interval = 1*30000,#milliseconds
						n_intervals = 0
					),
])

@app.callback(
    Output('plot1', 'figure'),
	Input('interval-component','n_intervals')
)
def update_plot1(df):
	bucket='carbonveda-poc-test'
	key='spectra_11-37-08_test.txt'
	spectra = builder._s3_pd(s3,bucket,key)
	#spectra = pd.read_csv(r'C:\Users\agmey\Desktop\spectra_11-37-08_test.txt',header =None)
	spectra.set_index(0,inplace = True)
	fig = make_subplots()
	for i in range(len(spectra)):
		fig.add_trace(
				go.Scatter(x = np.arange(0,len(spectra.columns)), y = spectra.iloc[i],mode = 'lines',name = spectra.index[i]),
			)
	return fig

@app.callback(
    Output('plot2', 'figure'),
	Input('interval-component','n_intervals')
)
def update_plot1(df):
	tph = pd.read_csv('C:/Users/agmey/Desktop/tph_11-37-08.txt',delimiter=' ',header=None).iloc[5:]
	tph.rename(columns={0:'ET',1:'T',2:'P',3:'RH'},inplace = True)
	tph['DT'] = pd.to_datetime(tph['ET'],unit='s')

	fig = make_subplots(specs=[[{"secondary_y": True}]])
	fig.add_trace(
		go.Scatter(x = tph['DT'], y = tph['T']),
		secondary_y = False
	)
	fig.add_trace(
		go.Scatter(x = tph['DT'], y = tph['P']),
		secondary_y=True
	)
	return fig
########### Run the app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=80,debug=True)
    #app.run_server(debug=True)