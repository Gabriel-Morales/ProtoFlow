#!/usr/bin/env python3

import os
import sys
import pandas as pd
import numpy as np

# Only labels bluetooth and wifi for now

# Purpose: For a *single* Consolidated and unlabeled table, use this tool and pruner.

devices = {'40:A9:CF:3B:13:DB' : 'streaming_stick',
		   'A8:5E:45:F6:1E:B8' : 'router',
		   'A8:5E:45:CA:6E:98' : 'router',
		   '78:9C:85:13:C7:7A' : 'smart_lock',
		   '78:9C:85:12:62:4E' : 'smart_lock',
		   '50:14:79:3C:C1:A8' : 'ereader',
		   'FE:70:1A:6D:F0:59' : 'smart_bp_monitor',
		   '60:AB:D2:FB:AA:AA' : 'smart_assistant',
		   '60:AB:D2:FB:AA:AB' : 'smart_speaker',
		   '88:D0:39:83:68:2A' : 'smart_switch',
		   '88:D0:39:83:67:55' : 'smart_switch',
		   '88:D0:39:82:FF:65' : 'smart_switch',
		   '88:D0:39:83:5E:BC' : 'smart_switch',
		   '88:D0:39:82:74:71' : 'smart_switch',
		   'C8:6C:3D:DF:F7:BE' : 'smart_assistant',
		   'D2:E9:05:C6:AC:75' : 'fitnesss_tracker',
		   '14:01:52:E3:B9:81' : 'smartphone',
		   'FB:D8:3E:DF:D4:CA' : 'smart_scale',
		   '50:14:79:3C:C1:A8' : 'smart_vacuum',
		   '40:A9:CF:53:67:45' : 'ereader',
		   'D1:FE:97:29:54:C4' : 'smart_thermometer',
		   '3C:61:05:D4:A9:B1' : 'smart_pet_feeder',
		   'EC:B5:FA:85:C1:86' : 'smart_bridge',
		   '58:24:29:67:AC:F5' : 'smartphone',
		   '64:03:7F:2F:7F:F9' : 'smartwatch',
		   '2C:71:FF:76:4D:DE' : 'smart_camera',
		   'EC:8A:C4:28:47:A1' : 'smart_camera',
		   '00:F3:81:A1:DA:05' : 'smart_camera',
		   '20:1F:3B:16:0C:04' : 'streaming_stick',
		   '14:22:3B:F1:47:98' : 'smartphone',
		   '14:22:3B:F1:47:C5' : 'smartphone',
		   '14:22:3B:F1:47:DD' : 'smartphone',
		   '14:22:3B:F1:47:39' : 'smartphone',
		   
		   '3A:9C:1D:94:AC:72' : 'smartphone',
		   '86:B6:25:22:EB:20' : 'smartphone',
		   '36:78:59:49:BB:4A' : 'smartphone',
		   '2A:69:93:83:CF:F9' : 'smartphone',
		   
		   '14:22:3B:F1:47:97' : 'smartphone',
		   '14:22:3B:F1:47:C4' : 'smartphone',
		   '14:22:3B:F1:47:DC' : 'smartphone', 
		   '14:22:3B:F1:47:68' : 'smartphone',
		   '58:24:29:67:AC:F4' : 'smartphone',
		   '14:01:52:E3:B9:82' : 'smartphone',
		   
		   'C0:06:C3:9B:D8:8C' : 'smart_camera',
		   'C0:06:C3:9B:D3:26' : 'smart_camera',
		   '48:A6:B8:FF:A6:3A' : 'smart_speaker',
		   '54:2A:1B:CC:58:3A' : 'smart_speaker',
		   'AC:84:C6:E3:3F:F4' : 'router'}

consolidated_cap = input('Path to flow table: ')

df = pd.read_csv(consolidated_cap, low_memory=False)
df['label'] = ''

device_keys = devices.keys()

# go through and label
for device in device_keys:
	df.loc[df['src_mac'] == device.lower(), 'label'] = devices[device]

consolidated_cap = consolidated_cap.split('/')[-1]
df['label'].replace('', np.nan, inplace=True)
df.dropna(subset=['label'], inplace=True)
df.to_csv(f'pruned_{consolidated_cap}', index=False)
