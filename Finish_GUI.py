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


# Print Params Method
def printAllParams(self):
	print('Files:' + str(len(self.Plot_Files)))
	print('Destination: ' + self.Plot_Destination)
	print('Title: ' + self.Plot_Title)
	print('Precision: ' + self.Plot_Precision)
	print('Types: '+ str(self.Plot_XData) + str(self.Plot_YData))
	print('Cycle Type: ' + str(self.Plot_Cycle_Type))
	print('Cycles:')
	print(self.Plot_Cycle_Number)

"""
def showContacts(self):
	self.disableButtons()

	cur_popup = tkinter.Toplevel()
	cur_popup.configure(bg= "#%02x%02x%02x" % (50, 60, 70))
	cur_popup.overrideredirect(True)

	text1 = 'Dr. Alana Aragon Zulke\n'
	alana_text = tkinter.Label(cur_popup, text = text1, image = alana, fg = 'white', anchor = 'center',
										font = "courier 12 bold italic", bg = "#%02x%02x%02x" % (50, 60, 70), 
										compound = 'left', borderwidth=0,padx=10,pady=10)
	alana_text.grid(row=0, column=0,stick = 'w')

	text2 = 'Caio Ferreira Bernardo\n'
	caio_text = tkinter.Label(cur_popup, text = text2, image = caio, fg = 'white', anchor = 'center',
										font = "courier 12 bold italic", bg = "#%02x%02x%02x" % (50, 60, 70), 
										compound = 'left', borderwidth=0,padx=10,pady=10)
	caio_text.grid(row=1, column=0,stick = 'w')

	text3 = 'Matheus Aparecido do Carmo Alves\n'
	micanga_text = tkinter.Label(cur_popup, text = text3, image = micanga, fg = 'white', anchor = 'center',
										font = "courier 12 bold italic", bg = "#%02x%02x%02x" % (50, 60, 70), 
										compound = 'left', borderwidth=0,padx=10,pady=10)
	micanga_text.grid(row=2, column=0,stick = 'w')
		
	ok_button = Button(cur_popup, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (50, 60, 70), fg = 'white',
									command = multFunc(self.ableButtons,cur_popup.destroy), image = okbuttonimg,
									highlightthickness = 0, activebackground = 'black',
									bd = 0, padx=5,pady=5,height=40,width=60)
	ok_button.grid(row=3, column=0)

	space = tkinter.Label(cur_popup, bg= "#%02x%02x%02x" % (50, 60, 70))
	space.grid(row=4,column=0)

	print('> Contacts')
"""

