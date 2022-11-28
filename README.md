Use this branch (playground_branch) if you want to mess around with the code, or anything else freely.

# ProtoFlow: Standard Agnostic Flow Table Tool Generation & Auxiliary tools
Flow metering tools for link-layer traffic on: Bluetooth, Zigbee, WiFi

## Known Issues:
1. Auto-detection of the protocol within the frame is defaulted to packet 0. In the event of malformed (or incomplete) packets, this can create a problem where it is not detected and not produce the table. 
Planned Fix: Find non-malformed packet to detect, or override via flag to force protocol choice.


All datasets are already in the CSV flow formats.

TODO: Relabel all CSV files into the abstract classes except for the ones under "ProtoFlow Originals", which are complete.


# How we approach the abstraction

Below is an example of device-to-class mappings for classification purposes.

Device | Class 
--- | --- | 
ASUS Router RT-N12 | router
ASUS RT-AC1200GE | router
August Smart Lock | smart_lock
Barnes & Noble Nook | ereader
Withings Blood Pressure monitor | smart_bp_monitor
Bose Home Speaker 300 | smart_speaker
C by GE 3-Wire On/Off Toggle | smart_switch
Echo W. Hub | smart_assistant
Fitbit 4 Health & Fitness Tracker | fitness_tracker
Galaxy A21 | smartphone
Garmin Index S2 Smart Scale | smart_scale
iRobot Roomba | smart_vacuum
Kindle | ereader
Kinsa Quickcare Smart Thermometer | smart_thermometer
PETKIT WiFi Feeder | smart_pet_feeder
Phillips Hue Bridge | smart_bridge
Pixel 4a | smartphone
Samsung Galaxy Watch Active | fitness_tracker
Dropcam | ip_camera
Insteon Camera | ip_camera
Netatomo Welcome | ip_camera
Samsung Smart Cam | ip_camera
TPlink Smart Cam | ip_camera
Withings Smart Baby Monitor | ip_camera
Macbook | laptop
Wemo Motion Sensor | motion_sensor
HP Printer | printer
Nest Smoke Alarm | smart_alarm
Blipcare Blood Pressure | smart_bp_monitor
LiFX Smart Bulb | smart_bulb
Pixstar Photo Frame | smart_frame
Smart Things Hub | smart_hub
TPlink Smart Plug | smart_plug
Withings Smart Scale | smart_scale
Echo | smart_speaker
iHome | smart_speaker
Triby Speaker | smart_speaker
Withings Aura Sleep Sensor | smart_speaker
Wemo Switch | smart_switch
Android Phone | smartphone
Iphone | smartphone
Samsung Galaxy Tab | tablet
Netatmo Weather Station | weather_station
Aria Smart Scale | smart_scale
Dlink Cam | ip_camera
Dlink Day Cam | ip_camera
Kasa Smart Plug | smart_plug
Samsung Smart TV | smart_tv
Facebook Portal | smart_display

Notes: Some of them are odd ducks (e.g., thermometer, bp monitor) as they don't have a greater class to belong to. In general, these abstractions can be anything as long as we have a clear umbrella for a large amount of these. For instance, we have multiple smartphones, routers, fitness trackers, etc.


