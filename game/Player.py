import pygame

# Player
class Player:
	control_LEFT = pygame.K_LEFT
	control_RIGHT = pygame.K_RIGHT
	control_UP = pygame.K_UP
	control_DOWN = pygame.K_DOWN
	control_PAINT = 1
	control_HOVER = 3
	
	def __init__( self ):
		pass
	
	def keyDownListener( self, key ):
		if key == self.control_LEFT:
			print 'left'
		elif key == self.control_RIGHT:
			print 'right'
		elif key == self.control_UP:
			print 'up'
		elif key == self.control_DOWN:
			print 'down'
	
	def keyUpListener( self, key ):
		pass
	
	def mouseDownListener( self, button ):
		if button == self.control_PAINT:
			print 'paint'
		elif button == self.control_HOVER:
			print 'hover'
	
	def mouseUpListener( self, button):
		pass
	
	def physics( ):
		pass
		