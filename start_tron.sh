#!/bin/bash
for i in `cat tile-hosts.txt` 
do
    ssh -f $i 'cd /export/home/sharedapps/Tron; export DISPLAY=:0.0; sudo ./tron_render.py'
done