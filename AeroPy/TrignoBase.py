"""
This class creates an instance of the Trigno base. Put in your key and license here
"""
import clr
clr.AddReference("/resources/DelsysApi")
clr.AddReference("System.Collections")


from Aero import AeroPy


key = ""
license = ""

class TrignoBase():
    def __init__(self):
        self.BaseInstance = AeroPy()