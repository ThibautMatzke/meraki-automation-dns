import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk

import ipaddress

import automation.automation_core


class StartPage(tk.Frame):
    """

    The application starts by asking you to provide your api key, checks it and set it to the AutomationCore Application
    variable, and then redirects you to the Organization Page

    """

    invalid_api_key = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Setting background color
        self.config(background='#3a995b')

        # Setting my_tkinter_interface controller
        self.controller = controller

        # Project name
        self.label_title = tk.Label(self, text='Welcome to Meraki-automation-dns', font=('Roboto', 32), bg='#3a995b',
                                    fg='white')
        self.label_title.pack()

        # Asking for Dashboard API key
        self.label_instruction = tk.Label(self, text='Please enter your Meraki Dashboard API key to start :',
                                          font=('Roboto', 16),
                                          bg='#3a995b', fg='white')
        self.label_instruction.pack()

        # Api key input
        api_key_input = Entry(self, font=("Helvetica", 12), text='')
        api_key_input.pack()

        # validate api key button
        validate_api_key_button = Button(self, text="Validate", font=("Helvetica", 12), bg='white', fg='#3a995b',
                                         command=lambda: self.validate_api_key(api_key=api_key_input.get(),
                                                                               controller=controller))
        validate_api_key_button.pack(pady=10)

        # Error message if the API Key is invalid
        self.invalid_api_key = tk.Label(self, text='Your Meraki Dashboard API key is invalid, please retry',
                                        font=('Roboto', 18), bg='#3a995b',
                                        fg='red')

    def validate_api_key(self, api_key: str, controller):
        """
        This checks if the API is right by using automation class method 'set_working_api_key'.

        If the key is invalid, it packs the invalid_api_key label corresponding to an error message.

        If the key is valid, it initializes the 'automation' variable with the API key,
        but also initializes the combobox for the Organization Page
        It then switch to the Organization Page

        :param api_key: str
        :param controller:
        :return:
        """
        # Checks if the provided API key is correct & sets it
        if controller.automation.set_working_api_key(api_key=api_key):

            # If the error message for wrong API key is up, cleans it
            if self.invalid_api_key.winfo_ismapped():
                self.invalid_api_key.pack_forget()

            # Sets the combobox for the next page
            page = self.controller.get_page('OrganizationPage')
            page.init_combo_box_after_valid_api_key()

            # Switch to the Organization page
            controller.show_frame("OrganizationPage")

        # If the API key is incorrect
        else:
            # Displays the API key error message if not already displayed
            if not self.invalid_api_key.winfo_ismapped():
                self.invalid_api_key.pack()


class OrganizationPage(tk.Frame):
    """

    This page ask your which Organization you want to work with.

    """

    # ComboBox containing the different organizations user has access to
    # It will be initialized in the 'init_combo_box_after_valid_api_key' function
    combobox = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Setting background color
        self.config(background='#3a995b')

        # Setting my_tkinter_interface controller
        self.controller = controller

        # Organization page
        self.label_title = tk.Label(self, text='Organization choice', font=('Roboto', 32), bg='#3a995b',
                                    fg='white')
        self.label_title.pack()

        # Asking to choose the Organization
        self.label_instruction = tk.Label(self, text='Please choose your working Organization :',
                                          font=('Roboto', 16),
                                          bg='#3a995b', fg='white')
        self.label_instruction.pack()

        # validate organization button
        self.validate_organization_button = Button(self, text="Validate", font=("Helvetica", 12), bg='white',
                                                   fg='#3a995b',
                                                   command=lambda: self.validate_organization(self.combobox.get()))
        self.validate_organization_button.pack(pady=10)

    def init_combo_box_after_valid_api_key(self):
        """
        Initializes the comboBox containing the user accessible organizations

        :return:
        """
        self.combobox = ttk.Combobox(self, values=self.controller.automation.get_available_organizations_names_list(),
                                     width=40)
        # Display first element of the list
        self.combobox.current(0)
        self.combobox.pack()

    def validate_organization(self, organization_name):
        """
        Sets the working organization and then switch to the Network Page

        :param organization_name:
        :return:
        """
        # Sets the working organization with the organization name
        self.controller.automation.set_working_organization(organization_name=organization_name)

        # Initializes the Network page ComboBox variable
        page = self.controller.get_page('NetworkPage')
        page.init_combo_box_after_valid_organization()

        # Shows the Network Page
        self.controller.show_frame("NetworkPage")


