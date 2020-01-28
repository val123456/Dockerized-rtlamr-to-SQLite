# colors for output
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "\n${RED}Waiting for rtl_tcp server $RTL_TCP_SERVER on port $RTL_TCP_SERVER_PORT\n"
until ping -c 4 -W 2 $RTL_TCP_SERVER; do :; done

echo -e "\n${RED}Waiting for Python backend server $PYTHON_SERVER on port $PYTHON_SERVER_PORT\n"
until ping -c 4 -W 2 $PYTHON_SERVER; do :; done

echo -e "\n${RED}Looking for meter IDs $METER_IDS\n"
echo -e "${RED}Looking for meter types $TYPES\n"
/root/go/bin/rtlamr -server=$RTL_TCP_SERVER:$RTL_TCP_SERVER_PORT -msgtype=$TYPES -format=json -unique=true -filterid=$METER_IDS | nc $PYTHON_SERVER $PYTHON_SERVER_PORT
