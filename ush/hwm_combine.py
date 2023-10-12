#!/usr/bin/env python
"""hwm_combine.py: Combine individual json files in COMOUT to make a combined file for the LIVE and DAILY charts"""
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
import subprocess
import glob
import time
from datetime import datetime, timedelta, date
import os
import re

rescount=sys.argv[3]
jsonsearch  = os.environ["DATA"] + '/nwges_'+rescount+'0*/'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Set PDY
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
chart=sys.argv[2]

if chart == 'live':

    jsondir = os.environ["DATA"] + '/'+chart+'_'+rescount+'_finaljson/'
    txtdir  = os.environ["DATA"] + '/'+chart+'_'+rescount+'_finaltxt/'

    print('This run is for the:', chart,'HWM chart')

    pdyHHMM=sys.argv[1]
    pyr=pdyHHMM[0:4];pmt=pdyHHMM[4:6];pda=pdyHHMM[6:8];phr=pdyHHMM[8:10];pmn=pdyHHMM[10:12]

    t=datetime(int(pyr),int(pmt),int(pda),int(phr),int(pmn))
    epoch_pdyHHMM=int(time.mktime(t.timetuple()))

    #for hwm live: present-24
    end=epoch_pdyHHMM*1000
    begin=end-86400000

    print('HWM', chart, 'begin time:' , begin)
    print('HWM', chart, 'end time:',end)
    print("")

elif chart == 'daily':

    jsondir = os.environ["DATA"] + '/'+chart+'_'+rescount+'_finaljson/'
    txtdir  = os.environ["DATA"] + '/'+chart+'_'+rescount+'_finaltxt/'

    print('This run is for the:', chart,'HWM chart')

    ypdyHHMM=sys.argv[1]
    ypyr=ypdyHHMM[0:4];ypmt=ypdyHHMM[4:6];ypda=ypdyHHMM[6:8]

    y=datetime(int(ypyr),int(ypmt),int(ypda),00,00)
    yepoch_pdy=int(time.mktime(y.timetuple()))

    #for hwm daily: yesterday start to end
    begin=(yepoch_pdy*1000)
    end=begin+86400000

    print('HWM', chart, 'begin time:' , begin)
    print('HWM', chart, 'end time:',end)
    print("")

#function for sorting final lists in txt files
def takeFirst(elem):
    return elem[0]

#project list
with open("wcossii_projects") as file:
    project_list = file.readlines()
    project_list = [line.rstrip() for line in project_list]

for i in project_list:
    filename="%s.json" %(i)
    filenametxt="%s.txt" %(i)
    result2=[]
    for f in glob.glob(jsonsearch+filename):
        if os.path.getsize(f):
            if i in f:
                with open(f, 'rb') as infile:
#                    print('error_file=',f)
                    jsonAddfile=json.load(infile)
                    arr=jsonAddfile[0]['data']
                    count=0
#new data list constrained by time window entered
                    result=[]
                    for k in arr:
                        if k[0] > begin:
                            if k[0] < end:
                                count+=k[1]
                                result.append(k)
                    if count > 0:
                        result2.extend(result)
                        with open(txtdir+filenametxt, 'w') as final:
                            final.write(json.dumps(result2))
        else:
            print('Individual json file=',f,' empty, not combined!')

#read in nonzero arrays for each project within the time window printed from above
for i in project_list:
    filename="%s.json" %(i)
    for f in glob.glob(txtdir+'*'):
        if i in f:
            splitf=f.split('/')
            finalf=splitf[-1]
            a=[]
            with open(txtdir+finalf, 'r') as f:
                a = json.loads(f.read())
                a.sort(key=takeFirst)
#                for j in a:
#                    print(j)
#                print(a)
#                print(i)
#                print(finalf)
#                print(filename)
                with open(jsondir+filename, 'w') as final:
                    data = json.dumps([{"name":i,"data":a}],indent=4,sort_keys=False)
                    final.write(data)

#phasenm='p1'
phase_combined=chart+'_p1.json'
combined=[]
for f in glob.glob(jsondir+'*'):
    result=[]
#    print(f)
    with open(f, 'rb') as infile:
        jsonAddfile=json.load(infile)
        result.append(jsonAddfile)
    combined.extend(result)
##    splitf=f.split('/')
##    finalf=splitf[-1]
##    foo2=open(finalf,'w')
#    foo2=open(jsondir+finalf,'w')
##    sortedResult=sorted(result,key=lambda k:k[0]['name'])
##    bylat = json.dumps(sortedResult,indent=4,sort_keys=True)
##    foo2.write(bylat)
##    foo2.close()

#make final combined file
#combf = open("%s.json" %(phasenm),'w')
combf = open(jsondir+phase_combined,'w')
sortedCombf = sorted(combined,key=lambda k:k[0]['name'])
combjson = json.dumps(sortedCombf,indent=4,sort_keys=True)
combf.write(combjson)
combf.close()
