import pygame

# BitmapFont
class BitmapFont( ):
	def __init__( self, image, chars ):
		self.src_image = pygame.image.load( image ).convert_alpha( )
		self.src_width, self.src_height = self.src_image.get_size( )
		self.images = []
		self.splitChars( chars[0], chars[1], chars[2] )
	
	def splitChars( self, chars, width, height ):
		self.chars = list(chars)
		self.charords = []
		
		for c in self.chars:
			self.charords.append( ord(str(c).lower()) )
		
		self.count_chars = len(self.chars)
		self.char_width = float(self.src_width) / float(width)
		self.char_height = float(self.src_height) / float(height)
		
		for h in range( height ):
			for w in range( width ):
				self.images.append( self.src_image.subsurface(float(w * self.char_width), float(h * self.char_height), self.char_width, self.char_height ) )
	
	def getChar( self, char ):
		o = ord(char)
		i = 0
		for c in self.charords:
			if c == o:
				return self.images[i]
			i += 1
		return self.images[0]

# BitmapText
class BitmapText( ):
	def __init__( self, font, pos ):
		self.setFont( font )
		self.setPos( pos )
		self.text = ""
		self.sprites = []
	
	def setFont( self, font ):
		self.font = font
	
	def setPos( self, pos ):
		self.pos = { 'x': pos[0], 'y': pos[1] }
	
	def setSurface( self, surface ):
		self.surface = surface
	
	def setText( self, text ):
		self.text = str(text)
		self.dirty = True
	
	def printText( self, text=None ):
		if text != self.text and text != None:
			self.setText( text )
			self.dirty = True
		
		if self.dirty:
			self.dirty = False
			
			text = self.text.lower( )
			chars = list(text)
			
			if len(self.sprites):
				for s in self.sprites:
					s.kill( )
			
			self.sprites = []
			
			x = self.pos['x']
			y = self.pos['y']
			
			i = 0
			for c in chars:
				s = pygame.sprite.Sprite( )
				s.image = self.font.getChar(c)
				s.rect = s.image.get_rect( )
				s.rect.x = x + (i * self.font.char_width) + (i*2)
				s.rect.y = y
				self.sprites.append( s )
				i += 1
			
		for s in self.sprites:
			self.surface.blit( s.image, s.rect )
	
	@staticmethod
	def echo( text, font, x, y ):
		pass