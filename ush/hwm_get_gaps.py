#!/usr/bin/env python
"""hwm_get_gap.py: compute the time of the earliest gap in the input time window for seamless backfill of the HWM LIVE and DAILY charts"""
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
import re

#directory for initialized json files
jsond = os.environ["DATA"]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Set PDY
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#start and end time of the catchup run, and timestamp for the running jobs, and whether the run is to count nodes or cores
spdyhhmm=sys.argv[1];epdyhhmm=sys.argv[2];proj_total=int(sys.argv[3]);countres=sys.argv[4]

#break calender time up for epoch time calculation
epyr=epdyhhmm[0:4];epmt=epdyhhmm[4:6];epda=epdyhhmm[6:8];ephr=epdyhhmm[8:10];epmn=epdyhhmm[10:12]
spyr=spdyhhmm[0:4];spmt=spdyhhmm[4:6];spda=spdyhhmm[6:8];sphr=spdyhhmm[8:10];spmn=spdyhhmm[10:12]

#end time epoch calculation
ed=datetime(int(epyr),int(epmt),int(epda),int(ephr),int(epmn))
eepoch_pdyhhmm=int(time.mktime(ed.timetuple()))

#start time epoch calculation
sd=datetime(int(spyr),int(spmt),int(spda),int(sphr),int(spmn))
sepoch_pdyhhmm=int(time.mktime(sd.timetuple()))

epoch_end=eepoch_pdyhhmm*1000
epoch_start=sepoch_pdyhhmm*1000

with open("wcossii_projects") as file:
    project_list = file.readlines()
    project_list = [line.rstrip() for line in project_list]

timesteps=int((epoch_end-epoch_start)/60000)

timei=epoch_start
for i in range(0,timesteps):

#to determine search file directory, returns a PDY
    timei_cal = datetime.fromtimestamp(timei/1000).strftime('%Y%m%d')

    dir_contents = os.listdir(jsond+'/'+timei_cal+'/jsonfiles_'+countres+'/')
    if dir_contents:
        count=0
        for i in project_list:
            filename="%s.json" %(i)
            with open(jsond+'/'+timei_cal+'/jsonfiles_'+countres+'/'+filename, 'r') as f:
                json_data = json.load(f)
                arr=json_data[0]['data']
                for i in arr:
                    if i[0] == timei:
                        if i[1] == 0:
                            count+=1
#                            print(count,'for filename= ',filename)

#        print('total count= ', count,'for timei= ', timei)
        if count == proj_total:
            final_time = datetime.fromtimestamp(timei/1000).strftime('%Y%m%d%H%M')
            print(final_time)
            exit()

    else:
            print('No Json files in the current search directory. Exiting!!!!!!!!!')
            exit()

    timei+= 60000
