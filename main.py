# Tkinter Imports
import tkinter
from tkinter import *

# Main
if __name__ == "__main__":
	# 1. Starting root
	root = tkinter.Tk()

	# 2. Setting the commom features
	root.title('C&M')
	root.resizable(width = False,height = False)

	sw = (root.winfo_screenwidth() - 700)/2
	sh = (root.winfo_screenheight() - 400)/2

	root.geometry('%dx%d+%d+%d' % (700,400,sw,sh))
	root.protocol("WM_DELETE_WINDOW", sys.exit)

	root.grid_rowconfigure(0,pad=0)
	root.grid_columnconfigure(0,pad=0)
	root.grid_rowconfigure(1,pad=0)

	root.grid_columnconfigure(1,pad=0)

	#root.iconbitmap('@logo.xmb')

	# 3. Starting app
	main_bg_img = tkinter.PhotoImage(file='img/screen1.png')
	main_bg = tkinter.Label(root, image=main_bg_img)
	main_bg.place(x=0,y=0,relwidth=1,relheight=1)

	from File_Dir_GUI import File_Dir_GUI
	File_Dir_GUI(root,None,main_bg,None,None)
	root.mainloop()

	# 4. That's all folks :) ... 