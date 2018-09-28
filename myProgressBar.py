import sys

class myProgressBar:

	def __init__(self,processname,steps,width):
		self.cur_step = 0
		self.cur_percentage = 0
		self.processname = processname
		self.steps = steps
		self.width = width
		print("Starting %s - %d steps" % (self.processname,len(self.steps)))

	def start(self):
		sys.stdout.write("[%s] : %s" % (" " * self.width,self.steps[self.cur_step]))
		sys.stdout.flush()
		sys.stdout.write("\b" * (self.width+4+len(self.steps[self.cur_step])))

	def update(self,percentage):
		sys.stdout.write("%s" % ("-" * int(self.width*(percentage-self.cur_percentage)/100)))
		sys.stdout.flush()
		self.cur_percentage = percentage

		if(percentage == 100):
			self.cur_step = self.cur_step + 1
			self.cur_percentage = 0
			sys.stdout.write("\n")

			if(self.cur_step != len(self.steps)):
				self.start()
			else:
				print("Finished")
