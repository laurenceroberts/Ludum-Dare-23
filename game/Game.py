import pygame

# Game
class Game:
	fps = 60
	frame = 1
	mode = "menu"
	sprites = { }
	gravity = 14
	gravity_a = 0.4
	
	score = 0
	score_required = 1
	level = 1
	real_level = 1
	max_level = 2
	
	def __init__( self ):
		pass
	
	# GAME
	@staticmethod
	def addSpriteGroup( name ):
		Game.sprites[ name ] = pygame.sprite.Group( )
	
	@staticmethod
	def addSprite( group, sprite ):
		Game.sprites[ group ].add( sprite )
		
	@staticmethod
	def outsideScreen( pos, rect ):
		if pos[0] < -rect.width or pos[0] > Game.screen_width or pos[1] < -rect.height or pos[1] > Game.screen_height:
			return True
		else:
			return False
	
	@staticmethod	
	def render( screen, frame_ticks, ticks ):
		#print len(Game.sprites["enemies"])
		
		Game.frame += 1
		if Game.frame > Game.fps:
			Game.frame = 1
		
		for zi in range(1, 11):
			for sg in Game.sprites:
				for s in Game.sprites[ sg ].sprites( ):
					if s.zindex == zi:
						r = s.draw( screen, frame_ticks, ticks, Game.fps )
						if r:
							if r[0] == 'sprite':
								Game.addSprite( r[1], r[2] )
							elif r[0] == 'sprites':
								for ns in r[2]:
									Game.addSprite( r[1], ns )
							elif r[0] == 'check-collisions':
								#collisions = pygame.sprite.spritecollideany( s, self.sprites[r[1]] )
								#if r[1] == 'player':
								#collisions = pygame.sprite.spritecollide( s, self.sprites[r[1]], False, pygame.sprite.collide_circle_ratio(0.3) )
								#else:
								if isinstance(r[1], basestring) == True:
									collisions = pygame.sprite.spritecollide( s, Game.sprites[r[1]], False )
									s.collisionsListener( collisions )
								else:
									for cg in r[1]:
										collisions = pygame.sprite.spritecollide( s, Game.sprites[cg], False )
										s.collisionsListener( collisions )
		
		#if self.terrain.redraw == True:
			#self.terrain.generate( self.terrain.tilesize['x'], 1, 'prepend' )