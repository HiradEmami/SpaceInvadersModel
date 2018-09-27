import time
import random
import operator

class Interruption:
	def __init__(self,window,draw,pginput,logger):
		self.window = window
		self.draw = draw
		self.pginput = pginput
		self.logger = logger

		self.mathprob = "Nothing"
		self.mathprobq = "What is "
		self.probs_solved = 0
		self.probs_failed = 0

		# self.last_interruption_time = 0
		self.random_time = random.randint(16,30)
		self.interrupt = False
		self.interruption_started = False

		self.start_time = 0
		self.end_time = 0
		self.total_time = 0
		
		self.solved = None
		self.first = True
		self.rand = 0
		self.fixed_score = 0

		self.first_time = 0


	# Returns the total number of interruptions until now
	def get_nr_of_interruptions(self):
		return self.probs_solved + self.probs_failed

	# Returns whether there should be an interruption moment or not based on the interruption condition
	def check_interrupt(self,condition,eyetracker,game_start_time):
		# We do not want to have an interruption until the game has started
		if (self.end_time == 0) or (self.end_time < game_start_time):
			self.end_time = game_start_time

		if condition == "practice_no":
			condition = "control"
		elif condition == "practice_yes":
			condition = "practice"

		if condition == "control":
				return False
		elif condition == "practice":
			if (time.time() >= (self.end_time + 25)):
				return True
			else: return False

		elif time.time() > (self.end_time + 10):

			if condition == "random":
				if time.time() >= self.end_time + self.random_time:
					return True
				else: return False
			elif condition == "eyetracker":
				# print("self.start_time >= self.end_time: %s" %(self.start_time >= self.end_time))
				# print("(time.time() > self.end_time + 5): %s" %(time.time() > self.end_time + 5))
				# We should not measure or store the pupil size during an interruption or until 5 seconds after an interruption
				if not ((self.start_time >= self.end_time) or (time.time() < self.end_time + 5)):
					self.interrupt = eyetracker.check_wiv()
					if not self.interrupt: return False
					# When 30 seconds have passed we want to start over
					elif time.time() > self.end_time + 30:
						self.logger.log("30 seconds without interruptions have passed, interruption times have been reset")
						self.start_time = time.time()
						self.end_time = time.time() + 1 # +1 to ensure that end_time is bigger than start_time
						return False
				if self.interrupt: 
					self.interruption_started = True
					return True
				elif self.interruption_started:
					return True
		else: return False

	# Makes actual interruption
	def make_interruption(self,events,score):
		if self.mathprob == "Nothing":
			self.mathprob = self.mathprob_generator()
			self.cur_input = ""
			self.mathprobq = "What is "
			self.solved = None
			self.start_time = time.time()
			self.first = True
			self.logger.log("Interruption started")
			self.draw.init_keys()
		enter = 0
		enter,self.cur_input = self.draw.input(events,self.cur_input)
		# cur_input remains empty
		# print("interruption.make_interruption test. cur_input: %s" %cur_input)
		# print("interruption.make_interruption test. events: %s" %events)
		if enter:
			if self.cur_input == str(self.mathprob["ans"]):
				# log("self.rand: " + str(self.rand))
				# self.rand = random.randint(1,int(threshold))
				self.probs_solved += 1
				self.logger.log("Problem solved")
				# self.logger.log("Score = " + str(int(score)))
				self.solved = True
			else:
				self.logger.log("cur_input: " + self.cur_input)
				self.logger.log("ans: " + str(self.mathprob["ans"]))
				self.probs_failed += 1
				self.logger.log("Problem failed")
				# self.do_score()
				# self.logger.log("Score = " + str(int(score)))
				self.solved = False
		end = False
		if self.solved:
			# self.do_score()
			if self.first:
				self.first_time = time.time()
				self.fixed_score = score # We want to display a fixed score, not one that keeps updating
				self.first = False
			if time.time() < (self.first_time + 1):
				self.window.screen.fill(self.draw.blue)
				text = "Correct answer, score +100. Score: " + str(int(self.fixed_score+100))
				width,height = self.draw.pg.font.SysFont("Arial", 20).size(text)
				rtext = self.draw.pg.font.SysFont("Arial", 20).render(text, 1, (200, 200, 255))
				self.window.screen.blit(rtext, ((self.window.res_x/2)-(width/2),self.window.res_y/2-15))
			else: end = True

		elif (self.solved == False):
			# self.do_score()
			if self.first:
				self.first_time = time.time()
				self.fixed_score = score # We want to display a fixed score, not one that keeps updating
				self.first = False
			if time.time() < (self.first_time + 1.5):
				self.window.screen.fill(self.draw.blue)
				text = "Incorrect answer, score -400. Score: " + str(int(self.fixed_score-150))
				width,height = self.draw.pg.font.SysFont("Arial", 20).size(text)
				rtext = self.draw.pg.font.SysFont("Arial", 20).render(text, 1, (200, 200, 255))
				self.window.screen.blit(rtext, ((self.window.res_x/2)-(width/2),self.window.res_y/2-15))
			else: end = True
		else:
			self.draw.draw_interruption(self.mathprobq + str(self.mathprob["int1"]) + " " + str(self.mathprob["op"]) + " " + str(self.mathprob["int2"]) + "?","top")
			self.draw.draw_interruption("".join(self.cur_input),"bottom")
			return None

		if end:
			self.interruption_started = False
			self.random_time = random.randint(16,30)
			# self.last_interruption_time = time.time()
			self.mathprob = "Nothing"
			self.end_time = time.time()
			self.total_time = self.end_time - self.start_time
			# self.last_interruption_time = self.end_time
			self.logger.log("Interruption ended, interruption time: %.2f" %self.total_time)
			return self.total_time


	def mathprob_generator(self):
		# returns generated dictionary with a math problem and its anself.window.res_xer from two random ints and a random operator
		ops = {'+':operator.add,'-':operator.sub}
		int1 = random.randint(1,10)
		int2 = random.randint(10,90)
		op = random.choice(list(ops.keys()))
		if int2 >= int1:
			temp = int1
			int1 = int2
			int2 = temp
		ans = ops.get(op)(int1,int2)
		return {"int1":int1,"int2":int2,"op":op,"ans":ans}

