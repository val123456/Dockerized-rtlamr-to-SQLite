# exit on any error.  Script below will not produce any recoverable errors.
set -e 

# colors for output
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "\n${RED}Waiting for rtl_tcp server $RTL_TCP_SERVER on port $RTL_TCP_SERVER_PORT\n"

# Use netcat ( nc ) to connect to rtl_tcp to see if it is up and accepting connections
until echo "Waiting.." ; sleep 10; nc -z -v -w5 $RTL_TCP_SERVER $RTL_TCP_SERVER_PORT; do :; done

echo -e "\n${RED}Waiting for Python backend server $PYTHON_SERVER on port $PYTHON_SERVER_PORT\n"

# Use netcat ( nc ) to connect to the python application to see if it is up and accepting connections
until echo "Waiting..."; sleep 10; nc -z -v -w5 $PYTHON_SERVER $PYTHON_SERVER_PORT; do :; done

# wait for python app to close and reopen socket after test connection attempt
sleep 4

echo -e "\n${RED}Looking for meter IDs $METER_IDS\n"
echo -e "${RED}Looking for meter types $TYPES\n"

# Launch rtlamr with rtl_tcp IP:port, message types, and meters IDS.  Pipe ( | ) to nc to send output to python app in another container.  Background it to enable monitoring
/root/go/bin/rtlamr -server=$RTL_TCP_SERVER:$RTL_TCP_SERVER_PORT -msgtype=$TYPES -format=json -unique=false -filterid=$METER_IDS | nc -w 1800 $PYTHON_SERVER $PYTHON_SERVER_PORT &

# simple status monitoring.  Checks to see if rltamr and nc programs are running, exits container if either dies.  Runs every 120 seconds
# docker will restart after exit
while true
do

    sleep 120

    if  ! pgrep -x rtlamr > /dev/null ; then
        echo "rtlamr died"
        killall nc
        exit 1
    fi

    if  ! pgrep -x nc > /dev/null ; then
        echo "nc died"
        killall rtlamr
        exit 1
    fi
    
done
