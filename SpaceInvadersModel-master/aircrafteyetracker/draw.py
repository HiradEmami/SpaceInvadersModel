import pygame as pg
import os

import buttons

class Draw:
	blue = (0,0,35)
	white = (255,255,255)
	green = (0, 255, 0)
	red = (255, 50, 50)
	grey = (125, 125, 125)
	
	def __init__(self,window,the_map):
		self.pg = pg
		self.window = window
		self.map = the_map

		self.posgreen = pg.image.load(os.path.join('images/posgreen.png'))
		self.posred = pg.image.load(os.path.join('images/posred.png'))
		self.posorange = pg.image.load(os.path.join('images/posorange.png'))
		self.pointimg = pg.image.load(os.path.join('images/point.png'))
		self.deadimg = pg.image.load(os.path.join('images/dead.png'))
		self.barbottomimg = pg.image.load(os.path.join('images/barbottom.png'))
		self.simpleairport = pg.transform.scale(pg.image.load(os.path.join('images/simpleairport.png')),(self.window.res_x,self.window.res_y))
		self.simpleairportb = pg.transform.scale(pg.image.load(os.path.join('images/simpleairportb.png')),(self.window.res_x,self.window.res_y))
		self.simpleairportc = pg.transform.scale(pg.image.load(os.path.join('images/simpleairportc.png')),(self.window.res_x,self.window.res_y))


		self.circle_brightness = 125
		self.brightest = True

		self.btn_list = []
		self.btn = []
		# cur_input = ""


	# Returns participant number, gender and age, and the name of the logfile
	def get_part_info(self,window):
		inputbox = Inputbox(self)
		i = inputbox.ask(window.screen, "Participant number")
		# if an already existing number is given, ask again
		while os.path.isfile("./log/%s.log" %i):
			i = inputbox.ask(window.screen, "Participant number is taken, try another one")
		# if nothing is given, assign the next available integer
		if i == "":
			i = "1"
			while os.path.isfile("./log/%s.log" %i): 
				i = str(int(i) + 1)
		pnr = i
		gen = inputbox.ask(window.screen, "Gender")
		age = inputbox.ask(window.screen, "Age")
		return(("\n" + "Participant nr: " + pnr + "\nGender: " + str(gen) + "\nAge: " + str(age)),pnr)


	def draw_planes(self,list_of_planes,selected_plane,warn_dis):
		for plane in list_of_planes:
			# "Glowing" circle
			if (self.brightest == True):
				self.circle_brightness = self.circle_brightness + 4
				if (self.circle_brightness > 225):
					self.brightest = False
			else:
				self.circle_brightness = self.circle_brightness - 4
				if (self.circle_brightness < 125):
					self.brightest = True

			# Heading line
			flx = 0
			fly = 0
			leng = warn_dis + int(0.5 * float(warn_dis))
			if (plane.heading == 1):
				flx = int(plane.x_coord)
				fly = int(plane.y_coord) - leng
			elif (plane.heading == 2):
				flx = int(plane.x_coord) + leng
				fly = int(plane.y_coord)
			elif (plane.heading == 3):
				flx = int(plane.x_coord)
				fly = int(plane.y_coord) + leng
			elif (plane.heading == 4):
				flx = int(plane.x_coord) - leng
				fly = int(plane.y_coord)

			misc = ""
			label_font = pg.font.SysFont("Courier New", 16)
			
			if (int(plane.altitude) != int(plane.new_altitude)): # if altitude is changing
				misc = str("->" + str(plane.new_altitude)) # write it to misc
				
			if plane.state == "nop":
				name_label = label_font.render(plane.name, 1, self.green) # green name_label
				misc_label = label_font.render("ALT " + str(plane.altitude) + misc, 1, self.green) # green altitude
				self.window.screen.blit(self.posgreen, (int(plane.x_coord) - 7, int(plane.y_coord) - 3)) # green marker
				
				if (plane is selected_plane): #if this plane is selected
					pg.draw.circle(self.window.screen, (0,self.circle_brightness,0), (int(plane.x_coord),int(plane.y_coord)), warn_dis, 2) # green circle

			elif plane.state == "danger":
				# TODO: solve problem of multiple planes being at the same dangerous distance
				nearest_plane,nearest_distance = plane.nearest
				name_label = label_font.render(plane.name, 1, self.red) # red name_label
				misc_label = label_font.render("DIS " + str(int(nearest_distance)), 1, self.red) # red distance
				self.window.screen.blit(self.posred, (int(plane.x_coord) - 7, int(plane.y_coord) - 3)) # red marker

				pg.draw.circle(self.window.screen, (self.circle_brightness,0,0), (int(plane.x_coord),int(plane.y_coord)), int(warn_dis), 1) # red circle

				pg.draw.line(self.window.screen, (150, 150, 150), (int(plane.x_coord), int(plane.y_coord)), (nearest_plane.x_coord, nearest_plane.y_coord)) # connecting line
				pg.draw.line(self.window.screen, (220,0,0), (int(plane.x_coord),int(plane.y_coord)), (flx,fly)) # front line

				if (plane is selected_plane): #if this plane is selected 
					pg.draw.circle(self.window.screen, (self.circle_brightness,0,0), (int(plane.x_coord),int(plane.y_coord)), int(warn_dis), 2) # bigger warning crcle

			if plane.state == "dead": 
				name_label = label_font.render(plane.name, 1, self.grey)
				misc_label = label_font.render("", 1, self.blue)
				self.window.screen.blit(self.deadimg, (int(plane.x_coord) - 7, int(plane.y_coord) - 3))

			self.window.screen.blit(name_label, (int(plane.x_coord), int(plane.y_coord)))
			self.window.screen.blit(misc_label, (int(plane.x_coord), int(plane.y_coord) + 15))
		pg.display.update()
			
	def draw_map(self,next_map):

		if 0 <= next_map <= 1:
			self.window.screen.blit(self.simpleairport, (0,0))
			next_map += 1
		elif 2 <= next_map <= 3:
			self.window.screen.blit(self.simpleairportb, (0,0))
			next_map += 1
		elif next_map == 4:
			self.window.screen.blit(self.simpleairportc, (0,0))
			next_map += 1
		elif next_map == 5:
			self.window.screen.blit(self.simpleairportc, (0,0))
			next_map = 0
		return next_map

	# def draw_fixed_info():
		# #passed / failed screen
		# if (mission == "passed"):
		# 	lab = pg.image.load(os.path.join("images/passed.png"))
		# 	labscaled = pg.transform.scale(lab, (sw, sh))
		# 	screen.blit(labscaled, (0,0))
		# if (mission == "failed"):
		# 	lab = pg.image.load(os.path.join("images/failed.png"))
		# 	labscaled = pg.transform.scale(lab, (sw, sh))
		# 	screen.blit(labscaled, (0,0))
		# 	#scale map to resolution
		
		
		
		# #lbottom bar
		# screen.blit(bottomimg, (0, (resy - 20)))
		# screen.blit(topimg, (0, 0))
		# #things that are not displayed at the end
		# if (mission == ""):		
		# #version label
		# 	sfont = pg.font.SysFont("Arial Black", 13)
			
		# 	if (int(speed) == int(nspeed)): versionlabel = sfont.render(version, 1, (180, 180, 180))

		# 	screen.blit(versionlabel, (sw - 40, sh - 21))
			

		# #sound label
		# sfont = pg.font.SysFont("Arial", 14)
		# if (psound == True): timelabel = sfont.render("Sound: on", 1, (255, 255, 255))
		# if (psound == False): timelabel = sfont.render("Sound: off", 1, (255, 255, 255))
		# screen.blit(timelabel, (10, sh - 17))
		
		# TODO: draw score label
		# #score label
		# sfont = pg.font.SysFont("Arial", 14)
		# scorelabel = sfont.render("Score: " + str(int(score)), 1, (255, 255, 255))
		# screen.blit(scorelabel, ((sw / 2) - 20, sh - 17))
		
		# myfont1 = pg.font.SysFont("Arial", 20) 
		# myfont2 = pg.font.SysFont("Arial", 16) 
		
		# infolabel = myfont1.render(textl1, 1, (255, 255, 255))
		# screen.blit(infolabel, (10, 5))
		
		#line 2
		# textl2 = "lost: " + str(planes_lost) + " // failed: " + str(planes_dead) + " // completed: " +  str(planes_landed) + " // Ground at " + cfg.get("map", "ground") + "ft"
		# infolabel2 = myfont2.render(textl2, 1, (255, 255, 255))
		# screen.blit(infolabel2, (10, 25))

	def draw_interruption(self,text,pos):
		# displays the given math problem		
		color = (200, 200, 255)				
		font = pg.font.SysFont("Arial", 20)
		rtext = font.render(text, 1, color)	
		if pos == "top":
			width, height = font.size(text)
			dest = ((self.window.res_x/2)-(width/2),self.window.res_y/2-15)
		elif pos == "bottom":
			width, height = font.size(text)
			dest = ((self.window.res_x/2)-(width/2),self.window.res_y/2+15)
	
		# displays the numerical keyboard for input
	
		# create and position all buttons with a for-loop
		x = 0
		y = 1
		n = 0
		for label in self.btn_list:
			self.btn[n] = buttons.Button()
			# create the button
			self.btn[n].create_button(self.window.screen,(107,142,35), x*65+(self.window.res_x/2)-75, y*45+(self.window.res_y/2)+40, 50, 30, 0, label, (255,255,255))
			# increment button index
			n += 1
			# update row/column position
			x += 1
			if x > 2:
				x = 0
				y += 1
	
		self.window.screen.blit(rtext, dest)


	def init_keys(self):
		
		self.btn_list = [
		'7',  '8',  '9',
		'4',  '5',  '6',
		'1',  '2',  '3',
		'Del','0',  'Enter']
		# list(range()) needed for Python3
		self.btn = list(range(len(self.btn_list)))
		# create and position all buttons with a for-loop
		x = 0
		y = 1
		n = 0
		for label in self.btn_list:
			self.btn[n] = buttons.Button()
			# create the button
			self.btn[n].create_button(self.window.screen,(107,142,35), x*65+(self.window.res_x/2)-75, y*45+(self.window.res_y/2)+40, 50, 30, 0, label, (255,255,255))
			# increment button index
			n += 1
			# update row/column position
			x += 1
			if x > 2:
				x = 0
				y += 1


	def input(self,events,cur_input):
		# displays the user input real time and returns true when enter is hit
		# using keyboard
		# event = pg.event.pump()
		# for event in pg.event.get():
		# 	if event.type == pg.KEYDOWN:
		# 		inkey = event.key
		# 		if inkey == pg.K_BACKSPACE:
		# 			cur_input = cur_input[0:-1]
		# 		elif inkey == pg.K_RETURN:
		# 			return True
		# 		elif inkey <= 127:
		# 			cur_input += str(chr(inkey))

		# using on screen numerical keyboard
		if events is not None:
			for event in events:
				if event.type == pg.MOUSEBUTTONDOWN:
					mousepos = pg.mouse.get_pos()
					if self.btn[0].pressed(mousepos):
						cur_input += str(7)
					elif self.btn[1].pressed(mousepos):
						cur_input += str(8)
					elif self.btn[2].pressed(mousepos):
						cur_input += str(9)
					elif self.btn[3].pressed(mousepos):
						cur_input += str(4)
					elif self.btn[4].pressed(mousepos):
						cur_input += str(5)
					elif self.btn[5].pressed(mousepos):
						cur_input += str(6)
					elif self.btn[6].pressed(mousepos):
						cur_input += str(1)
					elif self.btn[7].pressed(mousepos):
						cur_input += str(2)
					elif self.btn[8].pressed(mousepos):
						cur_input += str(3)
					elif self.btn[9].pressed(mousepos):
						cur_input = cur_input[0:-1]
					elif self.btn[10].pressed(mousepos):
						cur_input += str(0)
					elif self.btn[11].pressed(mousepos):
						return 1,cur_input
			return 0,cur_input