class Finish_GUI:

	def __init__(self, master, prev_sc, main_bg, nb, bb):
		self.master = master

		self.start_log = 		 "---------------------------------\n" + "| LOG SCREEN 3                  |\n" + "---------------------------------"
		self.back_button_txt =   "| Back button clicked           |"
		self.finish_button_txt  ="| Finish button clicked         |"
		self.notcycle 			="|--- Cycle not selected        -|"
		self.charge_txt 		="| Charge button clicked         |"
		self.discharge_txt 		="| Discharge button clicked      |"
		self.full_txt 			="| Full button clicked           |"
		self.cycle_number		="|--- Cycle Number not selected -|"

		# 1. Saving the previous screen information
		self.Plot_Files = prev_sc.Plot_Files
		self.Plot_Destination = prev_sc.Plot_Destination
		self.Plot_Protocol = prev_sc.Plot_Protocol

		self.Plot_Title = prev_sc.Plot_Title
		self.Plot_Precision = prev_sc.Plot_Precision
		self.Plot_XData = prev_sc.Plot_XData
		self.Plot_YData = prev_sc.Plot_YData

		print('--- Title: %s\n--- Precision: %s\n--- XData: %s\n--- YData: %s' % (str(self.Plot_Title),str(self.Plot_Precision),str(self.Plot_XData),str(self.Plot_YData)))
		print(self.start_log)
		
		# 2. Oppening the imgs
		bg_img = tkinter.PhotoImage(file='img/screen3_1.png')
		contact_img = tkinter.PhotoImage(file='img/contact.png')
		back_button_img = tkinter.PhotoImage(file='img/back_button.png')
		finish_button_img = tkinter.PhotoImage(file='img/finish.png')

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


		# S. Formating the files
		if(self.Plot_Protocol == Plot_Protocol_Novonix):
			for n_file in range(0,len(self.Plot_Files)):
				Novonix_Protocol.format(self.Plot_Files[n_file],self.Plot_Precision)
		elif(self.Plot_Protocol == Plot_Protocol_BaSyTec):
			for n_file in range(0,len(self.Plot_Files)):
				print('BaSyTec format')
		elif(self.Plot_Protocol == Plot_Protocol_Xanes):
			for n_file in range(0,len(self.Plot_Files)):
				print('Xanes format')

		# 4. Setting the Functions
		# a. Check Buttons
		self.charge_var = IntVar()
		self.charge = Checkbutton(master, variable=self.charge_var, command = self.charge_on, onvalue= CHARGE_CYCLE,
									bg = "#%02x%02x%02x" % (40, 45, 55), borderwidth = 0, highlightthickness = 0)
		self.charge.place(x = 290, y = 140)

		self.discharge_var = IntVar()
		self.discharge = Checkbutton(master, variable=self.discharge_var, command = self.discharge_on, onvalue= DISCHARGE_CYCLE,
									bg = "#%02x%02x%02x" % (40, 45, 55), borderwidth = 0, highlightthickness = 0)
		self.discharge.place(x = 290, y = 180)

		self.full_var = IntVar()
		self.full = Checkbutton(master, variable=self.full_var, command = self.full_on, onvalue= FULL_CYCLE,
									bg = "#%02x%02x%02x" % (40, 45, 55), borderwidth = 0, highlightthickness = 0)
		self.full.place(x = 290, y = 220)

		# b. Contacts
		self.cont = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = None,image = contact_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=32,width=107)
		self.cont.image = contact_img
		self.cont.place(x= 296, y= 320)

		# c. Back
		self.back_button = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = self.back_button_click,image = back_button_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=28,width=48)
		self.back_button.image = back_button_img
		self.back_button.place(x= 535, y= 345)

		# d. Finish
		self.finish_button = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = self.finish_button_click,image = finish_button_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=24,width=49)
		self.finish_button.image = finish_button_img
		self.finish_button.place(x= 595, y= 348)

		# e. Cycle Select
		self.cs_scroll = Scrollbar(master,orient = tkinter.VERTICAL)
		self.cycle_select = Listbox(master,selectmode=tkinter.EXTENDED,yscrollcommand = self.cs_scroll.set,width = 5, height = 7)
		self.cs_scroll.config(command = self.cycle_select.yview,relief=tkinter.FLAT)
		if(self.Plot_Protocol == Plot_Protocol_Novonix):
			for n_file in range(0,len(self.Plot_Files)):
				newfilename = standard_formated_name(self.Plot_Files[n_file])

				file = fopen(newfilename,'r')
				file.readline()
				line = file.readline()
				cycle = 0
				while(re.match('^$', line ) is None):
					tokens = line.split(',')
					line = file.readline()
					if(abs(int(tokens[1])) > cycle):
						cycle = abs(int(tokens[1]))

				file.close()
		for i in range(1,cycle+1):
			self.cycle_select.insert(END,i)
		self.cycle_select.place(bordermode=tkinter.OUTSIDE,x= 483, y= 130,height=120,width=50)
		self.cs_scroll.place(bordermode=tkinter.OUTSIDE,x= 535, y= 130,height=120,width=15)

	def charge_on(self):
		print(self.charge_txt)
		self.discharge.deselect()
		self.full.deselect()

	def discharge_on(self):
		print(self.discharge_txt)
		self.charge.deselect()
		self.full.deselect()

	def full_on(self):
		print(self.full_txt)
		self.discharge.deselect()
		self.charge.deselect()

	def ableButtons(self):
		self.charge.configure(state="normal")
		self.discharge.configure(state="normal")
		self.full.configure(state="normal")
		#self.cont.configure(state="normal")
		self.back_button.configure(state="normal")
		self.finish_button.configure(state="normal")

	def disableButtons(self):
		self.charge.configure(state="disabled")
		self.discharge.configure(state="disabled")
		self.full.configure(state="disabled")
		#self.cont.configure(state="disabled")
		self.back_button.configure(state="disabled")
		self.finish_button.configure(state="disabled")

	def destroyWidgets(self):
		self.charge.grid_remove()
		self.discharge.grid_remove()
		self.full.grid_remove()
		#self.cont.grid_remove()
		self.back_button.grid_remove()

	def back_button_click(self):
		print(self.back_button_txt)
		self.destroyWidgets()

		from Plot_Info_GUI import Plot_Info_GUI
		Plot_Info_GUI(self.master,self,self.main_bg,self.finish_button,self.back_button)

	def finish_button_click(self):
		print(self.finish_button_txt)

		continue_flag = True
		if(self.charge_var.get() == 0 and self.discharge_var.get() == 0 and self.full_var.get() == 0):
			print(self.notcycle)
			continue_flag = False
			self.disableButtons()
			myPopUp(self,' MISSING CYCLE!\n Define a Cycle Type to your Plots. ',None)

		if(len(self.cycle_select.curselection()) == 0):
			print(self.cycle_number)
			continue_flag = False
			self.disableButtons()
			myPopUp(self,' MISSING CYCLES!\n Select the Cycles Numbers to your Plots. ',None)

		if(continue_flag is True):
			self.Plot_Cycle_Type = self.charge_var.get() + self.discharge_var.get()+ self.full_var.get()
			self.Plot_Cycle_Number = self.cycle_select.curselection()
			self.destroyWidgets()

			printAllParams(self)
			run(self)

			from Plot_Info_GUI import Plot_Info_GUI
			Plot_Info_GUI(self.master,self,self.main_bg,self.finish_button,self.back_button)



















