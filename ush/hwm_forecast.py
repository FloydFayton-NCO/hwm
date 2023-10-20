"""hwm_forecast.py: predictive json files for HWM charts"""
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
import re
from datetime import datetime, timedelta, date
import os
import numpy as np
import pandas as pd

def hwm_modify(jsonfile,ctrl):
    with open(ctrl,'r') as cfile:
        jsonctrl = pd.read_csv(cfile,sep=" ",comment="#",header=None,skip_blank_lines=True,names=['sign','model','number','times'])
        jsonctrl = jsonctrl.fillna("0") # no NaNs or empty fields, last two fields in control have to be integers

    with open(jsonfile,'r') as jfile:
        data = json.load(jfile)
        data_str = re.sub(r'[\[\]]', '', str(data)) #super step for searching, object --> string

    #Create new models
    for idx, cow in jsonctrl.iterrows():
        sign=cow['sign']
        model=cow['model']
        modelfound=re.findall("\'"+model+"\'", data_str)
        number=int(cow['number'])
        times=cow['times'] #not integrated yet

        if not modelfound:
            xbegin=data[0][:][0]['data'][0][0]
            modelDat=[]
            for i in range(0,1439):
                modelDat.append([xbegin,0])
                xbegin+= 60000
            newmodel = json.dumps([{"name":model,"data":modelDat}],indent=4,sort_keys=False)
            poo=json.loads(newmodel)
            data.append(poo)

        #reset vars with updated data
        data_str = re.sub(r'[\[\]]', '', str(data)) 
        modelfound=re.findall("\'"+model+"\'", data_str)

        # if modelfound:
        #     print(model)

        for row in data:
            # modelfound=re.fullmatch(model, row[0]['name'])
            if modelfound:
                for i in range(0,1439):
                    x1=row[0]['data'][:][i][-1]
                    x2=number
                    # if sign == '*': # sign * 0 (number) == 0
                    #     nuvalue=max(0,int(x1*x2))
                    #     row[0]['data'][:][i][-1]=nuvalue
                    # elif sign == '-': # double meaning if number is 0 or empty, should both result in zero? FAFJ
                    #     if number == 0:
                    #         x1=0
                    #         continue
                    #     else:
                    #         nuvalue=max(0,int(x1-x2))
                    #         row[0]['data'][:][i][-1]=nuvalue
                    # elif sign == '/':
                    #     nuvalue=max(0,int(x1/x2))
                    #     row[0]['data'][:][i][-1]=nuvalue
                    # elif sign == '+':
                    #     nuvalue=max(0,int(x1+x2))
                    #     row[0]['data'][:][i][-1]=nuvalue
                    # else:
                    #     print('operand not detected, please fix $PARMhwm/fcst_ctrl file')
                    #     continue
                    # result=row[0]['data'][:][i][-1]
                    # print(x1," ",sign," ",x2,"=",result,"\n") # math test FAFJ

    with open('new.json','w') as final:
        final.write(json.dumps(data,indent=4,sort_keys=False))

ctrlfile = 'parm/fcst_ctrl'
infile = 'cactus_daily_nid_nodes_p1.json'

# ctrl = sys.argv[2]
# infile = sys.argv[1]
# fcst_ctrl = os.environ["FCST_CTRL"]
# workdir = os.environ["DATA"] + '/'

hwm_modify(infile,ctrlfile)



