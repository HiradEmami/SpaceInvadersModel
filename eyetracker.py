from pylink import *
import gc
import os
import sys
import random
import numpy as np
import time
import Queue

class Eyetracker:
	def __init__(self,pnr, winSize = 600):
		self.winSize = winSize
		self.pnr = pnr
		# self.simulation = False
		self.initialize()
		getEYELINK().doTrackerSetup() # Calibrate
		#for test without eyetracker, set simulation to True
		self.dilation_list = []


		self.baseline_counter = 0
		self.baseline_temp  = 0
		self.sample_dilation = 0
		self.baseline = 1

		self.wiv = 0
		self.low_wl = False
		self.low_wl_start_time = 0
		self.ic = 0
		self.live_avg = None
		self.pcps = 0
		self.pcps_list = []
		# self.last_live_avg_time = 0
		self.threshold = 0.997
		# threshold volgens eerder onderzoek 0.997!
		self.interruption_criterion = 2 # mean number of interruptions during a trial

	def initialize(self):
		spath = os.path.dirname(sys.argv[0])
		if len(spath) !=0: os.chdir(spath)

		# if self.simulation:
		# 	eyelinktracker = EyeLink(None)
		# else:
		eyelinktracker = EyeLink()

		#init pygame
		#pg.init()
		#pg.display.init()
		#pg.display.set_mode((800, 600), pg.FULLSCREEN |pg.DOUBLEBUF |pg.RLEACCEL|pg.HWSURFACE ,32)

		pylink.openGraphics()

		#Opens the EDF file.
		edfFileName = "ced_" + str(self.pnr) + ".edf"
		# edfFileName = "mar1.edf";
		getEYELINK().openDataFile(edfFileName)

		pylink.flushGetkeyQueue(); 
		getEYELINK().setOfflineMode();

		#Gets the display surface and sends a message to EDF file;
		surf = pg.display.get_surface()
		getEYELINK().sendCommand("screen_pixel_coords =  0 0 %d %d" %(self.winSize, self.winSize))
		getEYELINK().sendMessage("DISPLAY_COORDS  0 0 %d %d" %(self.winSize, self.winSize))

		tracker_software_ver = 0
		eyelink_ver = getEYELINK().getTrackerVersion()
		if eyelink_ver == 3:
			tvstr = getEYELINK().getTrackerVersionString()
			vindex = tvstr.find("EYELINK CL")
			tracker_software_ver = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))

		if eyelink_ver>=2:
			getEYELINK().sendCommand("select_parser_configuration 0")
			if eyelink_ver == 2: #turn off scenelink camera stuff
				getEYELINK().sendCommand("scene_camera_gazemap = NO")
		else:
			getEYELINK().sendCommand("saccade_velocity_threshold = 35")
			getEYELINK().sendCommand("saccade_acceleration_threshold = 9500")

		# set EDF file contents 
		getEYELINK().sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON")
		if tracker_software_ver>=4:
			getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS,HTARGET")
		else:
			getEYELINK().sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,AREA,GAZERES,STATUS")

		# set link data (used for gaze cursor) 
		getEYELINK().sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON")
		if tracker_software_ver>=4:
			getEYELINK().sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,HTARGET")
		else:
			getEYELINK().sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS")


		getEYELINK().sendCommand("button_function 5 'accept_target_fixation'");

		pylink.setCalibrationColors( (255, 255, 255), (0, 0, 0));  	#Sets the calibration target and background color
		pylink.setTargetSize(int(surf.get_rect().w/70), int(surf.get_rect().w/300));	#select best size for calibration target
		pylink.setCalibrationSounds("", "", "");
		pylink.setDriftCorrectSounds("", "off", "off");

	def start(self):
		getEYELINK().startRecording(1,1,1,1)
	
		gc.disable();
		#begin the realtime mode
		pylink.beginRealTimeMode(100)
		self.dil_update = 0
		self.dilation = 6000

	def drift_correct(self):
		surf = pg.display.get_surface()
		while 1:
			# Does drift correction and handles the re-do camera setup situations
			try:
				# print("Drift correction target at: " + str(surf.get_rect().w/2,surf.get_rect().h/2))
				error = getEYELINK().doDriftCorrect(self.winSize / 2,self.winSize /2,1,1)
				if error != 27:
					break
				else:
					getEYELINK().doTrackerSetup();
			except:
				break

		# self.start()

	# def check_dilation(self):

	# 	self.dil_update += 1
	# 	if self.dil_update > 5:
	# 		if self.simulation:
	# 			dt = 1
	# 		else:
	# 			dt = getEYELINK().getNewestSample() # check for new sample update
			
	# 		if(dt != None):
	# 			if self.simulation:
	# 				self.dilation += np.random.random_integers(-.015*self.dilation,.015*self.dilation)
	# 			else:
	# 				self.dilation = int(round(dt.getLeftEye().getPupilSize()))

	# 			self.dilation_list = np.append(self.dilation_list[1:],self.dilation)
	# 			self.dil_update = 0

	def get_dilation(self):
		try:
			dilation = int(round(getEYELINK().getNewestSample().getLeftEye().getPupilSize()))
			if (dilation > (.5 * self.baseline)) and self.on_screen(): # don't record eyeblinks and off-screen pupil positions
				return dilation
		except:
			return
	
	def on_screen(self):
		x,y = getEYELINK().getNewestSample().getLeftEye().getGaze()
		valid_x = (x > 0) and (x < 1600)
		valid_y = (y > 0) and (y < 1200)
		return (valid_x and valid_y)
	
	# Calculates Workload Identifier Value and determines if it is time for an interruption
	def check_wiv(self):
		live_avg = self.get_live_avg()
		if live_avg is not None:
			self.wiv = self.threshold * live_avg
		else: return False

		pcps = self.get_pcps()
		getEYELINK().sendMessage("%s: live_avg: %s" %(time.time(),live_avg))
		getEYELINK().sendMessage("%s: self.wiv: %s" %(time.time(),self.wiv))
		getEYELINK().sendMessage("%s: pcps: %s" %(time.time(),pcps))
  
		if (pcps is not None) and (pcps < self.wiv): # this is a low workload moment
			if not self.low_wl: # if the previous moment was no low workload moment
				self.low_wl_start_time = time.time()
				self.low_wl = True
			# print("%s: low_wl moment, starting time: %s" %(time.time(),self.low_wl_start_time))
		else:
			self.low_wl = False

		if self.low_wl and (self.low_wl_start_time + 0.2 <= time.time()):
			return True
		else:
			return False

	# Calculates the Percentage Change in Pupil Size
	def get_pcps(self):
		dilation = self.get_dilation()
		if dilation is not None:
			self.pcps = ((float(dilation) - float(self.baseline))/float(self.baseline))*100 + 1000 # + 1000 to prevent negative values (in check wiv)
			return self.pcps
		else: return None

	def get_live_avg(self):
		# make space and add newest dilation
		pcps = self.get_pcps()
		if pcps is not None:
			# The game loops max 14 times per second so the number of measures in a minute is about the same as 14*60 = 840
			while len(self.pcps_list) >= 840:
				self.pcps_list.pop(0)
			self.pcps_list.append(pcps)
		else: return None


		# test:
		# print("pcps_list: %s" %self.pcps_list)


		# return live_avg if available
		while len(self.pcps_list) < 840:
			self.pcps_list.append(self.pcps)
		else:
			#f = open('pcps_list', 'a')
			#s = str(self.pcps_list)
			#f.write(s)
			self.live_avg = sum(self.pcps_list) / float(len(self.pcps_list))
			return self.live_avg



	def get_baseline(self):
		dilation = self.get_dilation()
		if dilation is not None:
			self.baseline_counter += 1
			self.baseline_temp = (self.baseline_temp + dilation)
			self.baseline = (self.baseline_temp/self.baseline_counter)
		return self.baseline

	def adapt_threshold(self,nr_of_interruptions,super_trial_size):
		# Adapt the threshold proportionally to the deviation of the number of interruptions
		mean_nr_of_interruptions = float(nr_of_interruptions)/float(super_trial_size) # mean nr of interruptions per trial
		normal = 2 # Ideally the mean nr of interruptions per trial is 2
		scaling_factor = -0.001
		mean_nr_of_interruptions_normalized = (mean_nr_of_interruptions - normal) * scaling_factor
		self.threshold += mean_nr_of_interruptions_normalized
		return mean_nr_of_interruptions_normalized,self.threshold

	def send_message(self,message_contents):
		getEYELINK().sendMessage(message_contents)
        # """
        # The sendMessage method sends a string (max length 128 characters) to the
        # EyeLink device. The message will be time stamped and inserted into the
        # native EDF file, if one is being recorded. If no native EyeLink data file 
        # is being recorded, this method is a no-op.
        # """
        # try:        
        #     if time_offset:            
        #         r = self._eyelink.sendMessage("\t%d\t%s"%(time_offset,message_contents))
        #     else:
        #         r = self._eyelink.sendMessage(message_contents)
    
        #     if r == 0:
        #         return EyeTrackerConstants.EYETRACKER_OK
        #     return EyeTrackerConstants.EYETRACKER_ERROR
        # except Exception, e:
        #     printExceptionDetailsToStdErr()#return createErrorResult("IOHUB_DEVICE_EXCEPTION",
        #     #        error_message="An unhandled exception occurred on the ioHub Server Process.",
        #     #        method="EyeTracker.sendMessage", message_contents=message_contents,time_offset=time_offset, error=e) 

	def disableGraphics(self):
		pylink.closeGraphics()
		pg.display.quit()
	def exit(self):
		getEYELINK().stopRecording();
		# #some pylink stuff
		pylink.endRealTimeMode();
		gc.enable();
			
		getEYELINK().closeDataFile()
		getEYELINK().close();
		pylink.closeGraphics()
		pg.display.quit()
		exit()










