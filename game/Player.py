import pygame
from Game import Game
from AnimatedSprite import AnimatedSprite

# Player
class Player( AnimatedSprite ):
	control_LEFT = pygame.K_a
	control_RIGHT = pygame.K_d
	control_UP = pygame.K_w
	control_DOWN = pygame.K_s
	control_PAINT = 1
	control_HOOVER = 3
	
	speed_X = 5
	speed_Y = 8
	move_X = 0
	move_Y = 0
	
	collisions = {'Platform': []}
	
	def __init__( self ):
		super( Player, self ).__init__( [100,100], "sprites/player/player-green.png" )
		
		#self.addAnimState( "idle",	1, 1, 1 )
		self.addAnimState( "move",	0, 3, 6 )
		
		self.setAnimState( "move" )
	
	#def spriteRect( self ):
	#	r = self.image.get_rect( )
	#	return pygame.Rect( 20, 40, 5, 4 )
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		# Move
		self.pos[0] += self.move_X
		self.pos[1] += self.move_Y
		
		# Animation
		self.updateAnim( ticks )
		
		# Draw
		screen.blit( self.image, self.rect )
		
		return ["check-collisions", "world"]
	
	def keyDownListener( self, key ):
		if key == self.control_LEFT:
			#if self.move_Y == 0:
			self.move_X -= self.speed_X
		elif key == self.control_RIGHT:
			#if self.move_Y == 0:
			self.move_X += self.speed_X
		elif key == self.control_UP:
			if self.move_Y == 0:
				self.move_Y -= self.speed_Y
		elif key == self.control_DOWN:
			self.move_Y += self.speed_Y
	
	def keyUpListener( self, key ):
		if key == self.control_LEFT:
			#if self.move_Y == 0:
			self.move_X = 0
		elif key == self.control_RIGHT:
			#if self.move_Y == 0:
			self.move_X = 0
		elif key == self.control_UP:
			#self.move_Y += self.speed_Y
			pass
		elif key == self.control_DOWN:
			self.move_Y = 0
	
	def mouseDownListener( self, button ):
		if button == self.control_PAINT:
			print 'paint'
		elif button == self.control_HOOVER:
			print 'hoover'
	
	def mouseUpListener( self, button):
		pass
	
	def collisionsListener( self, collisions ):
		self.collisions = {'Platform': []}
		length = len( collisions )
		if length > 0:
			for i in range( 0, length ):
				self.collisions[collisions[i].__class__.__name__].append( collisions[i] )
	
	def physics( self ):
		
		# Apply gravity
		if self.move_Y < Game.gravity:
			self.move_Y += Game.gravity_a
			if self.move_Y > Game.gravity:
				self.move_Y = Game.gravity
		
		# Check platforms
		plength = len(self.collisions['Platform'])
		if plength > 0:
			if self.move_Y > 0:
				self.move_Y = 0
			