import pygame, math
from Game import Game
from Sprite import Sprite

# Parallax Background
class ParallaxBackground:
	layers = []
	
	def __init__( self, fore, middle, far, back ):
		self.layers = []
		self.layers.append( BackgroundLayer( back, 1, True, 0.25 ) )
		self.layers.append( BackgroundLayer( far, 2, False, 0.5 ) )
		self.layers.append( BackgroundLayer( middle, 3, False, 1.5 ) )
		self.layers.append( BackgroundLayer( fore, 4, False, 3.0 ) )
	
	def update( self, player ):
		for layer in self.layers:
			layer.update( player )
		
class BackgroundLayer:
	tile = None
	tiles = []
	scroll_adjust = 1
	move_X = 0
	
	def __init__( self, src, zindex, repeat_y, scroll_adjust ):
		self.tile = Sprite( [0,0], src, zindex )
		self.tiles = []
		
		self.scroll_adjust = float(scroll_adjust)
		self.bgsrc = src
		self.zindex = zindex
		
		count_x = int( math.ceil( float(Game.screen_width) / float(self.tile.rect.width) ) )
		if repeat_y:
			count_y = int( math.ceil( float(Game.screen_height) / float(self.tile.rect.height) ) )
		else:
			count_y = 1
		
		self.count_x = count_x
		self.count_y = count_y
		
		for x in range(0, count_x):
			for y in range(0, count_y):
				self.tiles.append( Sprite( [x*self.tile.rect.width, Game.screen_height - (y+1)*self.tile.rect.height], src, zindex ) )
				Game.addSprite( "background", self.tiles[len(self.tiles)-1] )
	
	def update( self, player ):
		if player.move_X != 0:
			if player.pos[0] < Game.screen_move_x or player.pos[0] > Game.screen_width - Game.screen_move_x:
				if player.move_X > 0:
					move_X = self.scroll_adjust
				else:
					move_X = -self.scroll_adjust
				
				if move_X > -1 and move_X < 1:
					self.move_X += move_X
				else:
					self.move_X = move_X
				
				far_left = Game.screen_width + 1
				far_right = -1
				
				for i in range(0, len(self.tiles)):
					if self.tiles[i].pos[0] <  -self.tiles[i].rect.width:
						self.tiles[i].kill( )
						self.tiles[i].remove
					
				if self.move_X <= -1 or self.move_X >= 1:
					for i in range(0, len(self.tiles)):
						self.tiles[i].pos[0] -= int( self.move_X )
						
						if self.tiles[i].pos[0] < far_left:
							far_left = self.tiles[i].pos[0]
						if self.tiles[i].pos[0] > far_right:
							far_right = self.tiles[i].pos[0]
						
					self.move_X = 0
					
					if far_left > 0:
						for y in range(0, self.count_y):
							self.tiles.append( Sprite( [far_left - self.tile.rect.width, Game.screen_height - (y+1)*self.tile.rect.height], self.bgsrc, self.zindex ) )
							Game.addSprite( "background", self.tiles[len(self.tiles)-1] )
					if far_right < Game.screen_width - self.tile.rect.width:
						for y in range(0, self.count_y):
							#print self.bgsrc
							self.tiles.append( Sprite( [far_right + self.tile.rect.width, Game.screen_height - (y+1)*self.tile.rect.height], self.bgsrc, self.zindex ) )
							Game.addSprite( "background", self.tiles[len(self.tiles)-1] )