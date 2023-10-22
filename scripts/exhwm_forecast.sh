#!/bin/bash

set -x

echo "*********************************************************************************************"
echo "EXHWM FORECAST ${res} ${rescount^^} SCRIPT EXECUTION"
echo "starttime= `date`"
start=`date +%s.%N`

# Copy original/current HWM chart to $DATA for modification

if [ -s "$COMIN/$live" ]; then
   echo "final combined file $live exists and is not empty, copying to $DATA"
   cpreq $COMIN/${live} $DATA/${live}
   IJSON=${IJSON:-${DATA}/${live}}
elif [ -s "$COMINy/$daily" ]; then
   echo "final combined file $daily exists and is not empty, copying to $DATA"
   cpreq $COMIN/${daily} $DATA/${daily}  
   IJSON=${IJSON:-${DATA}/${daily}}
elif [ -s "$IJSON" ]; then #local/non-system control file
   echo "non-system file $IJSON exists and is not empty, copying to $DATA"
   IJSON=${IJSON:-${DATA}/${live}}
else
   echo "final combined file, live or daily, does not exist, and is not empty, not copying to $DATA"
   err_exit
fi

${USHhwm}/hwm_forecast.py
export err=$?; err_chk

cpreq $DATA/hwm_*.json $COMOUTnwges/

function rsync_sh {
   source=$1
   dest=$2
   set +xa

   if [ $# -eq 2  ] ; then
      echo "=========================================================================================="
      echo "Now running \"rsync $source $dest\" "
      echo "=========================================================================================="
      echo " "
   else
      echo "FATAL ERROR: Missing source or destination variable."
      echo "Usage:  rsync_sh $source $dest"
      err_exit
   fi
   set -xa
   let numattempts=3
   while [ $numattempts -gt 0 ]; do
      /usr/bin/rsync ${options[@]} ${source} ${dest}
      err=$?
      date
      if [ $err -eq 23 ] || [ $err -eq 24 ]; then
         echo "Possible Failure: error code is 23, check if any file is really missing"
         let numattempts=-1  # successful completion
      elif [ $err -ne 0 ]; then
         ((numattempts--))
         sleep 5
      else
         let numattempts=-1  # successful completion
      fi
   done
   if [ $numattempts -eq 0 ]; then
      echo "FATAL ERROR: rsync failed after three attempts"
      err_exit
   fi
}

export SERVER=nwprod@intra
export RSYNC=rsync_sh
export options=(-aWzv --timeout=30 --delete --progress --stats)

cluster=$(cat /etc/cluster_name)

export REMOTE_PROD="~/pmb/spatools/HWM/${cluster^^}"
export REMOTE_PARA="~/pmb/spatools/HWM/${cluster^^}_${envir}"

if [ "${SENDWEB}" = "YES" ] && [ "${envir}" = "prod" ]; then

   echo "transfer forecast hwm files to intra!!!!"
   ${RSYNC} $COMIN/hwm_fcst_${res}_${rescount}_p1.json ${SERVER}:${REMOTE_PROD}/forecast/data
   export err=$?; err_chk 

elif [ "${SENDWEB}" = "YES" ] && [ "${envir}" = "para" ];then

   echo "transfer forecast HWM files to intra!!!!"
   ${RSYNC} $COMIN/hwm_fcst_${res}_${rescount}_p1.json ${SERVER}:${REMOTE_PARA}/forecast/data
   export err=$?; err_chk

else
   echo "NO FILES BEING SENT TO INTRA WITH THIS RUN!!!!!!!!!!!!!"
fi

end=$(date +%s.%N)
runtime=$(echo "$end - $start" | bc -l )
echo "runtime for exhwm_combine was $runtime seconds"
echo "endtime= `date`"

echo "EXIT COMBINE ${res} ${rescount^^} SCRIPT EXECUTION"
echo "**********************************************************************************************"
