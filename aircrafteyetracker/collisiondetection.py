"""
collision detection module
Copyright (C) 2010  Julian Wienand

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

import math

class CollDetec:
	
	def __init__(self):
	# 	self.dis = 1
		return

	
	# def iscollision(self, x1, y1, x2, y2):
		
	# 	realdis = math.sqrt(((x1 - x2) * (x1 - x2)) + ((y1 - y2) * (y1 - y2)))

	# 	return realdis < self.dis
		
	def get_distance(self, x1, y1, x2, y2):
		
		realdis = math.sqrt(((x1 - x2) * (x1 - x2)) + ((y1 - y2) * (y1 - y2)))

		return realdis
			

		
	
