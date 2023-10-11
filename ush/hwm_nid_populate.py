#!/usr/bin/env python
"""hwm_populate.py: code to count cores or nodes per project for queues and populate results into individual json files in COMOUT"""
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

#working directory, used for read and write of json files below
jsond = os.environ["DATA"]

#merge lists for project and nodes and project
def merge(list1, list2):

    merged_list = []
    for i in range(max((len(list1), len(list2)))):

        while True:
            try:
                tup = (list1[i], list2[i])
            except IndexError:
                if len(list1) > len(list2):
                    list2.append('')
                    tup = (list1[i], list2[i])
                elif len(list1) < len(list2):
                    list1.append('')
                    tup = (list1[i], list2[i])
                continue

            merged_list.append(tup)
            break
    return merged_list

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Set PDY
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#start and end time of run (will make the chart for that time window, and whether the run is to count nodes or cores
spdyhhmm=sys.argv[1];epdyhhmm=sys.argv[2];countres=sys.argv[3]

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

#commented out 202202, to not constrain to a list of queues, therefore using ALL queues returned from qstat in ex populate script. Kept this 
#here in case there's ever a need for it again (GM SPA). 

#with open("queue_list") as file:
#    queue_list = file.readlines()
#    queue_list = [line.rstrip() for line in queue_list]

#finallist of read in data after jobs we aren't concerned with are filtered out (after core count, or node (nodes not counted before going into list) below)
#I do extensive filtering of jobs before writing into finallist, this is necessary to avoid failures from a necessary variable not getting into the finallist. 
finallist=[]

#Read in qstat file
processing = True

jobs_file = open("qstat.out", "r")

# Handles chunks
while True:
    first_job_line = True
#each loop through creates a new dictionary for a job that is processed below and appeneded to finallist
    new={}

    # Handles one job
    while True:
        job_line = jobs_file.readline()

        # detect the end of the file
        if job_line == '':
            processing = False
            break

        # Detect first line(job id)
        if first_job_line:
            (key,val)= job_line.rstrip("\n").split(': ')
            splitv=val.split('.')
            new[key] = splitv[0]
            #search key to allow for 01/02 switch, and all 3 wcoss2 systems (abqs, dbqs, cbqs)
            if "bqs0" not in job_line:
                raise Exception("First line is not the job Id, file (or file chunk) isn't correct!!!")

            first_job_line = False
            continue  

        # Detect end of job line
        if "project = " in job_line:
            (key, val) = job_line.rstrip("\n").split(' = ')
            new[key] = str(val)
            break

        # if it is neither a first job line(jobid), or end job line(project variable), nor the end of the file
        # then it must be a job line between the first and last line of a job, read into dictionary
        (key, val) = job_line.rstrip("\n").split(' = ')
        new[key] = str(val)

    # end the while loop when end of file is reached
    if not processing:
        print('File Read In!!!')
        break

#remove whitespace from keys
    new = {x.replace(' ', ''): v for x, v in new.items()}

#deal with syntax errors in submitted project codes for jobs. Strip off first name (project)
#and last (projenv). I'm assuming an error like NCO-T20-TCO, where it "runs" and is 
#in qstat dump as "running," but incorrect in syntax.  
    for k,v in new.items():
        if k == 'project':
            splitv=v.split('-')
            new["project"] = splitv[0]+'-'+splitv[-1]

#sort through project list into new dictionary
    newer={}
    for key, value in new.items():    
        for i in project_list:
            if i in value:
                for key, value in new.items():
                    newer[key] = str(value)

#commented out 202202, kept incase needed again (GM SPA)
##sort through queue list into new dictionary old
##        newest={}
##    for key, value in newer.items():
##        for i in queue_list:
##            if i in value:
##                for key, value in newer.items():
##                    newest[key] = str(value)

##convert values to str in new dictionary
    newest={}
    for key, value in newer.items():
        newest[key] = str(value)

    if countres == 'nodes':

#nodes need to be counted every time slice so nodes aren't double counted, so the finalist here
#is just the raw exec_vnode. The purpose of this section is to weed out jobs that aren't F or R,
#with no exec_vnode, or stime. Some F jobs don't have either. 
        for key, value in newest.items():
            if key == 'job_state':
                if value == 'F' or value == 'R':
                    for key, value in newest.items():
                        if key == 'exec_vnode':
                            if 'nid' in value:
                                for key, value in newest.items():
                                    if key == 'stime':
                                        #final list to sort through each time slice, it's highly constrained to avoid failures in the project count next section
                                        finallist.append(newest)

#count cores once before jobs go into finallist
    elif countres == 'cores':

