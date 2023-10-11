#!/usr/bin/env python
"""initialize.py: initialize json files for HWM DAILY and LIVE charts"""
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
__author__ = 'Gregory Mott'
__credits__ = ["Gregory Mott"]
__version__ = "1.0.0"
__maintainer__ = "Gregory Mott"
__email__ = "Gregory.Mott@noaa.gov"
__status__ = "production"
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import json as json
import time
from datetime import datetime, timedelta, date
import os

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Set PDY
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pdy=sys.argv[1]; rescount=sys.argv[2] 

pyr=pdy[0:4];pmt=pdy[4:6];pda=pdy[6:8]

d=datetime(int(pyr),int(pmt),int(pda),00,00)
epoch_pdy=int(time.mktime(d.timetuple()))

#directory to put initialized json files
jsond = os.environ["DATA"] + '/' + pdy + '/jsonfiles_'+rescount+'/'

epoch_now=(epoch_pdy*1000)

with open("wcossii_projects") as file:
    project_list = file.readlines()
    project_list = [line.rstrip() for line in project_list]

xBegin=epoch_now
modelDat=[]
for i in range(0,1440):
    modelDat.append([xBegin,0])
    xBegin+= 60000

for i in project_list:
    filename="%s.json" %(i)
    with open(jsond+filename, 'w') as json_file:
        data = json.dumps([{"name":i,"data":modelDat}],indent=4,sort_keys=False)
        json_file.write(data)
