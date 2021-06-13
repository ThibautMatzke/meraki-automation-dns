import tkinter as tk
from tkinter import *
from automation import automation_core
from my_tkinter_interface import pages


class ProjectApp(tk.Tk):
    """

    This class goal is to provide a user-friendly interface for this script.
    This one also contains the possibility to choose & set the working Organization ID & Network ID

    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Meraki-automation-api-V1')
        self.minsize(480, 360)
        self.geometry("800x600")
        # Setting background color
        self.config(background='#3a995b')

        # The AutomationCore variable used in all pages
        self.automation = automation_core.AutomationCore()

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        container = tk.Frame(self)
        container.pack(expand=YES)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (pages.StartPage, pages.OrganizationPage,
                  pages.NetworkPage, pages.DnsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # Shows the starting application page
        self.show_frame("StartPage")

    def show_frame(self, page_name: str):
        """
         Show a frame for the given page name

        :param page_name: str
        :return:
        """
        frame = self.get_page(page_name)
        frame.tkraise()

    def get_page(self, page_name: str) -> tk.Frame:
        """
        Get a page, permitting pages to interact between each other

        :param page_name: str
        :return:
        """
        return self.frames[page_name]


if __name__ == "__main__":
    app = ProjectApp()
    app.mainloop()
