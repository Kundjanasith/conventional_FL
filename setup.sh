for ip in .1 .2 .3 .9 .13 .14 .15 .16 .33 .36 .37 .38 .39 .40 .41 .42 .45
do
    ssh 10.10.100.$ip "cd ~ && rm -rf conventional_FL"
done
