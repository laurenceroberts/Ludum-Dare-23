import pygame
from Sprite import Sprite
from Game import Game
import random

# Tiny World
class World:
	def __init__( self ):
		Platform( [100, 200], 4 )
		for i in range(0, 4):
			Platform( [random.randint(100, 800), random.randint(300, 600)], 4 )
		

# Platform
class Platform( Sprite ):
	pos = []
	
	def __init__( self, pos, size ):
		super( Platform, self ).__init__( pos, "sprites/worlds/water/platform-"+str(size)+".png" )
		Game.addSprite( "world", self )
		
		# Physics
		#self.physicsReactType = "force-move"
		#self.physicsReactTarget = [ "player", "enemy" ]
		#self.physicsReactForce = [ 0, 0, 0, 0 ] # stop all movement
		