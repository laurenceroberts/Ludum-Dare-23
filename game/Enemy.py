import pygame

# Enemy
class Enemy( AnimatedSprite ):
	def __init__( self, pos, src ):
		super( Enemy, self ).__init__( pos, src )

# Turpentine Baddies
class FloatyTurp( Enemy ):
	def __init__( self, pos ):
		super( FloatyTurp, self ).__init__( pos, "sprites/enemies/turp-1.png" )
		
		self.addAnimState( "move", 0, 3, 6 )
		self.setAnimState( "move" )