# proxyconf
Some scripts and information to configure the proxy and log the CPU temperature of the Raspberry Pi

Logging the CPU temperature is easy with a script, which is executed using crontab.

Put the file in this location:
/home/pi/Documents/proxyconf/log_temperature.sh<br>
and add this line with crontab -e to execute temp logging each minute.<br><br>
<code>   * *  *   *   *     /home/pi/Documents/proxyconf/log_temperature.sh </code> 

The script will write two files into file location:
1. temperature.log where measurements are appended
2. a file called actual_CPU_temp.txt which contains the date and time and actual temperature measurement

You may install this script once and then automatically get CPU temperature logging. This might be interesting in the RPi,
if you experience occasional crashes or freezes, which might be caused by an overheated CPU.
