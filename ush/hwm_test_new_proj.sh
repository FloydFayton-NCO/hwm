#!/bin/bash

#######################################################################################################################
#
#This script automates the adding of projects to the BPS_PROJ_FILE. If there was simply a link to this file 
#for all my populate and combine codes, they would fail because once a day all the json files are initialized at 00z. 
#So this script is needed to determine the new projects, initialize files for them only, and move them to COMOUTnwges(y)
#for all the populate and combine codes to work correctly.
#
# area of chart   :   http://www2.nco.ncep.noaa.gov/pmb/spatools/HWM/DOGWOOD/live/p1.nodes.html
#                     http://www2.nco.ncep.noaa.gov/pmb/spatools/HWM/DOGWOOD/live/p1.cores.html
#		      http://www2.nco.ncep.noaa.gov/pmb/spatools/HWM/DOGWOOD/daily/p1.nodes.html
#		      http://www2.nco.ncep.noaa.gov/pmb/spatools/HWM/DOGWOOD/daily/p1.cores.html
#
#                     http://www2.nco.ncep.noaa.gov/pmb/spatools/HWM/CACTUS/live/p1.nodes.html
#                     http://www2.nco.ncep.noaa.gov/pmb/spatools/HWM/CACTUS/live/p1.cores.html
#                     http://www2.nco.ncep.noaa.gov/pmb/spatools/HWM/CACTUS/daily/p1.nodes.html
#                     http://www2.nco.ncep.noaa.gov/pmb/spatools/HWM/CACTUS/daily/p1.cores.html
#
# product:        :   HWM
#
# Code: hwm_test_new_proj.sh 
#
# Output: new wcossii_projects file in FIX
#         new initialized *json files in COMOUTnwges and COMOUTnwgesy for populate and combine ex and ush codes
#
# History:
# Gregory Mott (author) 12/2021  new
#
###########################################################################################################################

#option -23 supresses output that is in both files (3), and output that is unique to MY_PROJ_FILE (2).
#we are only interested in new project additions in the PBS_PROJ_FILE and this method considers that.  

if [[ $(comm -23 <(sort < $PBS_PROJ_FILE) <(sort < $MY_PROJ_FILE)) ]]; then
   comm -23 <(sort < $PBS_PROJ_FILE) <(sort < $MY_PROJ_FILE) > new_wcossii_projects

   new_num_projs=$(wc -l new_wcossii_projects | awk '{print $1}')
   echo "$new_num_projs NEW PROJECTS HAVE BEEN ADDED TO THE PROJECT FILE OR THERE WAS NO PROJECT FILE IN COM!!!"
   cat new_wcossii_projects

   mkdir -p $DATA $DATA/$YPDY/new_proj_files_${rescount} $DATA/$PDY/new_proj_files_${rescount}

   echo "INITIALIZE FILES WITH NEW PROJECTS"
   #make initialized files for the new projects in the pbs project file, if there is any
   ${USHhwm}/hwm_initialize_new_proj.py $PDY ${rescount}
   export err=$?; err_chk

   ${USHhwm}/hwm_initialize_new_proj.py $YPDY ${rescount}
   export err=$?; err_chk

   #cat new projects into copied wcossii_projects file from COM (or initialized from system project file) for this run
   cat new_wcossii_projects >> wcossii_projects

   #copy new projects file into fix, make a backup of the old one

   #check for existence of intermediate project files
   if [[ -f "$COMOUTproj/wcossii_projects_${res}_${rescount}" ]];then
      cpreq $COMOUTproj/wcossii_projects_${res}_${rescount} $COMOUTproj/wcossii_projects_old_${PDY}_${res}_${rescount}
      cpreq wcossii_projects $COMOUTproj/wcossii_projects_${res}_${rescount}
      echo "UPDATED PROJECT FILE IN COM FOR THIS RUN!!!"
   else
      cpreq wcossii_projects $COMOUTproj/wcossii_projects_${res}_${rescount}
      echo "UPDATED PROJECT FILE IN COM FOR THIS RUN!!!"
   fi

   #copy new initialized files to COMOUT/nwges(y)'s
   cpreq $DATA/$PDY/new_proj_files_${rescount}/*json $COMOUTnwges
   cpreq $DATA/$YPDY/new_proj_files_${rescount}/*json $COMOUTnwgesy

   echo "COPIED INITIALIZED FILES TO COMOUT"

else
   echo "NO NEW PROJECTS IN PBS PROJ FILE THAT AREN'T IN MINE, DO NOTHING!!!"
fi
