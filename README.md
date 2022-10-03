# ProtoFlow: Standard Agnostic Flow Table Tool Generation & Auxiliary tools
Flow metering tools for link-layer traffic on: Bluetooth, Zigbee, WiFi

## Known Issues:
1. Auto-detection of the protocol within the frame is defaulted to packet 0. In the event of malformed (or incomplete) packets, this can create a problem where it is not detected and not produce the table. 
Planned Fix: Find non-malformed packet to detect, or override via flag to force protocol choice.


All datasets are already in the CSV flow formats.

TODO: Relabel all CSV files into the abstract classes except for the ones under "ProtoFlow Originals", which are complete.
