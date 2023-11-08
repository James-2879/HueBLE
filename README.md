# Hue Beacon

https://github.com/James-2879/HueBLE

## Overview

This code aims to control Philips Hue lights based on proximity of a BLE transmitter to a BT receiver.
The idea is that the transmitter is on-person, which is accommodated for by the small form factors of BLE devices.

I am unable to provide a list of compatible devices, but they may include phones, smartwatches, smart rings... _creativity is required :) !_

_Tested on Windows 11, partially on Ubuntu 22.04 LTS._

### DISCLAIMER

_This code is provided free of charge, 'as is', and with no warranty, and I accept no responsibility for adverse events derived from, or related to, the use of this code._
_I have tested the code to the best of my techincal knowledge, but I cannot guarantee that bugs will not exist._
_I also cannot anticipate issues which may arise from updates to dependencies, nor can I predict how the code may affect (or be affected by) a user's specific environment._

Feel free to fork or contribute.

## Usage

1. Install dependencies.

    ```
    pip install -r requirements.txt
    ```

2. Modify the 'User Config' section of the script; for minimum operation you will need to know:

    - Bridge IP address.
    - Transmitter MAC address.

3. Run (from terminal).

    ```
    python3 hue_beacon.py
    ```

In future releases, this process will likely be automated.


## Future development

- Automated discovery of bridge and BLE transmitters.
- Websockets to add support for multiple receivers.
- Triangulation between receivers (maybe).
- Support for multiple transmitters and unique actions per transmitter.
- Training option to discover best RSSI cutoff.
