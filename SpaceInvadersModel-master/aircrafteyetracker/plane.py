import random
from namecreator import rname
class Plane:
	def __init__(self,nr,game,altitude):
		self.nr = nr
		self.game = game
		self.altitude = altitude

		self.speed = 1.5
		rand_name = rname()   # create a random flight name
		self.name = rand_name.create()	
		self.x_coord = random.randint(50, self.game.window.res_x - 50)
		self.y_coord = random.randint(50, self.game.window.res_y - 30)
		self.heading = random.randint(1,4)
		# print("plane_nr: %s, heading: %s" %(self.nr,self.heading))
		self.new_altitude = self.altitude
		self.nearest = 10000
		# self.selected = False
		self.state = "nop"
		# self.tag = "none"


	# def set_x_coord(self,value):
	# 	self.x_coord = value

	# def set_y_coord(self,value):
	# 	self.y_coord = value

	# def set_heading(self,value):
	# 	self.heading = value
	
	# def set_altitude(self,value):
	# 	self.altitude = value
	
	# def set_new_altitude(self,value):
	# 	self.new_altitude = value

	# def set_nearest(self,value):
	# 	self.nearest = value
		
	# # def set_selected(self,value):
	# # 	self.selected = value
	
	# def set_state(self,value):
	# 	self.state = value
	# def set_tag(self,value):
	# 	self.tag = value

	def adjust_altitude(self):
		if (int(self.altitude) < int(self.new_altitude)): self.altitude = int(self.altitude) + 5
		if (int(self.altitude) > int(self.new_altitude)): self.altitude = int(self.altitude) - 5

	def control(self,pg,keyinput):
		if keyinput[pg.K_w]:
			self.game.logger.log('K_w pressed')
			self.heading = 1
		elif keyinput[pg.K_d]:
			self.game.logger.log('K_d')
			self.heading = 2
		elif keyinput[pg.K_s]:
			self.game.logger.log('K_s')
			self.heading = 3
		elif keyinput[pg.K_a]:
			self.game.logger.log('K_a')
			self.heading = 4
		elif keyinput[pg.K_PAGEUP]:
			self.game.logger.log('K_PAGEUP pressed')
			self.new_altitude = int(self.new_altitude) + 50
		elif keyinput[pg.K_PAGEDOWN]:
			self.game.logger.log('K_PAGEDOWN pressed')
			self.new_altitude = int(self.new_altitude) - 50

	def update(self):
		# Create new coordinates depending on heading
		new_x = self.x_coord
		new_y = self.y_coord
		x_factor = float(self.game.window.res_x) / 1000.0
		y_factor = float(self.game.window.res_y) / 780.0
		if (self.heading == 1): #north
			new_y = new_y - self.speed * (y_factor) * (self.game.calc_interval / 2)
		elif (self.heading == 2): #east
			new_x = new_x + self.speed * (x_factor) * (self.game.calc_interval / 2)
		elif (self.heading == 3): #south
			new_y = new_y + self.speed * (y_factor) * (self.game.calc_interval / 2)	
		elif (self.heading == 4): #west
			new_x = new_x - self.speed * (x_factor) * (self.game.calc_interval / 2)
		# Save new coordinates
		self.x_coord = new_x
		self.y_coord = new_y

	def adjust_altitude(self):
		if (int(self.altitude) < int(self.new_altitude)): self.altitude = int(self.altitude) + 5
		if (int(self.altitude) > int(self.new_altitude)): self.altitude = int(self.altitude) - 5

	def check_collision(self):		
		# Set the nearest dangerous plane with its distance
		self.state = "nop"
		nearest = None
		smallest_dist = 10000
		for plane2 in self.game.list_of_planes:
			if (plane2.state != "dead") and (self.nr != plane2.nr): 
				dist = self.game.cd.get_distance(self.x_coord,self.y_coord,plane2.x_coord,plane2.y_coord)
				if (dist < self.game.warn_dis) and self.alt_check(self.altitude,plane2.altitude) and (dist < smallest_dist):
					# self.game.logger.log("game.check_collision test")
					smallest_dist = dist
					nearest = plane2
					self.state= "danger"
					plane2.state= "danger"
		if nearest is not None:
			self.nearest = (nearest,smallest_dist)
			nearest.nearest = (self,smallest_dist)
			
			# When plane and its nearest dangerous plane collide:
			if (self.game.cd.get_distance(self.x_coord,self.y_coord,nearest.x_coord,nearest.y_coord) < self.game.collision_dis) and self.alt_check(self.altitude,nearest.altitude):
				# self.game.logger.log("game.check_collision test self.state: " + self.state)
				self.state = "dead"
				nearest.state = "dead"
				self.game.planes_dead += 2
				self.game.logger.log(self.name + " collided with " + nearest.name)
		# When plane collides with ground
		elif(int(self.altitude) <= self.game.ground):
			self.state = "dead"
			self.game.planes_dead += 1
			self.game.logger.log(self.name + " crashed into ground")

	def alt_check(self,a1,a2):
		diff = int(a1) - int(a2)
		if ((diff < 200) and (diff > -200)):
			return True
		elif ((diff > 200) or (diff < -200)):
			return False

	def check_landed(self):
		for runway in self.game.map.runways:
			if (float(self.game.cd.get_distance(int(self.x_coord), int(self.y_coord), int(runway.x_coord), int(runway.y_coord))) <= float(self.game.landing_dis)):
				if (self.alt_check(int(self.altitude),int(runway.height)) and (int(self.heading) == int(runway.direction))):
					self.state = "dead"
					self.game.planes_landed += 1
					self.game.logger.log(self.name + " reached its destination")

	def check_lost(self):
		if ((self.x_coord < -60) or (self.x_coord > self.game.window.res_x + 50) or (self.y_coord < -20) or (self.y_coord > self.game.window.res_y + 20)):
			self.state = "dead"
			self.game.planes_lost += 1
			self.game.logger.log(self.name + " got lost")
