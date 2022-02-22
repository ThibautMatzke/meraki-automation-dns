import ipaddress
import meraki


def check_ip_validity(ip: str) -> bool:
    """
    Checks if the provided IP is a valid IPV4 IP.

    :param ip:
    :return:
    """

    # Checks if there is a value
    if ip:
        try:
            # Checks if it is a valid IPV4 address
            ipaddress.IPv4Address(ip)

        # If not, catches the exception
        except ipaddress.AddressValueError:

            # And return false
            return False

        # If the IP address is valid, returns true
        return True

    # If no IP was given
    return False


class AutomationCore:
    """
    **This class was made to automate Meraki devices configuration**
    It uses the "meraki" python library V1

    It contains multiple functions permitting to easily change a network device's DNS IP.

    ...

    Attributes
    ----------
    _dashboard : DashboardAPI
        the dashboardAPI that enables the program to request the Meraki Dashboard.

    _org_id : str (private)
        The Meraki organization ID where the targeted devices are.
        It needs to be set by using the "set_working_organization" method before using specific org-related functions

    _network_id : str (private)
        The Meraki network ID that will be used by the class methods.
        It needs to be set by using the "set_working_network" method before using specific network-related functions

    _wan1 : dict (private)
        The Wan1 object is a dict() python variable.
        It contains the network information that will be used to configure the device management interface.


    """

    def __init__(self):
        self._dashboard = None
        self._org_id = ''
        self._network_id = ''
        self._wan1 = dict(usingStaticIp=True,
                          staticIp='',
                          staticSubnetMask='',
                          staticGatewayIp='',
                          staticDns=['', ''],
                          vlan=None)

    def set_working_api_key(self, api_key: str):
        """
        This method first checks your Meraki Dashboard API key and if it is correct, it will set it and return True.
        If the key is incorrect, it will return False.
        Using this function is mandatory before using other functions.
        Since meraki.myorgaccess doesn't exist anymore, it tries a function to test out the key.

        :param api_key:
        :return:
        """
        # Creates a persistent Meraki Dashboard API session with the given api_key

        try:

            # Tries a function to see if the API Key is valid
            self._dashboard = meraki.DashboardAPI(api_key=api_key)

            # Return true the key is valid
            return True

        # Catches the error if the API Key isn't valid
        except meraki.APIKeyError as e:

            # Prints the error message
            print(e)

            # Returns false if the key is invalid
            return False

    def set_working_organization(self, organization_name: str):
        """
            Sets the organization ID that will be used by the program by using the network name.
            You don't have to put the entire organization name, just a part of it.

        :param organization_name: name of the network
        :return:
        """
        try:
            # Gets all the organizations information related to the current api_key in a list
            user_organizations = self._dashboard.organizations.getOrganizations()

            # Iterates on each element of the list
            for row in user_organizations:

                # Checks if the current organization name match the given one
                if organization_name in row['name']:
                    # If yes, sets its self.org_id with it
                    self._org_id = row['id']

            # If at the end, no organization with the given name was found, it raises an Value Error
            if self._org_id == '':
                raise ValueError
        except ValueError:
            print('Cannot find that organization, please retry with a existing organization name')

    def set_working_network(self, network_name: str):
        """
            Sets the network ID that will be used by the program by using the network name.
            You don't have to put the entire network name, just a part of it.

        :param network_name: name of the network
        :return:
        """

        # Gets all the networks information related to the previously set org_id in a list.
        organization_networks = self._dashboard.organizations.getOrganizationNetworks(self._org_id)

        try:
            # Iterates on each element of the list
            for row in organization_networks:

                # Checks if the current network name match the given one
                if network_name in row['name']:
                    # If yes, sets its self.org_id with it
                    self._network_id = row['id']

            # If at the end, no network with the given name was found, it raises an Value Error
            if self._network_id == '':
                raise ValueError
        except ValueError:
            print('Cannot find that network, please retry with an existing network name')

    def get_available_organizations_names_list(self):
        """
        Returns the user accessible organizations names.

        :return: organizations_names
        """

        # Gets all the organizations information related to the current api_key in a list
        user_organizations = self._dashboard.organizations.getOrganizations()

        # Initialises the return list containing all available organizations
        organizations_names = []

        # Iterates on each element of the list
        for row in user_organizations:
            # For each element of the list, it adds the value 'name' inside of the return list
            organizations_names.append(row['name'])

        # Returns the list containing all organizations names.
        return organizations_names

    def get_available_networks_names_list(self):
        """
        Returns the user accessible networks names.

        :return: networks_names
        """
        # Gets all the networks information related to the current api_key in a list
        user_networks = self._dashboard.organizations.getOrganizationNetworks(self._org_id)

        # Initialises the return list containing all available networks
        networks_names = []

        # Iterates on each element of the list
        for row in user_networks:
            # For each element of the list, it adds the value 'name' inside of the return list
            networks_names.append(row['name'])

        # Returns the list containing all networks names.
        return networks_names

    def check_organization_device_serial_number(self, serial_number: str) -> bool:
        """
        Checks if the serial number provided is present in the current working organization inventory

        :param serial_number: device serial number
        :return:
        """
        org_inventory = self._dashboard.organizations.getOrganizationInventory(self._org_id, total_pages=-1)
        for row in org_inventory:
            if row['serial'] == serial_number:
                return True
        return False

    def check_network_device_serial_number(self, serial_number: str) -> bool:
        """
        Checks if the serial number provided is present in the current working network inventory

        :param serial_number: device serial number
        :return:
        """
        org_inventory = self._dashboard.networks.getNetworkDevices(networkId=self._network_id)
        for row in org_inventory:
            if row['serial'] == serial_number:
                return True
        return False

    def update_device_primary_dns(self, serial_number: str, primary_dns: str):
        """
        Updates the device's primary DNS IP. This is only for the WAN1 interface.

        :param serial_number: device serial number
        :param primary_dns: primary DNS IP
        :return:
        """

        # Get the current device management interface configuration for WAN1 and saves it in wan1
        self._wan1 = (self._dashboard.devices.getDeviceManagementInterface(serial=serial_number))['wan1']

        # Changes the wan1 primary DNS IP
        self._wan1['staticDns'][0] = primary_dns

        # Update the device management interface with the new DNS IP
        self._dashboard.devices.updateDeviceManagementInterface(serial=serial_number, wan1=self._wan1)

    def update_device_secondary_dns(self, serial_number: str, secondary_dns: str):
        """
        Updates the device's secondary DNS IP. This is only for the WAN1 interface.

        :param serial_number: device serial number
        :param secondary_dns: secondary DNS IP
        :return:
        """

        # Get the current device management interface configuration for WAN1 and saves it in wan1
        self._wan1 = (self._dashboard.devices.getDeviceManagementInterface(serial=serial_number))['wan1']

        # Changes the wan1 secondary DNS IP
        self._wan1['staticDns'][0] = secondary_dns

        # Update the device management interface with the new DNS IP
        self._dashboard.devices.updateDeviceManagementInterface(serial=serial_number, wan1=self._wan1)

    def update_device_dns(self, serial_number: str, dns_list: list):
        """
        Updates the device's primary and secondary DNS IP. This is only for the WAN1 interface.

        :param serial_number: device serial number
        :param dns_list: list containing primary and secondary DNS IP. index 0 corresponds to primary DNS.
        :return:
        """
        # Get the current device management interface configuration for WAN1 and saves it in wan1
        self._wan1 = (self._dashboard.devices.getDeviceManagementInterface(serial=serial_number))['wan1']

        # Changes the wan1 primary and secondary DNS
        self._wan1['staticDns'] = dns_list

        # Update the device management interface with the new DNS IP
        self._dashboard.devices.updateDeviceManagementInterface(serial=serial_number, wan1=self._wan1)

    def update_network_static_devices_primary_dns(self, primary_dns: str):
        """
        Updates the entire currently-working network static devices primary DNS configuration.
        This will only apply on devices using static IP.

        :param primary_dns: primary DNS IP
        :return:
        """

        # Get all static IP devices serial number in the network
        static_devices = self.get_network_devices_static()

        # Iterates on the list
        for serial_number in static_devices:
            # Modify primary DNS
            self.update_device_primary_dns(serial_number=serial_number, primary_dns=primary_dns)

    def update_network_static_devices_secondary_dns(self, secondary_dns: str):
        """
        Updates the entire currently-working network static devices secondary DNS configuration.
        This will only apply on devices using static IP.

        :param secondary_dns: secondary DNS IP
        :return:
        """

        # Get all static IP devices serial number in the network
        static_devices = self.get_network_devices_static()

        # Iterates on the list
        for serial_number in static_devices:
            # Modify secondary DNS
            self.update_device_secondary_dns(serial_number=serial_number, secondary_dns=secondary_dns)

    def update_network_static_devices_dns(self, dns_list: list):
        """
        Updates the entire currently-working network static devices DNS.

        :param dns_list: list containing primary and secondary DNS IP. index 0 corresponds to primary DNS.
        :return:
        """
        # Get all static IP devices serial number in the network
        static_devices = self.get_network_devices_static()

        # Iterates on the list
        for serial_number in static_devices:
            # Modify DNS
            self.update_device_dns(serial_number=serial_number, dns_list=dns_list)

    def check_device_static(self, serial_number: str) -> bool:
        """
        Checks if a device is in static IP configuration. Returns true if yes, false if no

        :param serial_number: device serial number
        :return:
        """

        return (self._dashboard.devices.getDeviceManagementInterface(serial=serial_number))['wan1']['usingStaticIp']

    def get_network_devices_static(self) -> list:
        """
        Retrieve all devices that have static IP configuration in the currently-working network

        :return: list of network devices serial number in static IP
        """

        # Retrieve all network devices
        devices_list = self._dashboard.networks.getNetworkDevices(networkId=self._network_id)

        # Creates the return list
        static_devices_sn_list = []

        # Iterates on each devices_list elements
        for device in devices_list:
            # Check if the device is in static IP
            if self.check_device_static(device['serial']):
                # Adds it to the list
                static_devices_sn_list.append(device['serial'])

        # Returns the static IP devices contained in this network
        return static_devices_sn_list
