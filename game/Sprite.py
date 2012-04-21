import pygame

class Sprite( pygame.sprite.Sprite ):
	visible = True
	
	def __init__( self, pos, src ):
		super( Sprite, self ).__init__( )
		
		self.pos = pos
		
		self.image = pygame.image.load( src ).convert_alpha( )
		self.rect = self.image.get_rect( )
		self.src_width, self.src_height = self.image.get_size( )
	
	def draw( self, screen, frame_ticks, ticks, fps ):
		if self.visible:
			self.rect.x = self.pos[0]
			self.rect.y = self.pos[1]
			screen.blit( self.image, self.rect )