#count cores once, no need to worry about double counting
        for key, value in newest.items():
            if key == 'job_state':
                if value == 'F' or value == 'R':
                    for key, value in newest.items():
                        if key == 'exec_vnode':
                            if 'nid' in value:
                                for key, value in newest.items():
                                    if key == 'stime':
                                        for key, value in newest.items():
                                            if key == 'Resource_List.place':
                                                if 'excl' in value:
                                                    for key, value in newest.items():
                                                        if key == 'exec_vnode':
                                                            matches = re.findall(r'([n][i][d]\d\d\d\d\d\d)',value, re.DOTALL)
                                                            count=0
                                                            for i in matches:
                                                                count+=1
                                                            cores=int(count)*128
                                                            newest["exec_vnode"] = cores
                                                elif 'excl' not in value:
                                                    for key, value in newest.items():
                                                        if key == 'exec_vnode':
                                                            newvalue=re.split('ncpus=|:|\)',value)
                                                            cleaned = [ x for x in newvalue if x.isdigit() ]
                                                            intcleaned = [ int(x) for x in cleaned ]
                                                            cores=sum(intcleaned)
                                                            newest["exec_vnode"] = cores

                                        #final list to sort through each time slice, it's highly constrained to avoid failures in the next section
                                        #this list has a core count, unlike the list for nodes above. The core-count code runs faster. 
                                        finallist.append(newest)

timesteps=int((epoch_end-epoch_start)/60000)
timei=epoch_start
min_count=0

for i in range(0,timesteps):

#final lists for the number of nodes used for each project for each time slice
    listproj=[]
    listnodes=[]

#make a list of used nodes for every time slice. 
    countlist=[]

    for job in finallist:
        for key, value in job.items():
            if key == 'history_timestamp':
                his_timestamp=int(value)*1000
            elif key == 'stime':
                dt = datetime.strptime(value, "%a %b %d %H:%M:%S %Y")
                stime_epoch=int(time.mktime(dt.timetuple()))*1000

        for key, value in job.items():
            if key == 'job_state':
                if value == 'F':
                    for key, value in job.items():
                        if key == 'project':
                            if timei > stime_epoch:
                                if timei < his_timestamp:
                                    listproj.append(value)
                        elif key == 'exec_vnode':
                            if countres == 'nodes':
                                if timei > stime_epoch:
                                    if timei < his_timestamp:
                                        matches = re.findall(r'([n][i][d]\d\d\d\d\d\d)',value, re.DOTALL)
                                        count=0
                                        for m in matches:
                                            if str(m) not in str(countlist):
                                                count+=1
                                                countlist.append(m)
                                        newvalue = value.replace(value,str(count))
                                        listnodes.append(int(newvalue))

                            elif countres == 'cores':
                                if timei > stime_epoch:
                                    if timei < his_timestamp:
                                        listnodes.append(int(value))

                elif value == 'R':
                    for key, value in job.items():
                        if key == 'project':
                            if timei > stime_epoch:
                                if timei < epoch_end:
                                    listproj.append(value)
                        elif key == 'exec_vnode':
                            if countres == 'nodes':
                                if timei > stime_epoch:
                                    if timei < epoch_end:
                                        matches = re.findall(r'([n][i][d]\d\d\d\d\d\d)',value, re.DOTALL)
                                        count=0
                                        for m in matches:
                                            if str(m) not in str(countlist):
                                                count+=1
                                                countlist.append(m)
                                        newvalue = value.replace(value,str(count))
                                        listnodes.append(int(newvalue))

                            elif countres == 'cores':
                                if timei > stime_epoch:
                                    if timei < epoch_end:
                                        listnodes.append(int(value))

##do a final count of nodes per project
    count={}
    for k,v in merge(listproj, listnodes):
        if k in count:
            count[k] += v
        else:
            count[k]=v

##timei_cal used to search through json files in DATA directory
    timei_cal = datetime.fromtimestamp(timei/1000).strftime('%Y%m%d')
    print('')

#match projects and nodes used per run with initialized json files. If time in initialized file matches 
#with this run, the json file for that timestamp gets replaced

    dir_contents = os.listdir(jsond+'/'+timei_cal+'/jsonfiles_'+countres+'/')
    if dir_contents:
        for k,v in count.items():
            filename="%s.json" %(k)
            with open(jsond+'/'+timei_cal+'/jsonfiles_'+countres+'/'+filename, 'r') as f:
                json_data = json.load(f)
                arr=json_data[0]['data']
                for i in arr:
                     if timei == i[0]:
                        i[1]=v
                        print('Time match', timei,' was found in the initialized files, populating:',filename, countres, v)
                        with open(jsond+'/'+timei_cal+'/jsonfiles_'+countres+'/'+filename, 'w') as final:
                            data = json.dumps([{"name":k,"data":arr}],indent=4,sort_keys=False)
                            final.write(data)

#if initialized files don't exist in that directory, program will stop with this warning in the log file. 
    else:
        print('No initialized files in directory. Exiting!')
        exit()

    timei+= 60000
    min_count+=1
    print('minute after gap= ',min_count)
    final_time = datetime.fromtimestamp(timei/1000).strftime('%Y%m%d%H%M')
    print('calendar date of populated timestamp in json file= ' ,final_time)
