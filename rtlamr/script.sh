set -e 

# colors for output
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "\n${RED}Waiting for rtl_tcp server $RTL_TCP_SERVER on port $RTL_TCP_SERVER_PORT\n"
until echo "Waiting.." ; sleep 10; nc -z -v -w5 $RTL_TCP_SERVER $RTL_TCP_SERVER_PORT; do :; done

echo -e "\n${RED}Waiting for Python backend server $PYTHON_SERVER on port $PYTHON_SERVER_PORT\n"
until echo "Waiting..."; sleep 10; nc -z -v -w5 $PYTHON_SERVER $PYTHON_SERVER_PORT; do :; done
# until ping -c 4 -W 2 $PYTHON_SERVER; do :; done
# wait for server to reopen socket after test connection
sleep 3

echo -e "\n${RED}Looking for meter IDs $METER_IDS\n"
echo -e "${RED}Looking for meter types $TYPES\n"
/root/go/bin/rtlamr -server=$RTL_TCP_SERVER:$RTL_TCP_SERVER_PORT -msgtype=$TYPES -format=json -unique=false -filterid=$METER_IDS | nc -w 900 $PYTHON_SERVER $PYTHON_SERVER_PORT &

sleep 10

while true
do

    if  pgrep -x rtlamr > /dev/null ; then
        # echo "rtlamr alive"
        :
    else
        echo "rtlamr died"
        killall nc
        exit 1
    fi

    if  pgrep -x nc > /dev/null ; then
        # echo "nc alive"
        :
    else
        echo "nc died"
        killall rtlamr
        exit 1
    fi
    sleep 60
    
done
