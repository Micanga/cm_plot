import tkinter, utils
from tkinter import *
from tkinter import font
from tkinter import LEFT, RIGHT, BOTTOM, TOP, NONE
from tkinter import messagebox, filedialog, StringVar
from tkinter.font import Font
from utils import multFunc

def exit():
	print('Exit box thrown')
	if tkinter.messagebox.askyesno('Exit', 'Do you want to make more graphics??'):
		tkinter.messagebox.showinfo('Yes', 'Lets go!')
	else:
		tkinter.messagebox.showinfo('No', 'Thank you for using C&M app :)')
		quit()

def disable_event():
	pass
	
class myPopUp:

	def __init__(self,cur_screen,text,img):
		# 1. Initializing and configuring
		self.cur_popup = tkinter.Toplevel()
		sw = (self.cur_popup.winfo_screenwidth() - 700)/2
		sh = (self.cur_popup.winfo_screenheight() - 400)/2
		self.cur_popup.configure(bg= "#%02x%02x%02x" % (50, 60, 70))
		self.cur_popup.protocol("WM_DELETE_WINDOW", disable_event)
		self.cur_popup.resizable(width = False,height = False)
		self.cur_popup.geometry("+%d+%d" % (sw+175,sh+100))

		# 2. Writting the text
		self.pop_text = tkinter.Label(self.cur_popup, text = text, image = img, fg = 'white', anchor = 'center',
											font = "courier 12 bold italic", bg = "#%02x%02x%02x" % (50, 60, 70), 
											compound = 'left', borderwidth=0,padx=10,pady=10)
		self.pop_text.image = img
		self.pop_text.grid(row=0, column=0)
		
		# 3. Setting the OK button
		okbuttonimg = tkinter.PhotoImage(file='img/veiak.png')
		self.ok_button = Button(self.cur_popup, anchor = 'center', compound = 'center', 
										bg = "#%02x%02x%02x" % (50, 60, 70), fg = 'white',
										command = multFunc(cur_screen.ableButtons,self.cur_popup.destroy), image = okbuttonimg,
										highlightthickness = 0, activebackground = 'black',
										bd = 0, padx=5,pady=5,height=40,width=60)
		self.ok_button.image = okbuttonimg
		self.ok_button.grid(row=1, column=0)

		# 4. Settig the Final Space
		self.space = tkinter.Label(self.cur_popup, bg= "#%02x%02x%02x" % (50, 60, 70))
		self.space.grid(row=2,column=0)

class MyOptionMenu(OptionMenu):
    def __init__(self, master, status, *options):
        self.var = StringVar(master)
        self.var.set(status)
        OptionMenu.__init__(self, master, self.var, *options)
        self.config( font = 'courier 10',bg= "#%02x%02x%02x" % (30, 30, 30), fg = 'white', bd = 0, width=30)
        self['menu'].config(fg = 'white', font = 'courier 10', bg = "#%02x%02x%02x" % (30, 30, 30), bd=0)
