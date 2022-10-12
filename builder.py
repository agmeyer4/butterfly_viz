# butterfly_viz/builder.py
# Created by: Aaron G. Meyer
# 
# Functions required for downloading data from S3 and use with application.py dashboard for visualizing butterfly data in real time. 

#Imports
import boto3
import pandas as pd
import os
import numpy as np
import io

def _s3_pd(s3_client,bucket,key):
	s3_client.download_file(bucket, key, 'temp.txt')
	data = pd.read_csv('temp.txt',header = None)
	return data
		
def main():
	s3 = boto3.client('s3')
	bucket='carbonveda-poc-test'
	key='spectra_11-37-08_test.txt'
	data = _s3_pd(s3,bucket,key)
	print(data)
if __name__ == "__main__":
	main()