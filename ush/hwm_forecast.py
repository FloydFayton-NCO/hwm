"""hwm_forecast.py: predictive json files for HWM DAILY and LIVE charts"""
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
__author__ = 'Floyd Fayton'
__credits__ = ["Floyd Fayton"]
__version__ = "1.0.0"
__maintainer__ = "Floyd Fayton"
__email__ = "floyd.fayton@noaa.gov"
__status__ = "test"
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import readline
import sys
import json
import time
from datetime import datetime, timedelta, date
import os
import numpy as np
import pandas as pd


def test(jsonfile,ctrl):
    with open(jsonfile,'r') as file:
        data = json.load(file)

    with open(ctrl,'r') as file:
        jsonctrl = pd.read_csv(file,sep=" ",comment="#",header=None,skip_blank_lines=True,names=['sign','model','number','times'])
        jsonctrl = jsonctrl.fillna("0") # no NaNs or empty fields, last two fields in control have to be integers

    for idx, cow in jsonctrl.iterrows():
        sign=cow['sign']
        model=cow['model']
        number=int(cow['number'])
        times=cow['times']
        
        #addition, multiplicatio, division, or subtraction
        for row in data:
            if model in row[0]['name']:
                print(model)
                for i, _ in enumerate(row):
                    big=row[i]['data'][:][-1]
                    x1=row[i]['data'][:][-1][1]
                    x2=number
                    print(x1," ",sign," ",x2,"=") # math test FAFJ
                    if sign == '*': # sign * 0 (number) == 0
                        nuvalue=max(0,int(x1*x2))
                        row[i]['data'][:][-1][1]=nuvalue
                    elif sign == '-': # double meaning if number is 0 or empty, should both result in zero? FAFJ
                        if number == 0:
                            x1=0
                            continue
                        else:
                            nuvalue=max(0,int(x1-x2))
                            row[i]['data'][:][-1][1]=nuvalue
                    elif sign == '/':
                        nuvalue=max(0,int(x1/x2))
                        row[i]['data'][:][-1][1]=nuvalue
                    elif sign == '+':
                        nuvalue=max(0,int(x1+x2))
                        row[i]['data'][:][-1][1]=nuvalue
                    else:
                        print('operand not detected, please fix $PARMhwm/fcst_ctrl file')
                        continue
                    result=row[i]['data'][:][-1][1]
                    print(result,"\n") # math test FAFJ

ctrlfile = 'parm/fcst_ctrl'
infile = 'cactus_daily_nid_nodes_p1.json'

# ctrl = sys.argv[2]
# infile = sys.argv[1]
# fcst_ctrl = os.environ["FCST_CTRL"]
# workdir = os.environ["DATA"] + '/'

test(infile,ctrlfile)



