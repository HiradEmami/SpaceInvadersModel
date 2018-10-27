class Map:
	def __init__(self):
		self.runways = []
		self.runways.append(Runway(812,601,1300,4))
		self.runways.append(Runway(780,641,1300,1))

class Runway:
	def __init__(self,x_coord,y_coord,height,direction):
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.height = height
		self.direction = direction
