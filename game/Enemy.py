import pygame, math, random
from Game import Game
from AnimatedSprite import AnimatedSprite

# Enemy
class Enemy( AnimatedSprite ):
	def __init__( self, pos, src ):
		super( Enemy, self ).__init__( pos, src, 9 )
		Game.addSprite( "enemies", self )

# Turpentine Baddies
class FloatyTurp( Enemy ):
	speed_X = 6
	
	angle = 0
	angle_speed = 4
	angle_size = 10
	
	def __init__( self, pos ):
		super( FloatyTurp, self ).__init__( pos, "sprites/enemies/turp-1.png" )
		
		self.addAnimState( "move", 0, 3, 6 )
		self.setAnimState( "move" )
		
		self.angle = random.randint(0, 359)
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		# Move	
		self.angle += self.angle_speed
		if self.angle > 359:
			self.angle = 0
		
		self.pos[0] -= self.speed_X
		self.pos[1] += ( self.angle_size * math.sin( math.radians(self.angle) ) )
		
		# Animation
		self.updateAnim( ticks )
		
		if Game.outsideScreen( self.pos, self.rect ):
			self.visible = False
		else:
			self.visible = True
		
		if self.pos[0] < -self.rect.width:
			self.kill( )
		
		if self.visible:
			# Draw
			screen.blit( self.image, self.rect )
		
		return [ "check-collisions", "player-paint" ]
	
	def collisionsListener( self, collisions ):
		length = len(collisions)
		if length > 0:
			for i in range(0, length):
				if collisions[i].state == "splat-idle":
					collisions[i].setAnimState( "splat-drip" )

class BulletTurp( Enemy ):
	speed_X = 10
	
	angle = 0
	angle_speed = 8
	angle_size = 1
	
	def __init__( self, pos ):
		super( BulletTurp, self ).__init__( pos, "sprites/enemies/turp-2.png" )
		
		self.addAnimState( "move", 0, 3, 6 )
		self.setAnimState( "move" )
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		# Move	
		self.angle += self.angle_speed
		if self.angle > 359:
			self.angle = 0
		
		self.pos[0] -= self.speed_X
		self.pos[1] += ( self.angle_size * math.sin( math.radians(self.angle) ) )
		
		# Animation
		self.updateAnim( ticks )
		
		if Game.outsideScreen( self.pos, self.rect ):
			self.visible = False
		else:
			self.visible = True
		
		if self.pos[0] < 0:
			self.kill( )
		
		if self.visible:
			# Draw
			screen.blit( self.image, self.rect )