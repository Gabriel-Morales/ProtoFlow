#!/usr/bin/env python3

import os
import sys
import pandas as pd
import numpy as np

# Only labels bluetooth and wifi for now

# Purpose: For a *single* Consolidated and unlabeled table, use this tool and pruner.
# Here the labels are given a higher level of abstraction.

devices = {'40:A9:CF:3B:13:DB' : 'audio_video',
		   'A8:5E:45:F6:1E:B8' : 'hub_gateway',
		   'A8:5E:45:CA:6E:98' : 'hub_gateway',
		   '78:9C:85:13:C7:7A' : 'utility',
		   '78:9C:85:12:62:4E' : 'utility',
		   '50:14:79:3C:C1:A8' : 'mobile_device',
		   'FE:70:1A:6D:F0:59' : 'wearable',
		   '60:AB:D2:FB:AA:AA' : 'audio_video',
		   '60:AB:D2:FB:AA:AB' : 'audio_video',
		   '88:D0:39:83:68:2A' : 'utility',
		   '88:D0:39:83:67:55' : 'utility',
		   '88:D0:39:82:FF:65' : 'utility',
		   '88:D0:39:83:5E:BC' : 'utility',
		   '88:D0:39:82:74:71' : 'utility',
		   'C8:6C:3D:DF:F7:BE' : 'audio_video',
		   'D2:E9:05:C6:AC:75' : 'wearable',
		   '14:01:52:E3:B9:81' : 'mobile_device',
		   'FB:D8:3E:DF:D4:CA' : 'utility',
		   '50:14:79:3C:C1:A8' : 'utility',
		   '40:A9:CF:53:67:45' : 'mobile_device',
		   'D1:FE:97:29:54:C4' : 'utility',
		   '3C:61:05:D4:A9:B1' : 'utility',
		   'EC:B5:FA:85:C1:86' : 'hub_gateway',
		   '58:24:29:67:AC:F5' : 'mobile_device',
		   '64:03:7F:2F:7F:F9' : 'wearable',
		   '2C:71:FF:76:4D:DE' : 'utility',
		   'EC:8A:C4:28:47:A1' : 'utility',
		   '00:F3:81:A1:DA:05' : 'utility',
		   '20:1F:3B:16:0C:04' : 'audio_video',
		   '14:22:3B:F1:47:98' : 'mobile_device',
		   '14:22:3B:F1:47:C5' : 'mobile_device',
		   '14:22:3B:F1:47:DD' : 'mobile_device',
		   '14:22:3B:F1:47:39' : 'mobile_device',
		   
		   '3A:9C:1D:94:AC:72' : 'mobile_device',
		   '86:B6:25:22:EB:20' : 'mobile_device',
		   '36:78:59:49:BB:4A' : 'mobile_device',
		   '2A:69:93:83:CF:F9' : 'mobile_device',
		   
		   '14:22:3B:F1:47:97' : 'mobile_device',
		   '14:22:3B:F1:47:C4' : 'mobile_device',
		   '14:22:3B:F1:47:DC' : 'mobile_device', 
		   '14:22:3B:F1:47:68' : 'mobile_device',
		   '58:24:29:67:AC:F4' : 'mobile_device',
		   '14:01:52:E3:B9:82' : 'mobile_device',
		   
		   'C0:06:C3:9B:D8:8C' : 'utility',
		   'C0:06:C3:9B:D3:26' : 'utility',
		   '48:A6:B8:FF:A6:3A' : 'audio_video',
		   '54:2A:1B:CC:58:3A' : 'audio_video',
		   'AC:84:C6:E3:3F:F4' : 'hub_gateway'}

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