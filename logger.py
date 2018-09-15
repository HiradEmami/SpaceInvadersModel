import logging
import time

class Logger:
	def __init__(self,format,filename,level,start_time,eyetracker):
		self.start_time = start_time
		self.eyetracker = eyetracker
		logging.basicConfig(format=format,filename=filename,level=eval(level))


	def log(self,log_text):
		elt2 = format(int((time.time() - self.start_time) * 1000))
		cline = str(str(elt2) + " " + log_text)
		loginfo = str(cline)
		print(loginfo)
		self.eyetracker.send_message(loginfo)
		logging.info(loginfo)