class FinishR_GUI:

	def __init__(self, master, prev_sc, main_bg, nb, bb):
		self.master = master

		self.start_log = 		"---------------------------------\n" + "| LOG SCREEN 3                  |\n" + "---------------------------------"
		self.back_button_txt = 	"| Back button clicked           |"
		self.finish_button_txt ="| Finish button clicked         |"
		
		# 1. Saving the previous screen information
		self.Plot_Files = prev_sc.Plot_Files
		self.Plot_Destination = prev_sc.Plot_Destination
		self.Plot_Protocol = prev_sc.Plot_Protocol

		self.Plot_Title = prev_sc.Plot_Title
		self.Plot_Precision = prev_sc.Plot_Precision
		self.Plot_XData = prev_sc.Plot_XData
		self.Plot_YData = prev_sc.Plot_YData

		print('--- Title: %s\n--- Precision: %s\n--- XData: %s\n--- YData: %s' % (str(self.Plot_Title),str(self.Plot_Precision),str(self.Plot_XData),str(self.Plot_YData)))
		print(self.start_log)

		# 2. Oppening the imgs
		bg_img = tkinter.PhotoImage(file='img/screen3_3.png')
		contact_img = tkinter.PhotoImage(file='img/contact.png')
		back_button_img = tkinter.PhotoImage(file='img/back_button.png')
		finish_button_img = tkinter.PhotoImage(file='img/finish.png')

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

		# 4. Setting functions
		# a. Contacts
		self.cont = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = None,image = contact_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=32,width=107)
		self.cont.image = contact_img
		self.cont.place(x= 296, y= 320)

		# b. Back
		self.back_button = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = self.back_button_click,image = back_button_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=28,width=48)
		self.back_button.image = back_button_img
		self.back_button.place(x= 535, y= 345)

		# c. Finish
		self.finish_button = Button(master, anchor = 'center', compound = 'center', 
									bg = "#%02x%02x%02x" % (30, 30, 30), fg = 'white',
									command = self.finish_button_click,image = finish_button_img,
									highlightthickness = 0,
									bd = 0, padx=0,pady=0,height=24,width=49)
		self.finish_button.image = finish_button_img
		self.finish_button.place(x= 595, y= 348)

		# d. Cycle Select
		self.cs_scroll = Scrollbar(master,orient = tkinter.VERTICAL)
		self.cycle_select = Listbox(master,selectmode=tkinter.EXTENDED,yscrollcommand = self.cs_scroll.set,width = 5, height = 7)
		self.cs_scroll.config(command = self.cycle_select.yview,relief=tkinter.FLAT)
		if(self.Plot_Protocol == Plot_Protocol_Novonix):
			for n_file in range(0,len(self.Plot_Files)):
				newfilename = standard_formated_name(self.Plot_Files[n_file])

				file = fopen(newfilename,'r')
				file.readline()
				line = file.readline()
				cycle = 0
				while(re.match('^$', line ) is None):
					tokens = line.split(',')
					line = file.readline()
					if(abs(int(tokens[1])) > cycle):
						cycle = abs(int(tokens[1]))

				file.close()
		for i in range(1,cycle+1):
			self.cycle_select.insert(END,i)
		self.cycle_select.place(bordermode=tkinter.OUTSIDE,x= 483, y= 130,height=120,width=50)
		self.cs_scroll.place(bordermode=tkinter.OUTSIDE,x= 535, y= 130,height=120,width=15)


	def ableButtons(self):
		self.cont.configure(state="normal")
		self.back_button.configure(state="normal")
		self.finish_button.configure(state="normal")

	def disableButtons(self):
		self.cont.configure(state="disabled")
		self.back_button.configure(state="disabled")
		self.finish_button.configure(state="disabled")

	def destroyWidgets(self):
		self.cont.grid_remove()
		self.back_button.grid_remove()

	def back_button_click(self):
		print(self.back_button_click)
		self.destroyWidgets()

		from Plot_Info_GUI import Plot_Info_GUI
		Plot_Info_GUI(self.master,self,self.main_bg,self.finish_button,self.back_button)

	def finish_button_click(self):
		print(self.finish_button_txt)
		self.Plot_Cycle_Type = -1
		self.Plot_Cycle_Number = self.cycle_select.curselection()
		self.destroyWidgets()

		printAllParams(self)
		run(self)

		from Plot_Info_GUI import Plot_Info_GUI
		Plot_Info_GUI(self.master,self,self.main_bg,self.finish_button,self.back_button)