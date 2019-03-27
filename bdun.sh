SLPTM=300

while [ 1 -eq 1 ]
do

if [ -f testCombos_6max_40.psv ]
then

echo "found file, killing stuff & shutting down"
ps -ef | grep TestComboGame.py | grep -v grep | awk '{ print "kill " $2 }' | bash
shutdown -P now
exit 0

fi

echo "sleeping 5 minutes `date`"
sleep ${SLPTM}

done

