p	#!/bin/bash
# file location: /home/pi/CPU_temperature/log_temperature.sh
path=/home/pi/proxyconf
now=$(date +%Y-%m-%d_%H:%M:%S)
temp=$(vcgencmd measure_temp)
rm           $path/actual_CPU_*
touch        $path/actual_CPU_$temp
echo $temp > $path/actual_CPU_$temp
echo -n $now  " "     >> $path/temperature.log
vcgencmd measure_temp >> $path/temperature.log
#echo $temp > $path/actual_CPU_temp.txt
