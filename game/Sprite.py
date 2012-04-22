import pygame
from Game import Game

class Sprite( pygame.sprite.Sprite ):
	visible = True
	zindex = 1
	
	def __init__( self, pos, src, zindex = 1 ):
		super( Sprite, self ).__init__( )
		
		self.pos = pos
		self.zindex = zindex

		self.src = src		
		self.image = pygame.image.load( src ).convert_alpha( )
		self.origin_image = self.image
		self.rect = self.image.get_rect( )
		self.src_width, self.src_height = self.image.get_size( )
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		#if Game.outsideScreen( self.pos, self.rect ):
		#	self.visible = False
		#else:
		#	self.visible = True
		
		if self.visible:
			self.rect = self.image.get_rect( )
			
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
			screen.blit( self.image, self.rect )