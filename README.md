# meraki-automation-dns

This project main goal is to simplify modifying the DNS configuration of devices inside a Meraki network.

## Installation

### Clone the repository

    git clone https://github.com/ThibautMatzke/meraki-automation-dns

### Install the requirements

It was made using Python 3.8, the Meraki API v1 release that can be found [here](https://github.com/meraki/dashboard-api-python), and you can install it via [PyPI](https://pypi.org/project/meraki/):

        pip install meraki
It also uses the 'ipaddress'  library for network checks:

        pip install ipaddress

You can also directly install all the requirements by using the following command inside project folder :

    pip install -r requirements.txt

## How to use

Simply launch the main.py file that will bring up the user-friendly interface.

        python main.py

Then, follow the instructions.

**Remember, this script is still under development.**
## Features

The AutomationCore class contains functions that permits you to automatically modify the devices DNS configuration.
It will modify all the given network static IP devices DNS configuration.
It also checks if the provided DNS are valid IPV4 IP addresses.
This script also has a friendly-user interface to prevent errors.

**This was tested & worked on MX & MR devices. It should work on any static IP device with a WAN1 interface, but it hasn't been tested yet.**


**WARNING :**    
**Devices needs to be already claimed in the right network before being configured**


## Remaining tasks :
- Add whole organization DNS configuration modification feature.
- Add network static device primary DNS modification feature.
- Add network static device secondary DNS modification feature.
- Add modifying only specific list of devices inside a network feature.
- Make the automation async so there will be no UI freezing during work in progress.
- Give more visibility on what has been modified to the user after the automation completion
