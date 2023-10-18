#jiif = open(iifile)
import readline
import json as j
import numpy as np
import pandas as pd

jiif = open('cactus_daily_nid_nodes_p1.json')
ljsonf = j.load(jiif)
ctrl = open('parm/fcst_ctrl','r')
#lines = jctrl.readlines()
jsonctrl = pd.read_csv(ctrl,sep=" ",comment="#",header=None,skip_blank_lines=True,names=['sign','model','number','times'])
#print(jsonctrl['model'][3])
for index, row in jsonctrl.iterrows():
    sign=row['sign']
    model=row['model']
    number=row['number']
    times=row['times']

    #addition, multiplicatio, division, or subtraction
    for i in ljsonf:
        if model in i[0]['name']:
            x1=i[0]['data'][:][:1]
            x2=number

            #del model by zero'ing value in time,value lists
            if number == 0:
                for t, v in i[0]['data']:
                    x1=0
        print(i[0]['data'][:][:1])
