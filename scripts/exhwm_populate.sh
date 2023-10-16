#!/bin/bash

set -x

echo "*********************************************************************************************"
echo "EXHWM POPULATE ${res} ${rescount^^} SCRIPT EXECUTION"
echo "starttime= `date`"
start=`date +%s.%N`

#check for existence of intermediate project files
if [[ -f "$COMOUTproj/wcossii_projects_${res}_${rescount}" ]];then
   cpreq $COMOUTproj/wcossii_projects_${res}_${rescount} $DATA/wcossii_projects
else
   echo "file doesn't exist, make it, and initialize all json files in hwm_test_new_proj.sh!"
   touch wcossii_projects
fi

#check for new projects in pbs project file. This is a seamless process to 
#update project file to avoid HMW failures when projects are added to the project file after json files are initialized at 0Z
echo "CHECK PBS PROJECT FILES FOR NEW PROJECTS OR IF PROJECT FILE IS MISSING EMPTY, INITIALIZE NEW FILES!!!"
${USHhwm}/hwm_test_new_proj.sh
export err=$?; err_chk

#check if initialized files are in COMINnwges (today)
if [ -z "$(ls -A $COMINnwges)" ] ; then
   echo "WARNING: NO INITIALIZED JSON FILES FOUND IN $COMINnwges"
   echo "INITIALIZING JSON FILES FOR $PDY!!!!"

   ${USHhwm}/hwm_initialize.py $PDY $rescount
   export err=$?; err_chk

