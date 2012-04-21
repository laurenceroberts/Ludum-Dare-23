import pygame, random
from Game import Game
from Sprite import Sprite
from AnimatedSprite import AnimatedSprite
from ParallaxBackground import ParallaxBackground

# World
class World:
	bg = None
	platforms = []
	
	def __init__( self ):
		
		self.bg = ParallaxBackground(
			"sprites/worlds/planet/background-fore.png",
			"sprites/worlds/planet/background-middle.png",
			"sprites/worlds/planet/background-far.png",
			"sprites/worlds/planet/background-back.png"
		)
		
		self.platforms.append( Platform( [600, 200], 4 ) )
		for i in range(0, 4):
			self.platforms.append( Platform( [random.randint(100, 800), random.randint(300, 600)], 4 ) )
		
		for i in range(0, 1):
			TinyWorld( [random.randint(100, 800), random.randint(300, 600)] )
	
	def update( self, player ):
		self.bg.update( player )
		for i in range(0, len(self.platforms)):
			if player.move_X < 0:
				if player.pos[0] < Game.screen_move_x:
					self.platforms[i].pos[0] -= player.move_X
			elif player.move_X > 0:
				if player.pos[0] > Game.screen_width - Game.screen_move_x:
					self.platforms[i].pos[0] -= player.move_X

# Platform
class Platform( Sprite ):
	pos = []
	
	def __init__( self, pos, size ):
		super( Platform, self ).__init__( pos, "sprites/worlds/planet/platform-1.png", 5 )
		Game.addSprite( "world", self )
		
		# Physics
		#self.physicsReactType = "force-move"
		#self.physicsReactTarget = [ "player", "enemy" ]
		#self.physicsReactForce = [ 0, 0, 0, 0 ] # stop all movement
		
# Tiny World
class TinyWorld( AnimatedSprite ):
	def __init__( self, pos ):
		super( TinyWorld, self ).__init__( pos, "sprites/worlds/planet/tiny-1.png", 9 )
		Game.addSprite( "tiny-worlds", self )
		
		self.addAnimState( "panic", 0, 3, 12 )
		
		self.setAnimState( "panic" )
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		# Move
		
		
		# Animation
		self.updateAnim( ticks )
		
		# Draw
		screen.blit( self.image, self.rect )