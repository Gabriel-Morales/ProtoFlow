#!/bin/bash

# for all the packet (pcap) captures in the directory, generate a flow table for each.

file_names=`ls *pcap*`

for name in $file_names; do

	echo $name | ../../flow_meter.py

done