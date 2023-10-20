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
elif [ -s "$live" ]; then
   echo "non-system file $live exists and is not empty, copying to $DATA"
   cpreq ${live} $DATA/${live}
   IJSON=${IJSON:-${DATA}/${live}}
else
   echo "final combined file, live or daily, does not exist, and is not empty, not copying to $DATA"
   err_exit
fi

${USHhwm}/hwm_forecast.py
export err=$?; err_chk

end=$(date +%s.%N)
runtime=$(echo "$end - $start" | bc -l )
echo "runtime for exhwm_combine was $runtime seconds"
echo "endtime= `date`"

echo "EXIT COMBINE ${res} ${rescount^^} SCRIPT EXECUTION"
echo "**********************************************************************************************"