class Window:
	def __init__(self):
		self.res_x = 1600
		self.res_y = 1200
		full_screen = True
		pg.display.set_caption('Towerm')
		icon = pg.image.load(os.path.join('images/icon.png'))
		pg.display.set_icon(icon)
		if full_screen == True:
			self.screen = pg.display.set_mode((self.res_x,self.res_y),pg.FULLSCREEN)
		else:
			os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100" # position window
			self.screen = pg.display.set_mode((self.res_x,self.res_y))


class Inputbox:

	def __init__(self,draw):
		self.draw = draw

	def get_key(self):
		while 1:
			event = pg.event.poll()
			if event.type == pg.KEYDOWN:
				return event.key
			elif event.type == pg.QUIT:
				pg.quit()
				sys.exit()
			else:
				pass

	def display(self,screen,message,fontsize,destsubtrx):
		# screen.fill(self.draw.blue)
		fontobject = pg.font.Font(None,fontsize)
		if len(message) != 0:
			screen.blit(fontobject.render(message, 1, self.draw.white),
			           ((screen.get_width() / 2) - destsubtrx, (screen.get_height() / 2) - 10))
		pg.display.flip()
	
	def display_box(self,screen, message):
		"Print a message in a box in the middle of the screen"
		# fontobject = pg.font.Font(None,18)
		pg.draw.rect(screen, self.draw.blue,
						((screen.get_width() / 2) - 100,
						 (screen.get_height() / 2) - 10,
						  200,20), 0)
		pg.draw.rect(screen, self.draw.white,
		                 ((screen.get_width() / 2) - 102,
		                  (screen.get_height() / 2) - 12,
		                  204,24), 1)
		self.display(screen,message,18,100)
		pg.display.flip()
	
	def ask(self,screen, question):
		"ask(screen, question) -> answer"
		pg.font.init()
		current_string = []
		self.display_box(screen, question + ": " + "".join(current_string))
		while 1:
			inkey = self.get_key()
			if inkey == pg.K_ESCAPE:
				pg.quit()
				sys.exit()
			elif inkey == pg.K_BACKSPACE:
				current_string = current_string[0:-1]
			elif inkey == pg.K_RETURN:
				break
			elif inkey == pg.K_MINUS:
				current_string.append("_")
			elif inkey <= 127:
				current_string.append(chr(inkey))
			self.display_box(screen, question + ": " + "".join(current_string))
		return "".join(current_string)
	