"""
script that creates random flight names
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
import random

class rname:
	
	def __init__(self):
		self.doit = True

	
 
	def create(self):
		if (self.doit == True):	
			flightletters = "AA", "LH", "AC", "AI", "BA", "BL", "AB", "CZ", "EK", "EN", "FA", "GW", "AF", "IR", "JA", "KA", "KQ", "LD", "MY", "NZ", "N7", "OS", "LH", "QR", "RQ", "SK", "SQ", "TK", "UA", "VN", "X3", "YT", "QQ", "ZT" 
			fz = random.randint(1,33)
			fl = flightletters[fz]
			nz = random.randint(1000, 9999)
			nam = (fl + str(nz))
			return nam
