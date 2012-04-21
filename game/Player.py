import pygame, math
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
	
	paintgun = None
	hoover = None
	
	speed_X = 5
	speed_Y = 8
	accel_X = 0.4
	move_X = 0
	move_Y = 0
	
	collisions = {'Platform': []}
	
	def __init__( self ):
		super( Player, self ).__init__( [100,100], "sprites/player/player-green.png" )
		
		#self.addAnimState( "idle",	1, 1, 1 )
		self.addAnimState( "move",	0, 3, 6 )
		
		self.setAnimState( "move" )
		
		# Add weapons
		self.paintgun = PaintGun( [0,0] )
		self.hoover = Hoover( [0,0] )
		self.hoover.hide( )
		
		self.active_weapon = 'paintgun'
		
		# Add player feet collider
		#self.feet = PlayerFeet( self )
		#Game.addSprite( "player", self.feet )
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		# Move
		self.pos[0] += self.move_X
		self.pos[1] += self.move_Y
		
		# Update attached weapons
		self.paintgun.updatePos( self.pos )
		self.hoover.updatePos( self.pos )
		
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
			self.active_weapon = 'paintgun'
			self.paintgun.show( )
			self.hoover.hide( )
			self.paintgun.fire( )
		elif button == self.control_HOOVER:
			self.active_weapon = 'hover'
			self.paintgun.hide( )
			self.hoover.show( )
			self.hoover.fire( )
	
	def mouseUpListener( self, button ):
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


class PlayerWeapon( Sprite ):
	def __init__( self, pos, src ):
		super( PlayerWeapon, self ).__init__( pos, src )
		Game.addSprite( "player-weapon", self )
	
	def show( self ):
		self.visible = True
	
	def hide( self ):
		self.visible = False
	
	def mouseMotionListener( self, event ):
		dx = float( event.pos[0] - self.pos[0] )
		dy = float( event.pos[1] - self.pos[1] )
		
		if dy == 0: dy = 0.01
		angle = math.degrees( math.atan2(dy, dx) )
		
		self.image = pygame.transform.rotate( self.origin_image, 360 - angle )

class PaintGun( PlayerWeapon ):
	is_firing = False
	fire_rate = 200
	fire_last = 0
	
	def __init__( self, pos ):
		super( PaintGun, self ).__init__( pos, "sprites/player/paint-gun.png" )
	
	def updatePos( self, player_pos ):
		self.pos[0] = player_pos[0] + 2
		self.pos[1] = player_pos[1] + 26
	
	def fire( self ):
		self.is_firing = True
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		if ticks - self.fire_last >= self.fire_rate:
			self.fire_last = ticks
			
			print 'fire'
		
		return super( PaintGun, self ).draw( screen, frame_ticks, ticks, fps )

class Hoover( PlayerWeapon ):
	def __init__( self, pos ):
		super( Hoover, self ).__init__( pos, "sprites/player/hoover.png" )
	
	def updatePos( self, player_pos ):
		self.pos[0] = player_pos[0] + 2
		self.pos[1] = player_pos[1] + 26
	
	def fire( self ):
		pass
