#!/bin/bash
for i in `cat tile-hosts.txt` 
do
    ssh -f $i /export/home/sharedapps/Tron/kill-tron.sh
done
