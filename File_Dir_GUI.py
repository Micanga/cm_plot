# Interface Imports
import tkinter, MyGUICommons
from MyGUICommons import myPopUp
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font

# Protocol, Plots and utils imports
import Novonix_Protocol, BaSyTec_Protocol, Plot2d, utils, re
from Novonix_Protocol import *
from BaSyTec_Protocol import *
from Plot2d import *
from utils import *

class File_Dir_GUI:

	def __init__(self, master, prev_sc, main_bg, nb, bb):
		self.master = master

		self.start_log = 		"---------------------------------\n" + "| LOG SCREEN 1                  |\n" + "---------------------------------"
		self.novonix_txt = 		"| Novonix Action Pressed        |"
		self.basytec_txt = 		"| Basytec Action Pressed        |"
		self.xanes_txt = 		"| Xanes Action Pressed          |"
		self.file_button_txt = 	"| Button File Button Pressed    |"
		self.dir_button_txt = 	"| Directory File Button Pressed |"
		self.next_button_txt = 	"| Next button clicked           |"
		self.notfile =			"|--- File not selected         -|"
		self.notdir =			"|--- Dir not selected          -|"
		self.notcycle = 		"|--- Cycle not selected        -|"
		self.success = 			"|--- success                   -|"

		# 1. Oppening the imgs
		print(self.start_log)
		bg_img = tkinter.PhotoImage(file='img/screen1.png')
		file_button_img = tkinter.PhotoImage(file='img/file_button.png')
		dir_button_img = tkinter.PhotoImage(file='img/dir_button.png')
		selected_dir_img = tkinter.PhotoImage(file='img/selected_dir.png')
		next_button_img = tkinter.PhotoImage(file='img/next_button.png')

		# 2. Destroying the previous BackGround and Setting the new
		self.main_bg = main_bg
		self.main_bg.destroy()
		self.main_bg = tkinter.Label(master, image=bg_img)
		self.main_bg.image= bg_img
		self.main_bg.place(x=0,y=0,relwidth=1,relheight=1)
		if(nb is not None):
			self.next_button = nb
			self.next_button.destroy()
		if(bb is not None):
			self.back_button = nb
			self.back_button.destroy()
	
		# 3. Setting Functions
		# a. File Button
		self.file_button = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = self.file_button_click, image = file_button_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=53,width=137)
		self.file_button.image = file_button_img
		self.file_button.place(x = 285, y = 105)

		# b. Selected File Combo
		self.selected_file = tkinter.Listbox(master, selectmode='SINGLE', fg = 'white', font = 'courier 10', bg = "#%02x%02x%02x" % (30, 30, 30), 
									 highlightcolor = 'white', bd=0, height = 1, width = 58)
		self.selected_file.place(x = 130, y = 175)
		self.scrollbar = Scrollbar(master, orient="vertical")
		self.scrollbar.config(command=self.selected_file.yview)
		self.scrollbar.place(x = 115, y = 170)
		self.selected_file.config(yscrollcommand=self.scrollbar.set)
		self.vartext1 = StringVar()
		self.counter_file = tkinter.Label(master, anchor = 'n', compound = 'center', 
									textvariable = self.vartext1, fg = 'white',bg = "#%02x%02x%02x"% (30, 30, 30), 
									font = "courier 10 bold", borderwidth=0,padx=0,pady=0)
		self.counter_file.place(x = 600, y = 176)
		self.vartext1.set("("+str(self.selected_file.size())+")")

		# c. Dir Button
		self.dir_button = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = self.dir_button_click, image = dir_button_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=48,width=168)
		self.dir_button.image = dir_button_img
		self.dir_button.place(x = 278, y = 242)

		# d. Selected Dir Label
		self.vartext2 = StringVar()
		self.selected_dir = tkinter.Label(master, anchor = 'n', compound = 'center', 
									textvariable = self.vartext2, fg = 'white', image = selected_dir_img,
									font = "courier 10 bold italic", borderwidth=0,padx=0,pady=0)
		self.selected_dir.image = selected_dir_img
		self.selected_dir.place(x = 126, y = 299)
		self.vartext2.set("selected directory")

		# e. Next Button
		self.next_button = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = multFunc(self.next_button_click),image = next_button_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=29,width=35)
		self.next_button.image = next_button_img
		self.next_button.place(x= 595, y= 355)

		# i. Check Buttons
		self.novonix_var = IntVar()
		self.novonix = Checkbutton(master, variable= self.novonix_var, text = 'Novonix', command = self.novonix_on, onvalue= 1,
									bg = "#%02x%02x%02x" % (22, 27, 33), fg = 'green', font = 'courier 12 bold', borderwidth = 0, highlightthickness = 0)
		self.novonix.place(x = 200, y = 360)

		self.basytec_var = IntVar()
		self.basytec = Checkbutton(master, variable= self.basytec_var, text = 'BaSyTec', command = self.basytec_on, onvalue= 2,
									bg = "#%02x%02x%02x" % (22, 27, 33), fg = 'red', font = 'courier 12 bold', borderwidth = 0, highlightthickness = 0)
		self.basytec.place(x = 300, y = 360)

		self.xanes_var = IntVar()
		self.xanes = Checkbutton(master, variable= self.xanes_var, text = 'Xanes', command = self.xanes_on, onvalue= 3,
									bg = "#%02x%02x%02x" % (22, 27, 33), fg = 'orange', font = 'courier 12 bold', borderwidth = 0, highlightthickness = 0)
		self.xanes.place(x = 400, y = 360)

	def novonix_on(self):
		print(self.novonix_txt)
		self.basytec.deselect()
		self.xanes.deselect()

	def basytec_on(self):
		print(self.basytec_txt)
		self.novonix.deselect()
		self.xanes.deselect()

	def xanes_on(self):
		print(self.xanes_txt)
		self.novonix.deselect()
		self.basytec.deselect()
		
	def file_button_click(self):
		print(self.file_button_txt)
		self.filename = filedialog.askopenfilenames(initialdir = ".",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
		self.selected_file.delete(0,END)
		for fp in range(0,len(self.filename)):
			if(self.filename[fp] not in self.selected_file.get(0,END)):
				self.selected_file.insert(END, self.filename[fp])
		self.vartext1.set("("+str(self.selected_file.size())+")")

	def dir_button_click(self):
		print(self.dir_button_txt)
		self.dirname = filedialog.askdirectory()
		self.vartext2.set(self.dirname)

	def ableButtons(self):
		self.file_button.configure(state="normal")
		self.dir_button.configure(state= "normal")
		self.next_button.configure(state="normal")
		self.novonix.configure(state="normal")
		self.basytec.configure(state="normal")
		self.xanes.configure(state="normal")

	def disableButtons(self):
		self.file_button.configure(state="disabled")
		self.dir_button.configure(state="disabled")
		self.next_button.configure(state="disabled")
		self.novonix.configure(state="disabled")
		self.basytec.configure(state="disabled")
		self.xanes.configure(state="disabled")

	def destroyWidgets(self):
		self.file_button.grid_remove()
		self.selected_file.grid_remove()
		self.scrollbar.grid_remove()
		self.counter_file.grid_remove()
		self.dir_button.grid_remove()
		self.selected_dir.grid_remove()

	def next_button_click(self):
		print(self.next_button_txt)
		continue_flag = True

		if(self.selected_file.size() == 0):
			continue_flag = False
			self.disableButtons()
			missingfile = tkinter.PhotoImage(file='img/missingfile.png')
			myPopUp(self,' MISSING FILE!\n File is not selected. ',missingfile)
			print(self.notfile)

		elif(re.match("^\s*[selected directory]*\s*$",self.vartext2.get()) is not None):
			continue_flag = False
			self.disableButtons()
			missingdir = tkinter.PhotoImage(file='img/missingdir.png')
			myPopUp(self,' MISSING DIRECTORY!\n Directory is not selected. ',missingdir)
			print(self.notdir)

		elif(self.novonix_var.get() == 0 and self.basytec_var.get() == 0 and self.xanes_var.get() == 0):
			continue_flag = False
			self.disableButtons()
			myPopUp(self,' MISSING PROTOCOL!\n Define the Data Source of your Files ',None)
			print(self.notcycle)

		if(continue_flag is True):
			print(self.success)

			self.Plot_Files = self.selected_file.get(0,END)
			self.Plot_Destination = self.vartext2.get()
			self.Plot_Protocol = self.novonix_var.get() + self.basytec_var.get()+ self.xanes_var.get()

			self.destroyWidgets()

			from Plot_Info_GUI import Plot_Info_GUI
			Plot_Info_GUI(self.master,self,self.main_bg,self.next_button,None)