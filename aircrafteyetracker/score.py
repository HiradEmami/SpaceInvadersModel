class Score:
	
	def __init__(self):
		self.done = 0
		self.failed = 0
		self.ptime = 0
		
		self.points_landed = 100
		self.points_lost = -150
		self.points_correct = 100
		self.points_incorrect = -400
		# self.second_point = 0.1
	
 
	def calc(self,landed,lost,correct,incorrect,game_time,start_score):
		score = int(landed) * self.points_landed + int(lost) * self.points_lost + int(correct) * self.points_correct + int(incorrect) * self.points_incorrect

		# timebonus = -(game_time * self.second_point)
		# score = score + timebonus
		return score
