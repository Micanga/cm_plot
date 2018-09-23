# Protocol, Plots and utils imports
import MyGUICommons, Novonix_Protocol, BaSyTec_Protocol, Defs, utils, re, csv, numpy, matplotlib.pyplot, scipy.interpolate
from MyGUICommons import exit
from Novonix_Protocol import *
from BaSyTec_Protocol import *
from Defs import *
from scipy.interpolate import spline
from utils import *

# Run Method
def run(info):
	# 1. Formating the files
	if(info.Plot_Protocol == Plot_Protocol_Novonix):
		for n_file in range(0,len(info.Plot_Files)):
			format(info.Plot_Files[n_file],info.Plot_Precision)
	elif(info.Plot_Protocol == Plot_Protocol_BaSyTec):
		for n_file in range(0,len(info.Plot_Files)):
			print('BaSyTec format')
	elif(info.Plot_Protocol == Plot_Protocol_Xanes):
		for n_file in range(0,len(info.Plot_Files)):
			print('Xanes format')


	# 2. Plotting
	if(info.Plot_Protocol == Plot_Protocol_Novonix):
		for n_file in range(0,len(info.Plot_Files)):
			newfilename = standard_formated_name(info.Plot_Files[n_file])
			Plot2d().plot(newfilename,info.Plot_Destination,info.Plot_XData+4,info.Plot_YData+4,info.Plot_Cycle,
							info.Plot_Title,Novonix_Table[info.Plot_XData],Novonix_Table[info.Plot_YData],True)
			#else:
			#	Plot2d().plot2y()

	elif(info.Plot_Protocol == Plot_Protocol_BaSyTec):
		print("BaSyTec")
	elif(info.Plot_Protocol == Plot_Protocol_Xanes):
		print("Xanes")

	# 3. That's all folks :) ...
	exit()



















