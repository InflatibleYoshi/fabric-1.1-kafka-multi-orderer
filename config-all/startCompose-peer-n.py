import string
from sys import argv

script, arg1 = argv
arg1 = int(arg1)

for i in range(arg1):
    file = """#!/bin/bash

if [ -z ${FABRIC_START_TIMEOUT+x} ]; then
 echo "FABRIC_START_TIMEOUT is unset, assuming 15 (seconds)"
 export FABRIC_START_TIMEOUT=15
else

   re='^[0-9]+$'
   if ! [[ $FABRIC_START_TIMEOUT =~ $re ]] ; then
      echo "FABRIC_START_TIMEOUT: Not a number" >&2; exit 1
   fi

 echo "FABRIC_START_TIMEOUT is set to '$FABRIC_START_TIMEOUT'"
fi

# Exit on first error, print all commands.
set -ev

#Detect architecture
ARCH=`uname -m`

# Grab the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ARCH=$ARCH docker-compose -f "${DIR}"/composer/docker-compose-peer""" + str(i + 1) + """.yml down
ARCH=$ARCH docker-compose -f "${DIR}"/composer/docker-compose-peer""" + str(i + 1) + """.yml up -d
"""

    text_file = open("startCompose-Peer" + str(i + 1) + ".sh", "w")
    text_file.write(file)
    text_file.close()