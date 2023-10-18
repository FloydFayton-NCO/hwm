#!/bin/bash

set -x

echo "*********************************************************************************************"
echo "EXHWM FORECAST ${res} ${rescount^^} SCRIPT EXECUTION"
echo "starttime= `date`"
start=`date +%s.%N`

# Copy original/current HWM chart to $DATA for modification
for infile in live_${res}_${rescount}_p1.json daily_${res}_${rescount}_p1.json; do
   if [ -s "$COMIN/$infile" ]; then
      echo "final combined file $infile exists and is not empty, copying to $DATA"
      cpreq $COMIN/${infile} $DATA/${infile} 
   else
      echo "final combined file $infile does not exist, and is not empty, not copying to $DATA"
      err_exit
   fi
done


end=$(date +%s.%N)
runtime=$(echo "$end - $start" | bc -l )
echo "runtime for exhwm_combine was $runtime seconds"
echo "endtime= `date`"

echo "EXIT COMBINE ${res} ${rescount^^} SCRIPT EXECUTION"
echo "**********************************************************************************************"
