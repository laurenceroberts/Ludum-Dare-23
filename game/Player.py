import pygame
from Game import Game
from AnimatedSprite import AnimatedSprite
from Sprite import Sprite

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
	accel_X = 0.4
	move_X = 0
	move_Y = 0
	
	feet = None
	
	collisions = {'Platform': []}
	
	def __init__( self ):
		super( Player, self ).__init__( [100,100], "sprites/player/player-green.png" )
		
		#self.addAnimState( "idle",	1, 1, 1 )
		self.addAnimState( "move",	0, 3, 6 )
		
		self.setAnimState( "move" )
		
		# Add player feet collider
		#self.feet = PlayerFeet( self )
		#Game.addSprite( "player", self.feet )
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		# Move
		self.pos[0] += self.move_X
		self.pos[1] += self.move_Y
		
		#self.feet.update( )
		
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
			for i in range(0, plength):
				platform = self.collisions['Platform'][i]
				
				if platform.rect.y > self.rect.y: # platform underneath
					if platform.rect.y < self.rect.y + self.rect.height: # player clipping platform
						self.pos[1] = platform.rect.y - self.rect.height + 1
						#self.move_Y = self.move_Y * 0.5
					
					if self.move_Y > 0:
						self.move_Y = 0
				else: # platform above
					if self.move_Y < 0:
						pass
						#self.move_Y = 0
				
'''
class PlayerFeet( Sprite ):
	player = None
	
	def __init__( self, player ):
		#self.rect = pygame.Rect( 0, 0, 10, 4 )
		super( PlayerFeet, self ).__init__( [0,0], "sprites/player/player-feet.png" )
		
		self.player = player
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		super( PlayerFeet, self ).draw( screen, frame_ticks, ticks, fps )
		return ["check-collisions", "world"]
	
	def update( self ):
		self.pos[0] = self.player.pos[0] + 4
		self.pos[1] = self.player.pos[1] + 45
		
	def collisionsListener( self, collisions ):
		self.player.collisions = {'Platform': []}
		length = len( collisions )
		print collisions
		if length > 0:
			for i in range( 0, length ):
				self.player.collisions[collisions[i].__class__.__name__].append( collisions[i] )
'''