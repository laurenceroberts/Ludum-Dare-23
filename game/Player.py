import pygame, math, random
from Game import Game
from AnimatedSprite import AnimatedSprite
from Sprite import Sprite

# Load sounds
pygame.mixer.init( )
sound_death = pygame.mixer.Sound( "sounds/scream.wav" )
sound_damage = pygame.mixer.Sound( "sounds/damage.wav" )

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
	
	death_wait = 0
	dead = False
	
	score = 0
	
	collisions = {'Platform': [], 'PaintSplat': [], 'FloatyTurp': [], 'BulletTurp': []}
	
	def __init__( self ):
		super( Player, self ).__init__( [Game.screen_width/2,50], "sprites/player/player-"+str(Game.level)+".png", 9 )
		Game.addSprite( "player", self )
		
		self.addAnimState( "idle",	0, 0, 1 )
		self.addAnimState( "move",	1, 4, 6 )
		
		self.setAnimState( "idle" )
		
		# Add weapons
		self.paintgun = PaintGun( [0,0] )
		self.hoover = Hoover( [0,0] )
		self.hoover.visible = False
		
		self.active_weapon = 'paintgun'
		
		self.target = PlayerWeaponTarget( [0,0] )
		self.target.weapon = self.active_weapon
		
	def clear( self ):
		self.kill( )
		self.paintgun.kill( )
		self.hoover.kill( )
		self.target.kill( )
		for i in range(0, len(self.paintgun.splats)):
			self.paintgun.splats[i].kill( )
		self.hoover.suction.kill( )

	def reset( self ):
		self.dead = False
		self.pos[0] = Game.screen_width/2
		self.pos[1] = 50
		self.move_X = 0
		self.move_Y = 0
		self.visible = True
		for i in range(0, len(self.paintgun.splats)):
			self.paintgun.splats[i].kill( )
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		# Kill player if falls down
		if self.dead == False and self.death_wait == 0 and self.pos[1] > Game.screen_height + self.rect.height:
			self.dead = True
			sound_death.play( )
			Game.lives -= 1
			
		
		if self.visible and self.dead == False:
			# Move
			if self.move_X < 0:
				if self.pos[0] > Game.screen_move_x:
					self.pos[0] += self.move_X
				else:
					for i in range(0, len(self.paintgun.splats)):
						self.paintgun.splats[i].pos[0] -= self.move_X
			elif self.move_X > 0:
				if self.pos[0] < Game.screen_width - Game.screen_move_x:
					self.pos[0] += self.move_X
				else:
					for i in range(0, len(self.paintgun.splats)):
						self.paintgun.splats[i].pos[0] -= self.move_X
			
			self.pos[1] += self.move_Y
			
			self.target.player_pos[0] = self.pos[0]
			self.target.player_pos[1] = self.pos[1]
			
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
			
			return ["check-collisions", ["world", "player-paint", "enemies"]]
		else:
			pass
	
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
			self.paintgun.visible = True
			self.hoover.visible = False
			self.paintgun.is_firing = True
			self.target.is_firing = True
		elif event.button == self.control_HOOVER:
			self.active_weapon = 'hoover'
			self.paintgun.visible = False
			self.hoover.visible = True
			self.hoover.is_firing = True
			self.target.is_firing = True
		
		self.target.weapon = self.active_weapon
	
	def mouseUpListener( self, event ):
		self.paintgun.is_firing = False
		self.hoover.is_firing = False
		self.target.is_firing = False
	
	def collisionsListener( self, collisions ):
		length = len( collisions )
		if length > 0:
			for i in range( 0, length ):
				self.collisions[collisions[i].__class__.__name__].append( collisions[i] )
		
	def physics( self ):
		if self.dead == False:
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
							if splat.state == "splat-idle":
								if splat.rect.y < self.rect.y + self.rect.height + 6: # player clipping splat
									self.pos[1] = splat.rect.y - self.rect.height + 6
									#self.pos[1] -= 1
							
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
			
			# Check enemies
			ftlength = len(self.collisions['FloatyTurp'])
			if ftlength > 0:
				for i in range(0, ftlength):
					turp = self.collisions['FloatyTurp'][i]
					
					self.move_X -= 1
					self.move_Y -= 1
					
					sound_damage.stop( )
					sound_damage.play( )
			
			btlength = len(self.collisions['BulletTurp'])
			if btlength > 0:
				for i in range(0, btlength):
					turp = self.collisions['BulletTurp'][i]
					
					self.move_X -= 2
					self.move_Y -= 2
					
					sound_damage.stop( )
					sound_damage.play( )
			
			move_max = 20
			if self.move_X > move_max:
				self.move_X = move_max
			elif self.move_X < -move_max:
				self.move_X = -move_max
			
			if self.move_Y > move_max:
				self.move_Y = move_max
			elif self.move_Y < -move_max:
				self.move_Y = -move_max
								
			self.collisions = {'Platform': [], 'PaintSplat': [], 'FloatyTurp': [], 'BulletTurp': []}

