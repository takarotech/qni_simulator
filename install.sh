#!/bin/bash

#-> Make sure we don't run as root
if (( EUID == 0 )); then
   echo 'Please run without sudo!' 1>&2
   exit 1
fi

#-> Install pyscreenshot package for capturing screen regions
sudo -H pip3 install pyscreenshot
