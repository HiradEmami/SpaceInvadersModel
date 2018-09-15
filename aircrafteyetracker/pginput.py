import pygame as pg
class Input():
	def __init__(self):
		return

	def get_input(self,eyetracker):
		events = []
		event = pg.event.pump()
		if events is not None:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					# pg.quit()
					eyetracker.exit()
				events.append(event)

		keyinput = pg.key.get_pressed()
		if keyinput[pg.K_ESCAPE]:
			# pg.quit()
			eyetracker.exit()
		
		return (events,keyinput)