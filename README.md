# meraki-automation-dns

This project main goal is to simplify modifying the DNS configuration of devices inside a Meraki network.  
It was made using Python 3.8, the Meraki API v1 release that can be found [here](https://github.com/meraki/dashboard-api-python), and you can install it via [PyPI](https://pypi.org/project/meraki/):

        pip install meraki
It also uses the 'ipaddress'  library for network checks:

        pip install ipaddress


**This script is still in development.**
## Features

The AutomationCore class contains functions that permits you to automatically modify the devices DNS configuration.
It will modify all the given network static IP devices DNS configuration.
It also checks if the provided DNS are valid IPV4 IP addresses.
this script also has a friendly-user interface to prevent errors.

**WARNING :**    
**Devices needs to be already claimed in the right network before being configured**

##Remaining tasks :
- Add whole organization DNS configuration modification feature.
- Add network static device primary DNS modification feature.
- Add network static device secondary DNS modification feature.
- Add modifying only specific list of devices inside a network feature.
- Make the automation async so there will be no UI freezing during work in progress.
- Give more visibility on what has been modified to the user after the automation completion
