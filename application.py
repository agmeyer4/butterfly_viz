import dash
from dash import dcc,html,Input,Output
import builder
import boto3
import datetime
import pandas as pd
import numpy as np
import os
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
bucket = 'carbonveda-poc-test'

########### Set up the layout
app.layout = html.Div(children=[
	html.Div(
		'Butterfly Cloud Dashboard: Version 0',
		style={'color':'blue','font-size':'22px','display':'inline-block','width':'50%'}
	),
    dcc.Graph(
            id='plot1',
			style={'height':'50vh'}
        ),
    dcc.Graph(
            id='plot2',
			style={'height':'50vh'}
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
	key='spectra_11-37-08_test.txt'
	spectra = builder._s3_pd(s3,bucket,key)
	#spectra = pd.read_csv(r'C:\Users\agmey\Desktop\spectra_11-37-08_test.txt',header =None)
	spectra.set_index(0,inplace = True)
	fig = make_subplots()
	for i in range(len(spectra)):
		fig.add_trace(
				go.Scatter(x = np.arange(0,len(spectra.columns)), y = spectra.iloc[i],mode = 'lines',name = spectra.index[i]),
			)
	fig.update_layout(
		title_text="Spectra",
	)
	return fig

@app.callback(
    Output('plot2', 'figure'),
	Input('interval-component','n_intervals')
)
def update_plot1(df):
	key = 'tph_11-37-08_test.txt'
	tph = builder._s3_pd(s3,bucket,key)

	tph.rename(columns={0:'ET',1:'T',2:'P',3:'RH'},inplace = True)
	tph['DT'] = pd.to_datetime(tph['ET'],unit='s')

	
	fig = go.Figure()

	fig.add_trace(go.Scatter(
		x=tph['DT'],
		y=tph['T'],
		name="Temp",
		line_color = "#1f77b4"
	))


	fig.add_trace(go.Scatter(
		x=tph['DT'],
		y=tph['P'],
		name="Pressure",
		yaxis="y2",
		line_color = "#ff7f0e"
	))

	fig.add_trace(go.Scatter(
		x=tph['DT'],
		y=tph['RH'],
		name="RH",
		yaxis="y3",
		line_color = "#d62728"
	))

	# Create axis objects
	fig.update_layout(
		xaxis=dict(
			domain=[0.1, 1]
		),
		yaxis=dict(
			title="Temp (C)",
			titlefont=dict(
				color="#1f77b4"
			),
			tickfont=dict(
				color="#1f77b4"
			)
		),
		yaxis2=dict(
			title="Pressure",
			titlefont=dict(
				color="#ff7f0e"
			),
			tickfont=dict(
				color="#ff7f0e"
			),
			anchor="free",
			overlaying="y",
			side="left",
			position=0.05
		),
		yaxis3=dict(
			title="RH (%)",
			titlefont=dict(
				color="#d62728"
			),
			tickfont=dict(
				color="#d62728"
			),
			anchor="x",
			overlaying="y",
			side="right"
		),
	)

	# Update layout properties
	fig.update_layout(
		title_text="Temp, Pressure, RH",
		width = 1500
	)

	
	return fig
########### Run the app
if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port=8050,debug=True)
    #app.run_server(debug=True)