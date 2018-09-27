# Interface Imports
import tkinter, MyGUICommons, Defs
from MyGUICommons import *
from Defs import *
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font

# Protocol, Plots and utils imports
import Novonix_Protocol, Plot2d, utils, re
from Novonix_Protocol import *
from Plot2d import *
from utils import *

class Plot_Info_GUI:

	def __init__(self, master, prev_sc, main_bg, nb, bb):
		self.master = master

		self.start_log = 		"---------------------------------\n" + "| LOG SCREEN 2                  |\n" + "---------------------------------"
		self.back_button_txt = 	"| Back button clicked           |"
		self.next_button_txt = 	"| Next button clicked           |"
		self.nottitle =			"|--- Title not selected        -|"
		self.notprecision =		"|--- Precision not selected    -|"

		# 1. Saving the previous screen information
		self.Plot_Files = prev_sc.Plot_Files
		self.Plot_Destination = prev_sc.Plot_Destination
		self.Plot_Protocol = prev_sc.Plot_Protocol

		print('--- Files: %s\n--- Dir: %s\n--- Protocol: %s' % (str(self.Plot_Files),self.Plot_Destination,str(self.Plot_Protocol)))
		print(self.start_log)

		# 2. Oppening the imgs
		bg_img = tkinter.PhotoImage(file='img/screen2.png')
		back_button_img = tkinter.PhotoImage(file='img/back_button.png')
		next_button_img = tkinter.PhotoImage(file='img/next_button.png')

		# 3. Destroying the previous screen and setting the new
		self.main_bg = main_bg
		self.main_bg.destroy()
		self.main_bg = tkinter.Label(master, image=bg_img)
		self.main_bg.image = bg_img
		self.main_bg.place(x=0,y=0,relwidth=1,relheight=1)
		if(nb is not None):
			self.next_button = nb
			self.next_button.destroy()
		if(bb is not None):
			self.back_button = bb
			self.back_button.destroy()

		# 4. Setting the Functions
		# a. Plot Title
		self.title_entry = tkinter.Entry(master, fg = 'white', font = 'courier 10', bg = "#%02x%02x%02x" % (30, 30, 30), 
									insertbackground = 'white', highlightcolor = 'white', text = 'Title', bd=0, width = 40)
		self.title_entry.place(x = 300, y = 78)
		self.title_entry.insert(0,'Title')

		# b. Precision
		self.precision_entry = tkinter.Entry(master, fg = 'white', font = 'courier 10', bg = "#%02x%02x%02x" % (30, 30, 30), 
									insertbackground = 'white', highlightcolor = 'white', text = '0.0001', bd=0, width = 40)
		self.precision_entry.place(x = 300, y = 125)
		self.precision_entry.insert(0,'0.0001')

		# c. X Y Y
		self.x_menu = MyOptionMenu(master,Novonix_Table[0],*Novonix_Table)
		self.x_menu.place(x = 300, y = 165)

		self.y_menu = MyOptionMenu(master,Novonix_Table[1],*Novonix_Table)
		self.y_menu.place(x = 300, y = 210)

		# d. Next and Back 
		self.back_button = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = multFunc(self.back_button_click),image = back_button_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=28,width=48)
		self.back_button.image = back_button_img
		self.back_button.place(x= 535, y= 345)

		self.next_button = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = multFunc(self.next_button_click),image = next_button_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=29,width=39)
		self.next_button.image = next_button_img
		self.next_button.place(x= 595, y= 345)

	def ableButtons(self):
		self.title_entry.configure(state="normal")
		self.precision_entry.configure(state="normal")
		self.x_menu.configure(state="normal")
		self.y_menu.configure(state="normal")
		self.next_button.configure(state="normal")
		self.back_button.configure(state="normal")

	def disableButtons(self):
		self.title_entry.configure(state="disabled")
		self.precision_entry.configure(state="disabled")
		self.x_menu.configure(state="disabled")
		self.y_menu.configure(state="disabled")
		self.next_button.configure(state="disabled")
		self.back_button.configure(state="disabled")

	def destroyWidgets(self):
		self.title_entry.delete(0, END)
		self.title_entry.grid_remove()
		self.precision_entry.grid_remove()
		self.precision_entry.delete(0, END)
		self.x_menu.grid_remove()
		self.y_menu.grid_remove()
		self.next_button.grid_remove()
		self.back_button.grid_remove()

	def back_button_click(self):
		print(self.back_button_txt)
		self.destroyWidgets()

		from File_Dir_GUI import File_Dir_GUI
		File_Dir_GUI(self.master,self,self.main_bg,self.next_button,self.back_button)

	def next_button_click(self):
		print(self.next_button_txt)
		continue_flag = True
		if(re.match("^\s*$",self.title_entry.get()) is not None):
			print(self.nottitle)
			continue_flag = False
			self.disableButtons()
			myPopUp(self,' MISSING TITLE!\n Define a Title to your Plots. ',None)
		elif(re.match("^\s*\d+[.]\d+\s*$",self.precision_entry.get()) is None):
			print(self.notprecision)
			continue_flag = False
			self.disableButtons()
			myPopUp(self,' MISSING PRECISION!\n Set the precision to your Plots.\nFormat ex.: \"0.0001\" ',None)

		if(continue_flag is True):
			self.Plot_Title = self.title_entry.get()
			self.Plot_Precision = self.precision_entry.get()
			self.Plot_XData = Novonix_Table.index(self.x_menu.var.get())
			self.Plot_YData = Novonix_Table.index(self.y_menu.var.get())
			self.destroyWidgets()

			from Finish_GUI import Finish_GUI, FinishR_GUI
			if(self.Plot_XData not in [COULUMBIC-4,DVA-4] and self.Plot_YData not in [COULUMBIC-4,DVA-4]):
				Finish_GUI(self.master,self,self.main_bg,self.next_button,self.back_button)
			else:
				FinishR_GUI(self.master,self,self.main_bg,self.next_button,self.back_button)