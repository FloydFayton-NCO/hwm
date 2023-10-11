#!/bin/bash

set -x

echo "*********************************************************************************************"
echo "EXHWM COMBINE ${res} ${rescount^^} SCRIPT EXECUTION"
echo "starttime= `date`"
start=`date +%s.%N`

#copy fixed files to work directory
cpreq $COMOUTproj/wcossii_projects_${res}_${rescount} $DATA/wcossii_projects

if [ -d "$COMINnwgesy" ] ; then
echo "$COMINnwgesy DIRECTORY FOUND!!!"

   if [ -z "$(ls -A $COMINnwgesy 2>/dev/null)" ] ; then
      echo "WARNING: NO INITIALIZED JSON FILES FOUND IN $COMINnwgesy"
      echo "INITIALIZING JSON FILES FOR $YPDY FOR THIS RUN!!!!!"

      ${USHhwm}/hwm_initialize.py $YPDY $rescount
      export err=$?; err_chk

      cpreq $DATA/$YPDY/jsonfiles_$rescount/*json $DATA/nwges_${rescount}01 
  
   else
      echo "$COMINnwgesy FILES COPIED TO $DATA/nwges_${rescount}01 FOR COMBINE!!!"
      cpreq $COMINnwgesy/* $DATA/nwges_${rescount}01 
   fi

else

   echo "WARNING: $COMINnwgesy DIRECTORY NOT FOUND!!!"
   echo "INITIALIZING JSON FILES FOR $YPDY FOR THIS RUN!!!!!"

   ${USHhwm}/hwm_initialize.py $YPDY $rescount
   export err=$?; err_chk

   cpreq $DATA/$YPDY/jsonfiles_${rescount}/*json $DATA/nwges_${rescount}01 

fi

#test for yesterdays COMIN/nwges, if it doesn't exist for populated files, initialize files but keep them in data so combine doesn't fail
#let populate code deal with it. 

if [ -d "$COMINnwges" ] ; then
   echo "$COMINnwges DIRECTORY FOUND!!!"

   if [ -z "$(ls -A $COMINnwges 2>/dev/null)" ] ; then
      echo "WARNING: NO INITIALIZED JSON FILES FOUND IN $COMINnwges"
      echo "INITIALIZING JSON FILES FOR $PDY!"

      ${USHhwm}/hwm_initialize.py $PDY $rescount
      export err=$?; err_chk

      cpreq $DATA/$PDY/jsonfiles_$rescount/*json $DATA/nwges_${rescount}02

   else
      echo "$COMINnwges FILES COPIED TO $DATA/nwges_${rescount}02 FOR COMBINE!!!"
      cpreq $COMINnwges/* $DATA/nwges_${rescount}02
   fi

else

   echo "WARNING: $COMINnwges DIRECTORY NOT FOUND!!!"
   echo "INITIALIZING JSON FILES FOR $PDY FOR THIS RUN!!!!!"

   ${USHhwm}/hwm_initialize.py $PDY $rescount
   export err=$?; err_chk

   cpreq $DATA/$PDY/jsonfiles_${rescount}/*json $DATA/nwges_${rescount}02

fi

export chart=live

#final combined file in live_finaljson in DATA
${USHhwm}/hwm_combine.py $PDYHHMM $chart $rescount
export err=$?; err_chk

export chart=daily

#final combined file in daily_finaljson in DATA
${USHhwm}/hwm_combine.py $YPDYHHMM $chart $rescount
export err=$?; err_chk

echo "copy final combined files from the live and daily combine runs to $COMOUT"

livefile="$DATA/live_${rescount}_finaljson/live_p1.json"

   if [ -s "$livefile" ]
   then
      echo "final combined file $livefile exists and is not empty, copying to $COMOUT"
      cpreq $DATA/live_${rescount}_finaljson/live_p1.json $COMOUT/live_${res}_${rescount}_p1.json    
   else
      echo "final combined file $livefile does not exist, and is not empty, not copying to $COMOUT"
   fi

dailyfile="$DATA/daily_${rescount}_finaljson/daily_p1.json"

   if [ -s "$dailyfile" ]
   then
      echo "final combined file $dailyfile exists and is not empty, copying to $COMOUT"
      cpreq $DATA/daily_${rescount}_finaljson/daily_p1.json $COMOUT/daily_${res}_${rescount}_p1.json
   else
      echo "final combined file $dailyfile does not exist, and is not empty, not copying to $COMOUT"
   fi

end=$(date +%s.%N)
runtime=$(echo "$end - $start" | bc -l )
echo "runtime for exhwm_combine was $runtime seconds"
echo "endtime= `date`"

echo "EXIT COMBINE ${res} ${rescount^^} SCRIPT EXECUTION"
echo "**********************************************************************************************"