class PlayerWeapon( Sprite ):
	def __init__( self, pos, src ):
		super( PlayerWeapon, self ).__init__( pos, src, 10 )
		Game.addSprite( "player-weapon", self )
	
	def mouseMotionListener( self, event ):
		dx = float( event.pos[0] - self.pos[0] )
		dy = float( event.pos[1] - self.pos[1] )
		
		if dy == 0: dy = 0.01
		angle = math.degrees( math.atan2(dy, dx) )
		
		self.image = pygame.transform.rotate( self.origin_image, 360 - angle )

class PlayerWeaponTarget( Sprite ):
	weapon = None
	player_pos = [0,0]
	is_firing = False
	
	def __init__( self, pos ):
		super( PlayerWeaponTarget, self ).__init__( pos, "sprites/player/mouse.png", 10 )
		Game.addSprite( "player-weapon", self )
		
	def draw( self, screen, frame_ticks, ticks, fps ):
		self.pos[0], self.pos[1] = pygame.mouse.get_pos( )
		super( PlayerWeaponTarget, self ).draw( screen, frame_ticks, ticks, fps )
		if self.weapon == "hoover" and self.is_firing:
			return [ "check-collisions", "tiny-worlds" ]
	
	def collisionsListener( self, collisions ):
		length = len(collisions)
		if length:
			for i in range(0, length):
				dx = float( self.player_pos[0] - collisions[i].pos[0] )
				dy = float( self.player_pos[1] - collisions[i].pos[1] )
				
				if abs(dx) < 200 and abs(dy) < 200:
					
					if dy == 0: dy = 0.01
					a = 360 - math.atan2(dy, dx)
					
					speed = 2
					
					collisions[i].move_X = (speed * math.sin(a))
					collisions[i].move_Y = (speed * math.cos(a))
	
					collisions[i].image_angle += 5
					
					diffx = abs(collisions[i].pos[0] - self.player_pos[0])
					diffy = abs(collisions[i].pos[1] - self.player_pos[1])
					check = 20
					if diffx > -check and diffx < check and diffy > -check and diffy < check:
						collisions[i].kill( )
						Game.score += 1

class PaintGun( PlayerWeapon ):
	is_firing = False
	fire_rate = 100
	fire_last = 0
	splats = []
	
	def __init__( self, pos ):
		super( PaintGun, self ).__init__( pos, "sprites/player/paint-gun.png" )
	
	def updatePos( self, player_pos ):
		self.pos[0] = player_pos[0] + 2
		self.pos[1] = player_pos[1] + 26
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		if self.is_firing:
			if ticks - self.fire_last >= self.fire_rate:
				self.fire_last = ticks
				self.splats.append( PaintSplat( [self.pos[0], self.pos[1]], pygame.mouse.get_pos() ) )
		
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
		
		super( PaintSplat, self ).__init__( pos, "sprites/player/paint-splat-"+str(random.randint(1,6))+".png", 8 )
		Game.addSprite( "player-paint", self )
		
		self.addAnimState( "move", 0, 0, 1 )
		self.addAnimState( "splat-idle", 1, 1, 1 )
		self.addAnimState( "splat-drip", 2, 10, 4 )
		
		self.setAnimState( "move" )
		
		self.target = [target[0] - 24, target[1] - 24]
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		
		if self.target:
			# Apply gravity
			#self.target[1] += 5
			
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
				if self.pos[1] < 100: #instant drip if near top of screen
					self.age = 99
				else:
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
		
		
		if Game.outsideScreen( self.pos, self.rect ):
			if self.state == "move":
				#self.visible = False
				pass
			else:
				self.kill( )	
		
		if self.visible:	
			# Draw
			screen.blit( self.image, self.rect )
		
		return None

class Hoover( PlayerWeapon ):
	is_firing = False
	suction = None
	
	def __init__( self, pos ):
		super( Hoover, self ).__init__( pos, "sprites/player/hoover.png" )
		self.suction = HooverSuction( [pos[0], pos[1]] )
		self.suction.visible = False
	
	def updatePos( self, player_pos ):
		self.pos[0] = player_pos[0] + 2
		self.pos[1] = player_pos[1] + 26
		
		self.suction.pos[0] = player_pos[0] - 12
		self.suction.pos[1] = player_pos[1] - 12
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		if self.is_firing:
			self.suction.visible = True
		else:
			self.suction.visible = False
		
		return super( Hoover, self ).draw( screen, frame_ticks, ticks, fps )
	
class HooverSuction( AnimatedSprite ):
	def __init__( self, pos ):
		super( HooverSuction, self ).__init__( pos, "sprites/player/hoover-suction-2.png", 8 )
		Game.addSprite( "player-weapon", self )
		
		self.addAnimState( "suck", 0, 1, 12 )
		self.setAnimState( "suck" )

	def draw( self, screen, frame_ticks, ticks, fps ):
		if self.visible:
			# Animate
			self.updateAnim( ticks )
			
			# Draw
			screen.blit( self.image, self.rect )