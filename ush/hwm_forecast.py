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

def err_exit(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

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
        times=cow['times']
        tarr=[] #time array not integrated yet

        # #work in progress##########################
        if times != "0":
            split=times.split(sep=",",maxsplit=-1)
            for idx,ranget in enumerate(split):
                ranget=ranget.split(sep="-")
                print(ranget[0])
                tarr.append(ranget)
                print(idx)
                print(tarr[idx][0])
        # # work in progress##########################


        if not modelfound:
            xbegin=data[0][:][0]['data'][0][0]
            modelDat=[]
            for i in range(0,1439):
                modelDat.append([xbegin,0])
                xbegin+= 60000
            newmodel = json.dumps([{"name":model,"data":modelDat}],indent=4,sort_keys=False)
            poo=json.loads(newmodel)
            data.append(poo)
            data_str = re.sub(r'[\[\]]', '', str(data)) #reset vars with updated data
            modelfound=re.findall("\'"+model+"\'", data_str)

        for row in data:
            mfound=re.fullmatch(model, row[0]['name'])
            if mfound:
                for i in range(0,1439):
                    x1=row[0]['data'][:][i][-1]
                    if sign == '*': # sign * 0 (number) == 0
                        nuvalue=max(0,int(x1*number))
                        row[0]['data'][:][i][-1]=nuvalue
                    elif sign == '-': # double meaning if number is 0 or empty, should both result in zero? FAFJ
                        if number == 0:
                            row[0]['data'][:][i][-1]=0 # sets value to zero since x1-0 makes no sense
                        else:
                            nuvalue=max(0,int(x1-number))
                            row[0]['data'][:][i][-1]=nuvalue
                    elif sign == '/':
                        nuvalue=max(0,int(x1/number))
                        row[0]['data'][:][i][-1]=nuvalue
                    elif sign == '+':
                        nuvalue=max(0,int(x1+number))
                        row[0]['data'][:][i][-1]=nuvalue
                    else:
                        err_exit('operand not detected, please fix $PARMhwm/fcst_ctrl file')
                    # result=row[0]['data'][:][i][-1] # Debug math
                    # print(model,result)
                    # print(x1," ",sign," ",number,"=",result,"\n") # math test FAFJ

    with open('hwm_fcst_nid_nodes_p1.json','w') as final:
        final.write(json.dumps(data,indent=4,sort_keys=False))

################ TESTING INPUTS ################
ctrlfile = 'parm/fcst_ctrl'
infile = 'cactus_daily_nid_nodes_p1.json'
################################################

################ PRODUCTION INPUTS #############
# infile = os.environ["IJSON"]
# ctrlfile = os.environ["FCST_CTRL"]
# workdir = os.environ["DATA"] + '/'
################################################
hwm_modify(infile,ctrlfile)