else

   echo "Previously populated json files copied from $COMINnwges!!!"
   cpreq $COMINnwges/*json $DATA/$PDY/jsonfiles_$rescount

   echo "checking for zero byte file size for json files copied from $COMINnwges"

   shopt -s nullglob
   for i in $DATA/$PDY/jsonfiles_$rescount/*.json; do

      if [ -s "$i" ]
      then
         echo "populated file $i copied from $COMINnwges exists and is not empty, do nothing" > /dev/null
      else
         echo "POPULATED FILE $i FROM $COMINnwges DOES NOT EXIST OR IS EMPTY, REINITIALIZE!!!!!"
         newi=$(echo $i | sed 's/.*\///' | sed 's|\(.*\)\..*|\1|')
         ${USHhwm}/hwm_reinit.py $PDY ${rescount} $newi
         export err=$?; err_chk
      fi

   done

fi

#copy reinitialized files back into directory of files to be populated from this run
shopt -s nullglob
for i in $DATA/$PDY/new_reinit_files_$rescount/*.json; do
   cpreq $i $DATA/$PDY/jsonfiles_$rescount
done

export qstat_start=$(date +%s.%N)

set +x

#determine server running on, qstat from that if run is during that time
cluster=$(cat /etc/cluster_name | cut -c1)

#dump F and R jobs
if [[ $(qstat -fHw @${cluster}bqs01) ]]; then
   echo "server ${cluster}bqs01!!!"
   qstat -fHw @${cluster}bqs01 | grep -E "Job Id|job_state|project =|queue =|exec_vnode =|Resource_List.place =|history_timestamp =|stime =" > qstat.out
   qstat -frw @${cluster}bqs01 | grep -E "Job Id|job_state|project =|queue =|exec_vnode =|Resource_List.place =|stime =" > qstat_running.out
elif [[ $(qstat -fHw @${cluster}bqs02) ]]; then
   echo "server ${cluster}bqs02!!!"
   qstat -fHw @${cluster}bqs01 | grep -E "Job Id|job_state|project =|queue =|exec_vnode =|Resource_List.place =|history_timestamp =|stime =" > qstat.out
   qstat -frw @${cluster}bqs01 | grep -E "Job Id|job_state|project =|queue =|exec_vnode =|Resource_List.place =|stime =" > qstat_running.out
fi

#Append files for read into python code
cat qstat_running.out >> qstat.out

set -x

#echo results of qstat to log 
echo "####################### start qstat.out echo #############################"
head -100 qstat.out 
echo "####################### end qstat.out echo ###############################"

#for 12 hours ago, the extent of qstat (to make sure the qstat covers this window)
export SPDYHHMM=$(date -d "360 minutes ago" +"%Y%m%d%H%M")
export EPDYHHMM=$(date +"%Y%m%d%H%M")

export qstat_end=$(date +%s.%N)
export qstat_time=$( echo "$qstat_end - $qstat_start" | bc -l )
echo "qstattime $rescount was $qstat_time seconds"

num_projs=$(wc -l wcossii_projects | awk '{print $1}')
echo $num_projs

SPDY=$(echo $SPDYHHMM | cut -c1-8)

#Only initialize these files or copy to DATA if they are needed. If the search start time SPDY is not in YPDY (yesterday), not needed
if [[ "${SPDY}" == "${YPDY}" ]]; then

   echo "$SPDY = $YPDY start time (SPDY) of search = YPDY, copy json files from $COMINnwgesy or initialize if they aren't there!!!"

   if [ -z "$(ls -A $COMINnwgesy)" ] ; then
      echo "WARNING: NO INITIALIZED JSON FILES FOUND IN $COMINnwgesy"
      echo "INITIALIZING JSON FILES FOR $YPDY!"

      ${USHhwm}/hwm_initialize.py $YPDY $rescount
      export err=$?; err_chk

   else

      echo "Previously populated json files copied from $COMINnwgesy!!!"
      cpreq $COMINnwgesy/*json $DATA/$YPDY/jsonfiles_$rescount

      echo "checking for zero byte file size for json files copied from $COMINnwges"

      shopt -s nullglob
      for i in $DATA/$YPDY/jsonfiles_$rescount/*.json; do

         if [ -s "$i" ]
         then
            echo "populated file $i copied from $COMINnwgesy exists and is not empty, do nothing" > /dev/null
         else
            echo "POPULATED FILE $i FROM $COMINnwgesy DOES NOT EXIST OR IS EMPTY, REINITIALIZE!!!!!"
            ynewi=$(echo $i | sed 's/.*\///' | sed 's|\(.*\)\..*|\1|')
            ${USHhwm}/hwm_reinit.py $YPDY ${rescount} $ynewi
            export err=$?; err_chk
         fi

      done
   fi

   #copy reinitialized files back into directory of files to be populated from this run
   shopt -s nullglob
   for i in $DATA/$YPDY/new_reinit_files_$rescount/*.json; do
      cpreq $i $DATA/$YPDY/jsonfiles_$rescount
   done

fi

#code exits after finding the first instance of a gap in the hwm live charts, which is the furthest back in the 12 hour input window
FSPDYHHMM=$(${USHhwm}/hwm_get_gaps.py $SPDYHHMM $EPDYHHMM $num_projs $rescount)
echo "final start time from get gaps code= $FSPDYHHMM"

FSPDY=$(echo $FSPDYHHMM | cut -c1-8)

${USHhwm}/hwm_${res}_populate.py $FSPDYHHMM $EPDYHHMM $rescount
export err=$?; err_chk

echo "copy files to COMOUT"

shopt -s nullglob
for i in $DATA/$PDY/jsonfiles_$rescount/*.json; do

   if [ -s "$i" ]
   then
      echo "populated file $i exists and is not empty, copying to $COMOUTnwges" > /dev/null
      cpreq $i $COMOUTnwges
   else
      echo "populated file $i does not exist, or is empty, do not copy to $COMOUTnwges"
   fi

done

#only copy these files if they were copied to DATA and populated, this tests for that
if [[ "${FSPDY}" == "${YPDY}" ]]; then

   echo "copy files to COMOUTy"

   shopt -s nullglob
   for i in $DATA/$YPDY/jsonfiles_$rescount/*.json; do

      if [ -s "$i" ]
      then
         echo "populated file $i exists and is not empty, copying to $COMOUTnwgesy" > /dev/null
         cpreq $i $COMOUTnwgesy
      else
         echo "populated file $i does not exist, or is empty, do not copy to $COMOUTnwgesy"
      fi

   done
fi

end=$(date +%s.%N)
runtime=$(echo "$end - $start" | bc -l )
echo "runtime for exhwm_populate for ${res} ${rescount} was $runtime seconds"

echo "EXIT EXHWM POPULATE ${res} ${rescount^^} SCRIPT EXECUTION"
echo "**********************************************************************************************"