class Plot2d():

	def __plotColumbic__(self,file,dest,col,plottitle,plotx,ploty):
		print('Columbic')
		# 1. Setting plot labels and retrieving the csv information
		print('3: ',end="")
		matplotlib.pyplot.title(plottitle)
		print('|||',end="")
		matplotlib.pyplot.xlabel(plotx)
		print('||||',end="")
		matplotlib.pyplot.ylabel(ploty)
		print('||| 100%')
		
		charge, discharge = [], []
		information = []
		cycle = 1

		# 5. Plotting
		print('4: Plotting... total estimate time: 15s')
		line = file.readline()
		matplotlib.interactive(True)

		while(re.match('^$', line ) is None):
			# a. tokenizing line
			tokens = line.split(',')

			while(re.match('^$', line ) is None and cycle == -int(tokens[1])):
				# b. storing the information
				value = float(tokens[col])

				if(int(tokens[1]) < 0 and value != 0):
					discharge.append(value)

				# c. reading the new line
				line = file.readline()
				tokens = line.split(',')

			cycle = cycle + 1

			while(re.match('^$', line ) is None and cycle == int(tokens[1])):
				# b. storing the information
				value = float(tokens[col])

				if(int(tokens[1]) > 0):
					charge.append(value)

				# c. reading the new line
				line = file.readline()
				tokens = line.split(',')

			# d. incrementing the cycle
			if(len(discharge) > 1 and len(charge) > 1 and (max(discharge)-min(discharge)) != 0):	
				information.append(((max(charge)-min(charge))/(max(discharge)-min(discharge)))*100)

			charge, discharge = [], []

		print(dest + '/' + plottitle + '.png')
		matplotlib.pyplot.plot(information,'-')

		# 6 . Closing the opened file
		matplotlib.pyplot.show()
		print('5: |||||||||| 100%')
		file.close()

		# 7. Thats all folks :) ...
		print('6: |||||||||| 100%')
		



















	def __smooth__(self, a, WSZ):
    # a: NumPy 1-D array containing the data to be smoothed
    # WSZ: smoothing window size needs, which must be odd number,
    # as in the original MATLAB implementation
		out0 = numpy.convolve(a,numpy.ones(WSZ,dtype=int),'valid')/WSZ    
		r = numpy.arange(1,WSZ-1,2)
		start = numpy.cumsum(a[:WSZ-1])[::2]/r
		stop = (numpy.cumsum(a[:-WSZ:-1])[::2]/r)[::-1]
		return numpy.concatenate((  start , out0, stop  ))

	def __plotDVA__(self,file,dest,plottitle,plotx_title,ploty_title):
		print('DVA')
		cycle_test = 1
		
		# 1. Setting plot labels and retrieving the csv information
		print('3: ',end="")
		matplotlib.pyplot.title(plottitle)
		print('|||',end="")
		matplotlib.pyplot.xlabel(plotx_title)
		print('||||',end="")
		matplotlib.pyplot.ylabel(ploty_title)
		print('||| 100%')
		
		Q = []
		V = []
		dQdV = []
		cycle, cur_file = 1, 1

		# 2. Plotting
		print('4: Plotting... total estimate time: 15s')
		line = file.readline()
		matplotlib.interactive(True)
		matplotlib.pyplot.figure(cur_file)
		
	

		while(re.match('^$', line ) is None):
			# a. tokenizing line
			tokens = line.split(',')

			while(re.match('^$', line ) is None and cycle == abs(int(tokens[1]))):
				# b. storing the information
				valueQ = float(tokens[7]) #capacitancia
				valueV = float(tokens[6]) #potencial

				
				if((-1)*int(tokens[1]) > 0 and valueQ != 0 and valueV != 0):
					Q.append(valueQ)
					V.append(valueV)

				# c. reading the new line
				line = file.readline()
				tokens = line.split(',')

			# d. incrementing the cycle
			cycle = cycle + 1
			time = []

			if(len(Q) != 0 and len(V) != 0 and any([t != Q[0] for t in Q]) ):
				# e. Differentiating dQ/dV

				#i. tmp_U = smooth(readings.U(bool_0A25),round(sum(bool_0A25)/50));
				V = self.__smooth__(V,round(len(V)/50) + 1 if ((round(len(V)/50) % 2) == 0) else round(len(V)/50))

				#ii. tmp_Ah = tmp_Ah - min(tmp_Ah)----OK
				minQ = min(Q)
				for i in range (0, len(Q)):
					Q[i] = Q[i] - minQ

				#iii. tmp_Ah(2)=(tmp_Ah(3)-tmp_Ah(1))/2;---???????
				#Q[3] = (Q[3] - Q[1])/2.0

				#iv. dQ = max(tmp_Ah) / 500;----OK
				dQ = max(Q)/500

				#v. dV = interp1(tmp_Ah, tmp_U, tmp_Ah+dQ, 'pchip') - tmp_U; 
				temp = []
				for i in range (0, len(Q)):
					temp.append(Q[i]+dQ) # temp_Ah + dQ ----OK

				#ordenation
				aux_sort = []
				for i in range(0, len(Q)):
					aux_sort.append([Q[i], V[i]])

				aux_sort = sorted(aux_sort)
				for i in range(0, len(aux_sort)):
					Q[i] = aux_sort[i][0]
					V[i] = aux_sort[i][1]

				aux = scipy.interpolate.pchip_interpolate(Q, V, temp) #pchip interpolation

				dV = []
				for i in range(0, len(aux)):
					dV.append(aux[i] - V[i]) #interpolation - V

				#dVdQ = dV/dQ;
				dVdQ = []
				for i in range(0, len(dV)):
					dVdQ.append(dV[i]/dQ)

				#vi. plot_x = (tmp_Ah+dQ/2)
				plotx = []
				for i in range(0, len(Q)):
					plotx.append((Q[i]+dQ)/2)

				#for i in range(1,len(dVdQ)+1):
				#	time.append(i)

				#spline(time,information,time)

				matplotlib.pyplot.plot(plotx, dVdQ,'-',label = 'Cycle ' + str(cycle-1))
				dVdQ = []
				dV = []
				dQ = []
				V = []
				Q = []
				plotx = []

				# f. plot
				if(abs(cycle) / 10 > cur_file):

					print(dest + '/' + plottitle + str(cur_file) + '.png')
					matplotlib.pyplot.legend(loc = 'upper right')

					cur_file = cur_file + 1
					matplotlib.pyplot.figure(cur_file)

					matplotlib.pyplot.title(plottitle)
					matplotlib.pyplot.xlabel(plotx_title)
					matplotlib.pyplot.ylabel(ploty_title)

		# 6 . Closing the opened file
		matplotlib.pyplot.show()
		print('5: |||||||||| 100%')
		file.close()

		# 7. Thats all folks :) ...
		print('6: |||||||||| 100%')




















	def plot(self,filename,dest,xcol,ycol,mode,plottitle,plotx,ploty,header):
		print('starting save - total steps: 6')

		# 1. Opening the file
		print('1: ',end="")
		file = fopen(filename,'r')
		print('|||||||||| 100%')
		print(file)
		
		# 2. Ignoring the header
		print('2: ',end="")
		if(header is True):
			file.readline()
		print('|||||||||| 100%')

		# 3. Verifying the plot type
		if(COULUMBIC in [xcol,ycol]):
			self.__plotColumbic__(file,dest,7,plottitle,'Cycle Number','Coulombic Efficiency (%)')
			return(None)
			
		if(DVA in [xcol,ycol]):
			self.__plotDVA__(file,dest,plottitle,'Cycle Number','dQ/dV')
			return(None)
			
		# 4. Setting plot labels and retrieving the csv information
		print('3: ',end="")
		matplotlib.pyplot.title(plottitle)
		print('|||',end="")
		matplotlib.pyplot.xlabel(plotx)
		print('||||',end="")
		matplotlib.pyplot.ylabel(ploty)
		print('||| 100%')
		
		information, xinformation, yinformation = [], [], []
		cycle, cur_file = 1, 1

		# 5. Plotting
		print('4: Plotting... total estimate time: 15s')
		line = file.readline()
		matplotlib.interactive(True)
		matplotlib.pyplot.figure(cur_file)

		if(xcol == 4):
			while(re.match('^$', line ) is None):
				# a. tokenizing line
				tokens = line.split(',')

				while(re.match('^$', line ) is None and cycle == abs(int(tokens[1]))):
					# b. storing the information
					value = float(tokens[ycol])

					if(mode*int(tokens[1]) > 0):
						information.append(value)
					elif(mode == FULL_CYCLE):
						information.append(value)

					# c. reading the new line
					line = file.readline()
					tokens = line.split(',')

				# d. incrementing the cycle
				cycle = cycle + 1
				time = []

				for i in range(1,len(information)+1):
					time.append(i)

				#spline(time,information,time)
				matplotlib.pyplot.plot(information,'-',label = 'Cycle ' + str(cycle-1))
				information = []

				# e. plotting
				if(abs(cycle) / 10 > cur_file):
					print(dest + '/' + plottitle + str(cur_file) + '.png')
					matplotlib.pyplot.legend(loc = 'upper right')

					cur_file = cur_file + 1
					matplotlib.pyplot.figure(cur_file)

					matplotlib.pyplot.title(plottitle)
					matplotlib.pyplot.xlabel(plotx)
					matplotlib.pyplot.ylabel(ploty)


			if(abs(cycle) / 10 == cur_file):
				print(dest + '/' + plottitle + str(cur_file) + '.png')
				matplotlib.pyplot.legend(loc = 'upper right')
		elif(ycol == 4):
			matplotlib.pyplot.xlabel(ploty)
			matplotlib.pyplot.ylabel(plotx)

			while(re.match('^$', line ) is None):
				# a. tokenizing line
				tokens = line.split(',')

				while(re.match('^$', line ) is None and cycle == abs(int(tokens[1]))):
					# b. storing the information
					value = float(tokens[xcol])

					if(mode*int(tokens[1]) > 0):
						information.append(value)
					elif(mode == FULL_CYCLE):
						information.append(value)

					# c. reading the new line
					line = file.readline()
					tokens = line.split(',')

				# d. incrementing the cycle
				cycle = cycle + 1
				time = []

				for i in range(1,len(information)+1):
					time.append(i)

				#spline(time,information,time)
				matplotlib.pyplot.plot(information,'-',label = 'Cycle ' + str(cycle-1))
				information = []

				# e. plotting
				if(abs(cycle) / 10 > cur_file):
					print(dest + '/' + plottitle + str(cur_file) + '.png')
					matplotlib.pyplot.legend(loc = 'upper right')

					cur_file = cur_file + 1
					matplotlib.pyplot.figure(cur_file)

					matplotlib.pyplot.title(plottitle)
					matplotlib.pyplot.xlabel(ploty)
					matplotlib.pyplot.ylabel(plotx)


			if(abs(cycle) / 10 == cur_file):
				print(dest + '/' + plottitle + str(cur_file) + '.png')
				matplotlib.pyplot.legend(loc = 'upper right')
		else:
			while(re.match('^$', line ) is None):
				# a. tokenizing line
				tokens = line.split(',')

				while(re.match('^$', line ) is None and cycle == abs(int(tokens[1]))):
					# b. storing the information
					xvalue = float(tokens[xcol])
					yvalue = float(tokens[ycol])

					if(mode*int(tokens[1]) > 0):
						xinformation.append(xvalue)
						yinformation.append(yvalue)
					elif(mode == FULL_CYCLE):
						xinformation.append(xvalue)
						yinformation.append(yvalue)

					# c. reading the new line
					line = file.readline()
					tokens = line.split(',')

				# d. incrementing the cycle
				cycle = cycle + 1

				#spline(time,information,time)
				matplotlib.pyplot.plot(xinformation,yinformation,'s',label = 'Cycle ' + str(cycle-1))
				xinformation, yinformation = [], []

				# e. plotting
				if(abs(cycle) / 10 > cur_file):
					print(dest + '/' + plottitle + str(cur_file) + '.png')
					matplotlib.pyplot.legend(loc = 'upper right')

					cur_file = cur_file + 1
					matplotlib.pyplot.figure(cur_file)

					matplotlib.pyplot.title(plottitle)
					matplotlib.pyplot.xlabel(plotx)
					matplotlib.pyplot.ylabel(ploty)


			if(abs(cycle) / 10 == cur_file):
				print(dest + '/' + plottitle + str(cur_file) + '.png')
				matplotlib.pyplot.legend(loc = 'upper right')

		# 6 . Closing the opened file
		matplotlib.pyplot.show()
		print('5: |||||||||| 100%')
		file.close()

		# 7. Thats all folks :) ...
		print('6: |||||||||| 100%')
