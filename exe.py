#!/usr/bin/env python
__author__ = 'Hiep Nguyen'
import os
import sys

try:               # Python 2.7x
    import Tkinter as tk
    import ttk
    import tkFont
    import tkMessageBox
    import tkFileDialog
    import tkSimpleDialog
    from ScrolledText import ScrolledText as tkScrolledText
except Exception:  # Python 3.x
    import tkinter as tk
    from tkinter import ttk
    import tkinter.font as tkFont
    import tkinter.messagebox as tkMessageBox
    import tkinter.filedialog as tkFileDialog
    import tkinter.simpledialog as tkSimpleDialog
    from tkinter.scrolledtext import ScrolledText as tkScrolledText

import numpy             as np
import matplotlib        as mpl
import matplotlib.pyplot as plt
import webbrowser

mpl.use("TkAgg")
from matplotlib.figure                 import Figure
from matplotlib.ticker                 import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from PIL                               import Image

# Webcam library
try:
    import cv2
    hasCV2 = True
except ImportError:
    hasCV2 = False

# Disable cv2 use on Mac OS because of buggy implementation
if sys.platform=="darwin":
    hasCV2 = False

# Modules
import calc as c




# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(tk.Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        tk.Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master         = master
        
        self.bg_colour      = '#ececec'
        self.txtfont        = 'TkFixedFont'
        self.array          = ''
        self.C              = 2.99792458e8 # m/s - speed of light
        self.uv_status      = False
        self.src_status     = False
        self.griduv_status  = False
        self.beam_status    = False
        self.src_fft_status = False

        # changing the title of our master widget      
        self.master.title('GUI - Miriad Imaging')
        
        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    





    #Creation of init_window
    def init_window(self):

        # Add a grid
        self.mainframe = ttk.Frame(self.master)
        self.mainframe.grid(row=0, column=0, sticky='NWES' )
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        self.mainframe.pack(side='left', fill='both', expand=True, pady = 10, padx = 10)

        # creating a menu instance
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)


        # 1. create the file object)
        file = tk.Menu(menu, tearoff=True)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label='Exit', command=self._exit)

        # add "file" to our menu
        menu.add_cascade(label='File', menu=file)

        



        # 2. Edit
        edit = tk.Menu(menu, tearoff=True)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label='Undo')

        #added "Edit" to our menu
        menu.add_cascade(label='Edit', menu=edit)



        

        # 3. mode for data reduction
        mode = tk.Menu(menu, tearoff=True)

        # adds a command to the menu 'mode'
        mode.add_command(label='Freebie' )
        mode.add_command(label='Continuum' )
        mode.add_command(label='Spectral line' )

        # add "Mode" to our menu
        menu.add_cascade(label='Mode', menu=mode)






        # Help
        help = tk.Menu(menu, tearoff=True)

        # adds a command to the menu option
        help.add_command(label='Guide',
            command=lambda filename='docs/HELP.txt',
            title='GUI - Miriad Imaging': self.show_textfile(filename, title) )

        #added "Help" to our menu
        menu.add_cascade(label='Help', menu=help)




        




        # Set the grid expansion properties
        self.mainframe.columnconfigure(0, weight=2)
        self.mainframe.columnconfigure(1, weight=2)
        self.mainframe.columnconfigure(2, weight=0)
        self.mainframe.columnconfigure(3, weight=0)
        self.mainframe.columnconfigure(4, weight=0)
        self.mainframe.columnconfigure(5, weight=0)
        self.mainframe.columnconfigure(6, weight=1)
        self.mainframe.columnconfigure(7, weight=1)
        self.mainframe.columnconfigure(8, weight=1)
        self.mainframe.columnconfigure(9, weight=1)

        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=9)




        # For command dropdown
        self.work = tk.StringVar(self.master)

        choices   = c.get_items('projects/', ext='')
        self.work.set(choices[0]) # set the default option

        xmenu    = tk.OptionMenu(self.mainframe, self.work, *choices, command=self.change_work)
        tk.Label(self.mainframe, text='Project').grid(row=0, column=0, padx=5, pady=2, sticky='EW')
        xmenu.grid(row=0, column=1, padx=5, pady=2, sticky='EW')







        # For command dropdown
        self.cmd = tk.StringVar(self.master)

        choices  = c.get_items('cmd/recommend/', ext='')
        self.cmd.set('atlod') # set the default option

        xmenu    = tk.OptionMenu(self.mainframe, self.cmd, *choices, command=self.change_cmd)
        tk.Label(self.mainframe, text='Command').grid(row=1, column=0, padx=5, pady=2, sticky='EW')
        xmenu.grid(row=1, column=1, padx=5, pady=2, sticky='EW')

        
        # Link for the command
        link = tk.Label(self.mainframe, text='Help '+self.cmd.get()+' (online)', fg='blue', cursor='hand2')
        link.bind("<Button-1>", lambda e: self.callback('https://www.atnf.csiro.au/computing/software/miriad/doc/'+self.cmd.get()+'.html') )
        link.grid(row=1, column=2, padx=5, pady=2, sticky='EW')


        # Text area: Recommend
        fstyle    = tkFont.Font(family='Calibri', size=13)
        args      = c.get_content( self.cmd.get(), self.work.get(), full=False )

        tk.Label(self.mainframe, text='Recommended cmd').grid(row=3, column=0, padx=5, pady=2, sticky='EW')
        self.text = tk.Text(self.mainframe, height=30, width=50, font=fstyle)
        self.text.insert(tk.END, args)
        self.text.grid(row=4, column=0, columnspan=2, padx=5, pady=2, sticky='EW')

        
        # Text area: FUll
        args      = c.get_content( self.cmd.get(), self.work.get(), full=True )
        tk.Label(self.mainframe, text='Full cmd').grid(row=3, column=3, padx=5, pady=2, sticky='EW')
        self.textf = tk.Text(self.mainframe, height=30, width=50, font=fstyle)
        self.textf.insert(tk.END, args)
        self.textf.grid(row=4, column=3, columnspan=2, padx=5, pady=2, sticky='EW')

        ## Go!
        tk.Button(self.mainframe, text='Go!', bg='lime', fg='black',
            command=self._run).grid(row=0, column=4, columnspan=1, padx=5, pady=2, sticky='EW')


        ## Exit
        tk.Button(self.mainframe, text='Exit', bg='red', fg='black',
            command=self._exit).grid(row=0, column=5, columnspan=1, padx=5, pady=2, sticky='EW')







    def _exit(self):
        exit()


    def _run(self):
        cmd = self.cmd.get()
        print('Running cmd: ' + self.cmd.get())
        kwargs = c.get_args( cmd, self.text.get("1.0", tk.END) )
        c.exe_cmd(cmd, kwargs)








    



    def show_textfile(self, filename, title=''):
        """Show a text file in a new window."""

        win = tk.Toplevel(background=self.bg_colour)
        win.title(title)
        txt = tkScrolledText(win, width=80, font=self.txtfont)
        txt.config(state="normal")
        with open(filename,'r') as f:
            text = f.read()
        txt.insert('1.0', text)
        txt.config(state="disabled")
        txt.grid(column=0, row=0, padx=5, pady=2, sticky="NSEW")
        xbtn = ttk.Button(win, text='Close',
                                   command=win.destroy)
        xbtn.grid(column=0, row=1, padx=5, pady=2, sticky="E")
        win.rowconfigure(0, weight=1)
        win.columnconfigure(0, weight=1)


    # on change dropdown value
    def change_cmd(self,value):
        self.text.delete('1.0', tk.END)
        args = c.get_content( self.cmd.get(), self.work.get() )
        self.text.insert(tk.END, args)


        self.textf.delete('1.0', tk.END)
        args = c.get_content( self.cmd.get(), self.work.get(), full=True )
        self.textf.insert(tk.END, args)

        link = tk.Label(self.mainframe, text="Help "+self.cmd.get(), fg="blue", cursor="hand2")
        link.bind("<Button-1>", lambda e: self.callback('https://www.atnf.csiro.au/computing/software/miriad/doc/'+self.cmd.get()+'.html') )
        link.grid(row=1, column=2, padx=5, pady=2, sticky='EW')


    # on change dropdown value
    def change_work(self,value):
        self.text.delete('1.0', tk.END)
        args = c.get_content( self.cmd.get(), self.work.get() )
        self.text.insert(tk.END, args)


    def callback(self,url):
        webbrowser.open_new(url)



# root window created. Here, that would be the haveonly window, but
# you can later have windows within windows.
root = tk.Tk()

# root.minsize(640, 100)
root.geometry('1400x680')
root.resizable(0, 0)

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  