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
import json as j
import time
from datetime import datetime, timedelta, date
import os
import numpy as np
import pandas as pd

# setting vars, ii is wcossii
# iifile = sys.argv[1]
# fcst_ctrl = os.environ["FCST_CTRL"]
# workdir = os.environ["DATA"] + '/'
# jiif = open(iifile,'r')

jiif = open('cactus_daily_nid_nodes_p1.json','r')
ctrl = open('parm/fcst_ctrl','r')
data = j.load(jiif)
jsonctrl = pd.read_csv(ctrl,sep=" ",comment="#",header=None,skip_blank_lines=True,names=['sign','model','number','times'])

#print(jsonctrl['model'][3])
for index, row in jsonctrl.iterrows():
    sign=row['sign']
    model=row['model']
    number=row['number']
    times=row['times']

    #addition, multiplicatio, division, or subtraction
    for i in data:
        if model in i[0]['name']:
            x1=i[0]['data'][:][-1][1]
            x2=number
            if number == 0:
                x1=0            
            # print(sign,model,number,times) #,x2,x1)
            if sign == '*':
                nuvalue=max(0,int(x1*x2))
                x1=nuvalue
            elif sign == '-':
                nuvalue=max(0,int(x1-x2))
                x1=nuvalue
            elif sign == '/':
                nuvalue=max(0,int(x1/x2))
                x1=nuvalue
            elif sign == '+':
                nuvalue=max(0,int(x1+x2))
                x1=nuvalue
            else:
                print('operand not detected, please fix $PARMhwm/fcst_ctrl file')
                continue 




