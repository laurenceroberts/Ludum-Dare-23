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
	speed_Y = 12
	accel_X = 0.4
	move_X = 0
	move_Y = 0
	
	collisions = {'Platform': [], 'PaintSplat': []}
	
	def __init__( self ):
		super( Player, self ).__init__( [100,100], "sprites/player/player-green.png" )
		
		self.addAnimState( "idle",	0, 0, 1 )
		self.addAnimState( "move",	1, 4, 6 )
		
		self.setAnimState( "idle" )
		
		# Add weapons
		self.paintgun = PaintGun( [0,0] )
		self.hoover = Hoover( [0,0] )
		self.hoover.hide( )
		
		self.active_weapon = 'paintgun'
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		# Move
		self.pos[0] += self.move_X
		self.pos[1] += self.move_Y
		
		# Update attached weapons
		self.paintgun.updatePos( self.pos )
		self.hoover.updatePos( self.pos )
		
		# Animation
		if self.move_X != 0 or self.move_Y != 0:
			self.setAnimState( "move" )
		else:
			self.setAnimState( "idle" )
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
	
	def mouseDownListener( self, event ):
		if event.button == self.control_PAINT:
			self.active_weapon = 'paintgun'
			self.paintgun.show( )
			self.hoover.hide( )
			self.paintgun.is_firing = True
		elif event.button == self.control_HOOVER:
			self.active_weapon = 'hover'
			self.paintgun.hide( )
			self.hoover.show( )
			self.hoover.is_firing = True
	
	def mouseUpListener( self, event ):
		if event.button == self.control_PAINT:
			self.paintgun.is_firing = False
		elif event.button == self.control_HOOVER:
			self.hoover.is_firing = False
	
	def collisionsListener( self, collisions ):
		self.collisions = {'Platform': [], 'PaintSplat': []}
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
		# Check splats
		slength = len(self.collisions['PaintSplat'])
		if slength > 0:
			for i in range(0, slength):
				splat = self.collisions['PaintSplat'][i]
				
				if splat.state != "move":
					if splat.rect.y > self.rect.y: # splat underneath
						#if splat.rect.y < self.rect.y + self.rect.height: # player clipping splat
						#	self.pos[1] = splat.rect.y - self.rect.height + 1
						
						if splat.state == "splat-idle":
							if self.move_Y > 0:
								self.move_Y = 0
						else:
							if self.move_Y > 1:
								self.move_Y = 1
					else: # splat above
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
	fire_rate = 100
	fire_last = 0
	
	def __init__( self, pos ):
		super( PaintGun, self ).__init__( pos, "sprites/player/paint-gun.png" )
	
	def updatePos( self, player_pos ):
		self.pos[0] = player_pos[0] + 2
		self.pos[1] = player_pos[1] + 26
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		if self.is_firing:
			if ticks - self.fire_last >= self.fire_rate:
				self.fire_last = ticks
				PaintSplat( [self.pos[0], self.pos[1]], pygame.mouse.get_pos() )
		
		return super( PaintGun, self ).draw( screen, frame_ticks, ticks, fps )
	
class PaintSplat( AnimatedSprite ):
	speed = 20
	move_X = 0
	move_Y = 0
	
	target = None
	
	age = 0
	
	def __init__( self, pos, target ):
		pos[0] -= 0
		pos[1] -= 16
		
		super( PaintSplat, self ).__init__( pos, "sprites/player/paint-splat.png" )
		Game.addSprite( "world", self )
		
		self.addAnimState( "move", 0, 0, 1 )
		self.addAnimState( "splat-idle", 1, 1, 1 )
		self.addAnimState( "splat-drip", 2, 10, 4 )
		
		self.setAnimState( "move" )
		
		self.target = [target[0] - 24, target[1] - 24]
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		# Apply gravity
		#if self.move_Y < Game.gravity:
		#	self.move_Y += ( Game.gravity_a / 4 )
		#	if self.move_Y > Game.gravity:
		#		self.move_Y = Game.gravity
		
		if self.target:
			dx = float( self.target[0] - self.pos[0] )
			dy = float( self.target[1] - self.pos[1] )
			if dy == 0: dy = 0.01
			a = 360 - math.atan2(dy, dx)
			
			self.move_X = (self.speed * math.sin(a))
			self.move_Y = (self.speed * math.cos(a))
			
			# Move
			self.pos[0] += self.move_X
			self.pos[1] += self.move_Y
			
			near_x = abs(self.pos[0] - self.target[0])
			near_y = abs(self.pos[1] - self.target[1])
			check = 10
			if near_x > -check and near_x < check and near_y > -check and near_y < check:
				self.target = None
				self.setAnimState( "splat-idle" )
				self.age = 1
			
			self.updateAnim( ticks )
		
		if self.age > 0:
			self.age += 1
			
			if self.state == "splat-drip" and self._frame == 10:
				self.kill( )
			else:
				self.updateAnim( ticks )
			
			if self.age == 100:
				self.setAnimState( "splat-drip" )
		
		# Draw
		screen.blit( self.image, self.rect )
		
		return None

class Hoover( PlayerWeapon ):
	def __init__( self, pos ):
		super( Hoover, self ).__init__( pos, "sprites/player/hoover.png" )
	
	def updatePos( self, player_pos ):
		self.pos[0] = player_pos[0] + 2
		self.pos[1] = player_pos[1] + 26
