import pygame as pg
import os
from collisiondetection import CollDetec
import random
# TODO: time en os meegeven vanuit towerm..?
import plane
import time
import score

class Game:
	def __init__(self,window,the_map,draw,pginput,logger,interruption,nr_of_planes,condition,start_time,eyetracker,trial_nr,Draw):
		self.window = window
		self.map = the_map
		self.draw = draw
		self.pginput = pginput
		self.logger = logger
		self.interruption = interruption
		self.nr_of_planes = nr_of_planes
		self.condition = condition
		self.start_time = start_time
		self.eyetracker = eyetracker
		self.trial_nr = trial_nr
		if trial_nr < 0:
			self.practice_trial = True
		else:
			self.practice_trial = False
		self.inputbox = Draw.Inputbox(draw)

		self.game_start_time = 0


		
		# self.plane_speeds = list()
		# self.plane_speedsf = list()
		# self.speed = 1
		self.ground = 1000
		self.warn_dis = 60
		self.collision_dis = 8
		self.landing_dis = 10
		self.list_of_planes = list()
		for i in range(nr_of_planes):
			self.list_of_planes.append(plane.Plane(i+1,self,random.randint((int(int(self.ground) / 100) + 3), (int(int(self.ground) / 100) + 3) + 15) * 100))
		
		pg.init()
		# self.nearest_planes = list()
		# self.fan = list()
		# self.planes_selected = list()
		self.selected_plane = self.list_of_planes[0]
		self.planes_dead = 0
		self.planes_lost = 0
		self.planes_landed = 0

		self.clock = pg.time.Clock()
		self.game_time = 0
		self.pause = False
		self.rate_limiter = 14
		self.log_interval = int(self.rate_limiter) / 8
		self.calc_interval = int(self.rate_limiter) / 5
		self.last_calc_time = 0
		self.running = True
		# self.score = 0
		self.game_duration = 40

		self.next_map = 0
		self.cd = CollDetec()

		self.baseline = 0



	def game_loop(self,start_score,baseline):
		cur_score = start_score
		self.game_start_time = time.time()
		self.baseline = baseline
		
		while self.running:
			events,keyinput = self.pginput.get_input(self.eyetracker)

			if self.practice_trial:
				self.baseline = self.eyetracker.get_baseline()

			# We should do nothing when the game is paused
			if not self.pause:
			#We should not control the game or end the trial during an interruption
				if not self.interruption.check_interrupt(self.condition,self.eyetracker,self.game_start_time):
					self.selected_plane.control(pg,keyinput)
					self.select_plane(events)
					self.check_end()

				self.window.screen.fill(self.draw.blue)

				self.game_time = int(self.game_time) + 1 #time update
				 
				for plane in self.list_of_planes:
					if plane.state != "dead":
						plane.update()
						plane.adjust_altitude()
						plane.check_collision()
						plane.check_landed()
						plane.check_lost()


				# During an interruption we should draw nothing
				if self.interruption.check_interrupt(self.condition,self.eyetracker,self.game_start_time):
					self.interruption_time = self.interruption.make_interruption(events,cur_score)
					if self.interruption_time is not None:
						self.game_duration += self.interruption_time

				else:
					self.next_map = self.draw.draw_map(self.next_map)
					self.draw.draw_planes(self.list_of_planes,self.selected_plane,self.warn_dis)
			
			pg.display.update()
			self.clock.tick(int(self.rate_limiter))
			cur_score = score.Score().calc(self.planes_landed,self.planes_dead + self.planes_lost,self.interruption.probs_solved,self.interruption.probs_failed,self.game_time,start_score)
		return cur_score,self.baseline



	def check_end(self):
		if ((self.condition == "practice_no") or (self.condition == "practice_yes")):
			if (self.planes_landed + self.planes_lost + self.planes_dead) >= self.nr_of_planes:
				self.logger.log("No planes anymore, practice trial ended after %.2f s" %(time.time() - self.game_start_time))
				self.running = False
		elif time.time() > (self.game_start_time + self.game_duration):
			self.running = False

	def select_plane(self,events):
		nearest = None
		if events is not None:
			for event in events:
				if event.type == pg.MOUSEMOTION:
					mx, my = pg.mouse.get_pos()
					temp_dist = 1000
					for plane in self.list_of_planes:
						dist = self.cd.get_distance(mx,my,plane.x_coord,plane.y_coord)
						if (dist < temp_dist):
							if (plane.state != "dead"):
								temp_dist = dist
								nearest = plane
					if nearest is not None:
						self.selected_plane = nearest
						self.logger.log("Plane " + str(nearest.nr) + " selected.")
