import json as jn
import numpy as np
import pandas as pd

with open('cactus_daily_nid_nodes_p1.json','r') as f1:
    data = jn.load(f1)

with open('parm/fcst_ctrl','r') as f2:
    jsonctrl = pd.read_csv(f2,sep=" ",comment="#",header=None,skip_blank_lines=True,names=['sign','model','number','times'])

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
                x1=i[0]['data'][:][-1][1]=0

            if sign == '*':
                #max nuvalue 0
                nuvalue=max(0,x1*x2)
                x1=nuvalue
            elif sign == '-':
                nuvalue=max(0,x1-x2)
                x1=nuvalue
                exit
            elif sign == '/':
                nuvalue=max(0,x1/x2)
                x1=nuvalue
            elif sign == '+':
                nuvalue=max(0,x1+x2)
                x1=nuvalue
            else:
                continue #print('operation not detected, please fix $PARMhwm/fcst_ctrl file')
    print(model,x1)

#newData = json.dumps(data, indent=4)
#with open('forecast_nid_nodes_p1.json', 'w') as file:
#    file.write(newData)
