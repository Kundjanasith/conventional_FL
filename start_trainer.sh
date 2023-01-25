for ip in .1 .2 .3 .9 .13 .14 .15 .16 .33 .36 .37 .38 .39 .40 .41 .42
do
    echo $ip
    ssh 10.10.100$ip "cd ~/conventional_FL/trainer_mode && screen screen -d -m -L -Logfile screen_log -S trainer python3 main.py 10.10.100$ip 19192"
done
