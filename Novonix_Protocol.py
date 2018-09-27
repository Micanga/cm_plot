import os, re, pathlib, Defs
from Defs import *
from pathlib import Path
from utils import *

Novonix_Table = ["Time (Data Colect Point)","Current (A)","Potential (V)","Capacity (Ah)","Temperature (C)","Circuit Temperature (C)","Coulombic Efficiency (Fg-1)/(Cycle number)","Differential Voltage Analysis (A/V)"]

CURRENT      = 5
POTENTIAL    = 6
CAPACITY     = 7
TEMPERATURE  = 8
CIRCUIT_TEMP = 9
COULUMBIC 	 = 10
DVA 		 = 11

def standard_formated_name(filename):
	part = filename.rpartition('/')
	if(os.path.isdir(part[0] + "/form") == False):
		os.mkdir(part[0] + "/form")
	return part[0] + '/form/formated' + part[len(part)-1]

def format(filename,prec):
	print('checking if this file is already formated: ')
	if(Path(standard_formated_name(filename)).exists()):
		print('file already exists.')
		return(None)

	print('starting format: total steps: 5')
	# 0. Verifying the precision
	precision = 0.0001
	print('setting precision')
	if(re.match('^\s*$', prec ) is None):
		precision = float(prec)
	print('precision set')

	# 1. Opening the original file
	print('1: ',end="")
	file = fopen(filename,'r')
	print('|||||||||| 100%')

	# 2. Removing the protocol information
	print('2: ',end="")
	line = file.readline()
	while(re.match('^\s*\[Data\]', line ) is None):
		line = file.readline()
	print('|||||||||| 100%')

	# 3. Creating a new file
	# a. opening a new file
	print('3: ',end="")
	newfile = open(standard_formated_name(filename),'w')
	print('||',end="")

	# b. writing the header
	newfile.write(file.readline())
	print('||',end="")

	# c. writing the data to update the cycle numbering
	print('||',end="")
	cycle, tendency, prev_v = 1, 1, INF
	line = file.readline()

	while(re.match('^$', line ) is None):
		# i. split the data information
		tokens = line.split(',')

		# ii. analysing if the battery is discharging
		if(abs(float(tokens[6]) - prev_v) > float(precision)):
			if(float(tokens[6]) - prev_v > 0 and tendency < 0):
				cycle = abs(cycle) + 1
				tendency = float(tokens[6]) - prev_v
			elif(float(tokens[6]) - prev_v < 0 and tendency > 0):
				cycle = cycle * (-1)
				tendency = float(tokens[6]) - prev_v


		# iii. writing the updated data
		prev_v = float(tokens[6])
		line = str(cycle)
		tokens[1] = line 
		newfile.write(','.join(tokens))
		line = file.readline()	

	print('|||| 100%')	

	# 4. Closing the opened files
	print('4: ',end="")
	file.close()
	print('|||||',end="")
	newfile.close()
	print('||||| 100%')

	# 5. That`s all folks :) ...
	print('5: |||||||||| 100%')
