#!/bin/bash

#-> Make sure we don't run as root
if (( EUID == 0 )); then
   echo 'Please run without sudo!' 1>&2
   exit 1
fi

#-> Go to the directory of this script
cd "$(dirname "${BASH_SOURCE[0]}")"

#-> Run qni_simulator with arguments
./src/qni_simulator.py "$@"
