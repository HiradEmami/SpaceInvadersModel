# Python modules
import os
import time
import ConfigParser as configparser
import random
import pygame as pg
# Custom modules
import draw
import interruption
import logger
import game
import the_map
import pginput
import eyetracker

# This is the main class
class Towerm:

	# Constructor of the main class
	def __init__(self):
		self.start_time = time.time()
		self.window = draw.Window()
		self.map = the_map.Map()
		self.draw = draw.Draw(self.window,self.map)
		self.pginput = pginput.Input()

		self.config = configparser.RawConfigParser()
		self.config.read(os.path.join("towerm.conf"))

		# Get information about the user and write it to the logfile

		# threshold = self.config.get("interruption", "threshold")
		part_info,self.pnr = self.draw.get_part_info(self.window)
		log_file_name = "./log/" + self.pnr + ".log"

		# Instantiate and calibrate the eyetracker
		self.eyetracker = eyetracker.Eyetracker(self.pnr)
		self.logger = logger.Logger("%(asctime)s %(message)s",log_file_name,"logging.DEBUG",self.start_time,self.eyetracker)
		self.logger.log(part_info)
		self.interruption = interruption.Interruption(self.window,self.draw,self.pginput,self.logger)


		self.baseline = 0
		self.eyetracker.start()

		# Initiate and start 3 practice trials with 2 planes
		self.condition = "practice"
		trial_nr = -1
		nr_of_practice_trials = 6

		while trial_nr >= -nr_of_practice_trials:
			if (trial_nr == -1) or (trial_nr == -2):
				self.condition = "practice_no"
			if (trial_nr == -3) or (trial_nr == -4):
				self.condition = "practice_yes"
			if (trial_nr == -5) or (trial_nr == -6):
				self.condition = "practice"
			self.condition = "practice"
			practice_trial = self.Trial(trial_nr,self.window,self.map,self.draw,self.pginput,self.logger,self.interruption,3,self.condition,self.eyetracker)

			waiting = True
			while waiting:
				events,keyinput = self.pginput.get_input(self.eyetracker)
				if not keyinput[pg.K_SPACE]:
					self.window.screen.fill(self.draw.blue)
					draw.Inputbox(self.draw).display(self.window.screen,"Hit SPACE to start the next practice trial",50,320)
				# print("game.game_loop test. self.pause: %s" %self.pause)
				else:
					self.logger.log("SPACE was pressed, practice trial starts now") 
					waiting = False
			x,baseline_temp = practice_trial.run(0,0)
			self.baseline = self.baseline + baseline_temp
			self.logger.log("temporary baseline: %s" %self.baseline)
			trial_nr -= 1
		self.baseline = self.baseline/nr_of_practice_trials
		self.logger.log("final baseline: %s" %self.baseline)

	def run(self):
		# if (self.pnr == "1") or (self.pnr == "7"):
		# 	block_condition_order_list = ["eyetracker","random","control"]
		# elif (self.pnr == "2") or (self.pnr == "8"):
		# 	block_condition_order_list = ["random","control","eyetracker"]
		# elif (self.pnr == "3") or (self.pnr == "9"):
		# 	block_condition_order_list = ["control","eyetracker","random"]
		# elif (self.pnr == "4") or (self.pnr == "10"):
		# 	block_condition_order_list = ["eyetracker","control","random"]
		# elif (self.pnr == "5") or (self.pnr == "11"):
		# 	block_condition_order_list = ["random","eyetracker","control"]
		# elif (self.pnr == "6") or (self.pnr == "12"):
		# 	block_condition_order_list = ["control","random","eyetracker"]
		# else:
			# block_condition_order_list = ["eyetracker","random","control"]
		#block_condition_order_list = ["eyetracker","random","control"] # TODO: remove
		block_condition_order_list = ["eyetracker","eyetracker","eyetracker","eyetracker","eyetracker","random","random","random","random","random","control","control","control","control","control"]
		random.shuffle(block_condition_order_list)
		first_condition = block_condition_order_list[0]
		self.logger.log("Condition order: %s" %block_condition_order_list)

		# Start blocks
		self.block_size = self.config.get("experiment", "block_size")
		super_trial_size = self.config.get("experiment", "super_trial_size")
		block_nr = 1
		for b in block_condition_order_list:
			block = self.Block(block_nr,self.SuperTrial,self.Trial,self.window,self.map,self.draw,self.pginput,self.logger,self.interruption,b,self.block_size,super_trial_size,self.eyetracker,self.baseline)
			block_nr += 1
			self.logger.log("current block nr: %s" %block_nr)
			if ((block_nr == 2) or (block_nr == 6) or (block_nr == 11)):
				waiting = True
				self.logger.log("Paused at block nr: %s" %block_nr)
			while waiting:
				events,keyinput = self.pginput.get_input(self.eyetracker)
				if not keyinput[pg.K_SPACE]:
					self.window.screen.fill(self.draw.blue)
					draw.Inputbox(self.draw).display(self.window.screen,"You can have a short break, hit SPACE to start",50,400)
				else: 
					self.logger.log("SPACE was pressed, break ended")
					self.logger.log("Drift correction starts now")
					waiting = False
					self.eyetracker.drift_correct()
			
			block.run()		
			# print(block.condition)

		self.eyetracker.exit()

	class Block:
		# initialize supertrials
		# start supertrials
		# adjust threshold

		# start eyetracker

		def __init__(self,nr,SuperTrial,Trial,window,the_map,draw,pginput,logger,interruption,condition,block_size,super_trial_size,eyetracker,baseline):
			self.nr = nr
			self.SuperTrial = SuperTrial
			self.logger = logger
			self.interruption = interruption
			self.condition = condition
			self.block_size = block_size
			self.super_trial_size = super_trial_size
			self.eyetracker = eyetracker

			# Initialize super trials
			self.super_trial_list = []
			self.super_trial_nr = 1
			while int(self.super_trial_nr) <= int(self.block_size):
				self.super_trial_list.append(self.SuperTrial(self.super_trial_nr,Trial,window,the_map,draw,pginput,logger,interruption,condition,super_trial_size,eyetracker,baseline))
				self.super_trial_nr += 1

		
		def run(self):
			self.logger.log("Block %s started" %self.nr)
			interruptions_at_start = self.interruption.get_nr_of_interruptions()
			
			self.logger.log("Current block condition: %s" %self.condition)
			
			if self.condition == "eyetracker":
				self.eyetracker.start()
			
			# Set the score for the first trial of the block to 300
			score = 300

			for super_trial in self.super_trial_list:
				score = super_trial.run(score)
			
			self.logger.log("End score of this block: %s" %score)
			self.logger.log("Nr of interruptions of this block: %s" %(self.interruption.get_nr_of_interruptions() - interruptions_at_start))
			self.logger.log("Block %s ended" %self.nr)
			return

	class SuperTrial:
		def __init__(self,nr,Trial,window,the_map,draw,pginput,logger,interruption,condition,super_trial_size,eyetracker,baseline):
			self.nr = nr
			self.window = window
			self.draw = draw
			self.logger = logger
			self.interruption = interruption
			self.condition = condition
			self.super_trial_size = super_trial_size
			self.eyetracker = eyetracker
			self.baseline = baseline


			# Determine the order of hard (5 planes) and easy (2 planes) trials of this block
			trial_difficulty_order = [3] * int(int(super_trial_size)/2) + [6] * int(int(super_trial_size)/2)
			#random.shuffle(trial_difficulty_order)
			self.trials = []
			trial_nr = 1
			for t in trial_difficulty_order:
				# print("Test Super trial constructor")
				# self.logger.log("trial_difficulty_order: %s, super_trial_size: %s" %(trial_difficulty_order,super_trial_size))
				self.trials.append(Trial(trial_nr,window,the_map,draw,pginput,logger,interruption,t,condition,eyetracker))
				trial_nr += 1

		def run(self,score):
			self.logger.log("Super trial %s started" %self.nr)
			interruptions_at_start = self.interruption.get_nr_of_interruptions()

			for trial in self.trials:
				# Draw countdown time
				end_loop_time = time.time() + 6
				time_left = 5
				while end_loop_time >= time.time() + 1.1:
					if end_loop_time <= time.time() + time_left:
						time_left -= 1
					self.window.screen.fill(self.draw.blue)
					draw.Inputbox(self.draw).display(self.window.screen,("The next trial will start in %s seconds" %time_left),50,300)

				score,x = trial.run(score,self.baseline)


			self.logger.log("End score of this super trial: %s" %score)
			interruptions = self.interruption.get_nr_of_interruptions() - interruptions_at_start
			self.logger.log("Nr of interruptions of this super trial: %s" %interruptions)
			
			
			if self.condition == "eyetracker":
				adapted,threshold = self.eyetracker.adapt_threshold(interruptions,self.super_trial_size)
				self.logger.log("Threshold adapted by %s, new threshold: %s" %(adapted,threshold))
			self.logger.log("Super trial %s ended" %self.nr)
			return score


	class Trial:
		def __init__(self,nr,window,the_map,d,pginput,logger,interruption,nr_of_planes,condition,eyetracker):
			# practice_trial = False
			self.nr = nr
			self.interruption = interruption
			# if nr <= 0:
			# 	practice_trial = True
			self.game = game.Game(window,the_map,d,pginput,logger,interruption,nr_of_planes,condition,time.time(),eyetracker,nr,draw)
			self.logger = logger
			# self.logger.log("Kom ik hier? Trial")
			self.eyetracker = eyetracker

		def run(self,start_score,baseline):
			self.logger.log("Trial %s started" %self.nr)
			interruptions_at_start = self.interruption.get_nr_of_interruptions()
			end_score,baseline = self.game.game_loop(start_score,baseline)
			interruptions = self.interruption.get_nr_of_interruptions() - interruptions_at_start
			self.logger.log("Trial %s ended. End score: %s, number of interruptions: %s, baseline: %s" %(self.nr,int(end_score),interruptions,baseline))
			return end_score,baseline

program = Towerm()
program.run()