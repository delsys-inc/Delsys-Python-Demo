"""
Author: Chan
Last Edit: 3/2/2020

Summary:
This is the main function for the PythonDemo gui, this should be run for the main experience of the demo.

Known Limitations:

TODO:
"""

from PythonDemo import *

# THIS IS THE MAIN CODE THAT RUNS
def main():
    root = tk.Tk()
    root.geometry('800x750+0+0')
    app = Window(root)
    root.mainloop()

if __name__== "__main__":
    main()