class NetworkPage(tk.Frame):
    """

    This page ask you which network you want to work with

    """

    # ComboBox containing the different organizations user has access to
    # It will be initialized in the 'init_combo_box_after_valid_organization' function
    combobox = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Setting background color
        self.config(background='#3a995b')

        # Setting the frame controller
        self.controller = controller

        # Network page
        self.label_title = tk.Label(self, text='Network choice', font=('Roboto', 32), bg='#3a995b',
                                    fg='white')
        self.label_title.pack()

        # Asking to choose the Network
        self.label_instruction = tk.Label(self, text='Please choose your working Network :',
                                          font=('Roboto', 16),
                                          bg='#3a995b', fg='white')
        self.label_instruction.pack()

        # validate network button
        self.validate_network_button = Button(self, text="Validate", font=("Helvetica", 12), bg='white', fg='#3a995b',
                                              command=lambda: self.validate_network(self.combobox.get()))
        self.validate_network_button.pack(pady=10)

    def init_combo_box_after_valid_organization(self):
        """
        Initializes the comboBox containing the user accessible networks

        :return:
        """
        self.combobox = ttk.Combobox(self, values=self.controller.automation.get_available_networks_names_list(),
                                     width=40)
        # Display first element of the list
        self.combobox.current(0)
        self.combobox.pack()

    def validate_network(self, network_name):
        """
        Sets the working network and then switch to the Template Page

        :param network_name:
        :return:
        """
        # Sets the working network with the network name
        self.controller.automation.set_working_network(network_name=network_name)

        # Shows the Template Page
        self.controller.show_frame("DnsPage")


class DnsPage(tk.Frame):
    """

    This page makes you choose two DNS IP to modify an entire network device static DNS configuration.

    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Setting background color
        self.config(background='#3a995b')

        # Setting the frame controller
        self.controller = controller

        # DNS page
        self.label_title = tk.Label(self, text='DNS modification', font=('Roboto', 32), bg='#3a995b',
                                    fg='white')
        self.label_title.pack()

        # Asking to choose the DNS configuration
        self.label_instruction = tk.Label(self, text='Please input two DNS IP :',
                                          font=('Roboto', 16),
                                          bg='#3a995b', fg='white')
        self.label_instruction.pack()

        # DNS 1 label
        dns_one_label = Label(self, text='DNS 1 :',
                              font=('Roboto', 16),
                              bg='#3a995b', fg='white')
        dns_one_label.pack()

        # DNS 1 input
        dns_one_input = Entry(self, font=("Helvetica", 12))
        dns_one_input.pack()

        # DNS 2 label
        dns_two_label = Label(self, text='DNS 2 :',
                              font=('Roboto', 16),
                              bg='#3a995b', fg='white')
        dns_two_label.pack()

        # DNS 2
        dns_two_input = Entry(self, font=("Helvetica", 12))
        dns_two_input.pack()

        # Validate DNS button
        # Here we use for the button's command a different thread, so the frame doesn't freezes when the automation runs
        self.validate_dns_button = tk.Button(self, text="Validate DNS and launch automation",
                                             font=("Helvetica", 12),
                                             bg='white',
                                             fg='#3a995b',
                                             command=lambda:
                                             threading.Thread(target=self.validate_dns(dns_one_ip=dns_one_input.get(),
                                                                                       dns_two_ip=dns_two_input.get()))
                                             .start()
                                             )
        self.validate_dns_button.pack(pady=10)

        # Error message if DNS 1 isn't valid
        self.dns_one_invalid = tk.Label(self, text='First DNS is not valid, please correct it',
                                        font=('Roboto', 14), bg='#3a995b',
                                        fg='red')

        # Error message if DNS 2 isn't valid
        self.dns_two_invalid = tk.Label(self, text='Second DNS is not valid, please correct it',
                                        font=('Roboto', 14), bg='#3a995b',
                                        fg='red')

        # Validation message when both DNS are ok
        self.dns_both_valid = tk.Label(self, text='Both DNS are valid, automation started !',
                                        font=('Roboto', 14), bg='#3a995b',
                                        fg='white')

        # Work in progress label
        self.label_work_in_progress = tk.Label(self, text='Work in progress...',
                                               font=('Roboto', 14),
                                               bg='#3a995b', fg='white')
        # Done label
        self.label_done = tk.Label(self, text='Done ! Automation complete',
                                   font=('Roboto', 20),
                                   bg='#3a995b', fg='white')

    def validate_dns(self, dns_one_ip, dns_two_ip):
        """
        Checks if the DNS provided by the user are OK and then launches the automation.

        :param dns_one_ip:
        :param dns_two_ip:
        :return:
        """

        # Clears previous messages
        self.dns_one_invalid.pack_forget()
        self.dns_two_invalid.pack_forget()
        self.dns_both_valid.pack_forget()
        self.label_work_in_progress.pack_forget()
        self.label_done.pack_forget()

        # Checks if DNS IP are correct
        dns_one_valid = automation.automation_core.check_ip_validity(ip=dns_one_ip)
        dns_two_valid = automation.automation_core.check_ip_validity(ip=dns_two_ip)

        # If both DNS are OK
        if dns_one_valid and dns_two_valid:
            # Displays the validation message of both DNS
            self.dns_both_valid.pack()
            # Displays Work in progress label
            self.label_work_in_progress.pack()
            # Starts the automation
            self.controller.automation.update_network_static_devices_dns(dns_list=[dns_one_ip, dns_two_ip])
            # Displays the done message
            self.label_done.pack()

        # If DNS 1 is invalid
        elif not dns_one_valid:
            # Displays the DNS 1 error message
            self.dns_one_invalid.pack()

            # If DNS 2 is also invalid
            if not dns_two_valid:
                # Displays the DNS 2 error message
                self.dns_two_invalid.pack()

        # If only DNS 2 is invalid
        elif not dns_two_valid:
            # Displays the DNS 2 error message
            self.dns_two_invalid.pack()
