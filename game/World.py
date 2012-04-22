import pygame, random
from Game import Game
from Sprite import Sprite
from AnimatedSprite import AnimatedSprite
from ParallaxBackground import ParallaxBackground
from Enemy import FloatyTurp, BulletTurp

# World
class World:
	bg = None
	platforms = []
	tinyworlds = []
	enemies = []
	
	last_tinyworld = 0
	last_platform = 0
	
	def __init__( self ):
		
		self.bg = ParallaxBackground(
			"sprites/worlds/"+str(Game.level)+"/background-fore.png",
			"sprites/worlds/"+str(Game.level)+"/background-middle.png",
			"sprites/worlds/"+str(Game.level)+"/background-far.png",
			"sprites/worlds/"+str(Game.level)+"/background-back.png"
		)
		
		self.platforms.append( Platform( [(Game.screen_width/2)-50, 200] ) )
		#self.tinyworlds.append( TinyWorld( [random.randint(100, 800), random.randint(300, 600)] ) )
	
	def clearLevel( self ):
		for i in range(0, len(self.platforms)):
			self.platforms[i].kill( )
		
		for i in range(0, len(self.tinyworlds)):
			self.tinyworlds[i].kill( )
			
		for i in range(0, len(self.enemies)):
			self.enemies[i].kill( )
			
		self.platforms = []
		self.tinyworlds = []
		self.enemies = []
		self.last_tinyworld = 0
		self.last_platform = 0
	
	def clearBg( self ):
		for s in Game.sprites["background"]:
			s.kill( )
		#for i in range(0, len(self.bg.layers)):
		#	for t in range(0, len(self.bg.layers[i].tiles)):
		#		self.bg.layers[i].tiles[t].kill( )
		#	self.bg.layers[i].tile.kill( )
		self.bg.layers = []
		self.bg = None
	
	def resetLevel( self ):
		self.clearLevel( )
		self.platforms.append( Platform( [(Game.screen_width/2)-50, 200] ) )
		#self.tinyworlds.append( TinyWorld( [random.randint(100, 800), random.randint(300, 600)] ) )
	
	def update( self, player ):
		# update background
		self.bg.update( player )
		
		# randomly add baddies
		randomiser = random.randint( 0, 1000 )
		if randomiser <= 10:
			self.enemies.append( FloatyTurp( [Game.screen_width, random.randint(100, Game.screen_height - 100)] ) )
		
		if randomiser > 10 and randomiser <= 15:
			self.enemies.append( BulletTurp( [Game.screen_width, random.randint(100, Game.screen_height - 100)] ) )
		
		# Randomly add platforms and tiny worlds
		if player.pos[0] > Game.screen_width - Game.screen_move_x:
			if self.last_tinyworld == 0:
				if randomiser > 15 and randomiser <= 20:
					self.tinyworlds.append( TinyWorld( [random.randint(Game.screen_width, Game.screen_width * 2), random.randint(100, Game.screen_height - 100)] ) )
					self.last_tinyworld = 100
			else:
				self.last_tinyworld -= 1
				
			if self.last_platform == 0:
				if randomiser > 20 and randomiser <= 30:
					self.platforms.append( Platform( [random.randint(Game.screen_width, Game.screen_width * 2), random.randint(100, Game.screen_height - 100)] ) )
					self.last_platform = 100
			else:
				self.last_platform -= 1
		
		# move platforms
		for i in range(0, len(self.platforms)):
			if player.move_X < 0:
				if player.pos[0] < Game.screen_move_x:
					self.platforms[i].pos[0] -= player.move_X
			elif player.move_X > 0:
				if player.pos[0] > Game.screen_width - Game.screen_move_x:
					self.platforms[i].pos[0] -= player.move_X
		
		# move tiny worlds
		for i in range(0, len(self.tinyworlds)):
			if player.move_X < 0:
				if player.pos[0] < Game.screen_move_x:
					self.tinyworlds[i].pos[0] -= player.move_X
			elif player.move_X > 0:
				if player.pos[0] > Game.screen_width - Game.screen_move_x:
					self.tinyworlds[i].pos[0] -= player.move_X
		
		# move enemies
		for i in range(0, len(self.enemies)):
			if player.move_X < 0:
				if player.pos[0] < Game.screen_move_x:
					self.enemies[i].pos[0] -= player.move_X
			elif player.move_X > 0:
				if player.pos[0] > Game.screen_width - Game.screen_move_x:
					self.enemies[i].pos[0] -= player.move_X

# Platform
class Platform( Sprite ):
	pos = []
	
	def __init__( self, pos ):
		super( Platform, self ).__init__( pos, "sprites/worlds/"+str(Game.level)+"/platform-1.png", 5 )
		Game.addSprite( "world", self )
		
# Tiny World
class TinyWorld( AnimatedSprite ):
	image_angle = 1.0
	move_X = 0
	move_Y = 0
	
	def __init__( self, pos ):
		super( TinyWorld, self ).__init__( pos, "sprites/worlds/"+str(Game.level)+"/tiny-1.png", 9 )
		Game.addSprite( "tiny-worlds", self )
		
		self.addAnimState( "panic", 0, 3, 12 )
		
		self.setAnimState( "panic" )
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		# Move
		self.pos[0] += self.move_X
		self.pos[1] += self.move_Y
		
		if self.move_X > 0:
			self.move_X -= 0.025
		elif self.move_X < 0:
			self.move_X += 0.025
		
		if self.move_Y > 0:
			self.move_Y -= 0.025
		elif self.move_Y < 0:
			self.move_Y += 0.025
		
		# Animation
		self.updateAnim( ticks )
		
		# Draw
		screen.blit( self.image, self.rect )