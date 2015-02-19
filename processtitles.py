#!/usr/bin/python

import pandas as pd
import numpy as np
import time, datetime

# script to load data as raw csv, and add columns to data frame

infilename = "Homebrewing_titles_1214239837_1424289414.csv"
columns = ['row_id', 'post_id', 'score', 'time','title']
# row is an integer
# post_id is a alphanumeric integer. 
# score is an integer
# time is a POSIX timestamp, in decimal
# Word is a string consisting of a single word or symbol

frame = pd.read_csv(infilename, names=columns, sep='\t', header=1)

dayofweek = [datetime.datetime.fromtimestamp(x).isocalendar()[2] for x in frame['time']]
isoweek = [datetime.datetime.fromtimestamp(x).isocalendar()[1] for x in frame['time']]
dayofyear = [datetime.datetime.fromtimestamp(x).utctimetuple().tm_yday for x in frame['time']]
month = [datetime.datetime.fromtimestamp(x).utctimetuple().tm_mon for x in frame['time']]
year = [datetime.datetime.fromtimestamp(x).utctimetuple().tm_year for x in frame['time']]

frame['dayofweek'] = dayofweek
frame['isoweek'] = isoweek
frame['dayofyear'] = dayofyear
frame['month'] = month
frame['year'] = year

has_first = ['first' in str(x).lower() for x in frame['title']]
has_question = [('?' in str(x) or 'question' in str(x).lower()) for x in frame['title']]

frame['has_first'] = has_first
frame['has_question'] = has_question
