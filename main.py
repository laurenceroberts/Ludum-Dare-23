# Un-named Project
# @compo Ludum Dare 23
# @theme Tiny World
# @author Gelatin Design, Laurence Roberts

# Defines
project_title = "Un-named Project"
screen_size = screen_width, screen_height = 1024, 600

# Initialise pygame
import pygame
pygame.init()

# Import game files
from game.Game import Game
from game.AnimatedSprite import AnimatedSprite
from game.TinyWorld import *
from game.Player import Player

# Setup screen
size = [ screen_width, screen_height ]
screen = pygame.display.set_mode( size )
pygame.display.set_caption( project_title )

# Start game
Game.addSpriteGroup( "world" )
Game.addSpriteGroup( "player" )

world = World( )
player = Player( )

Game.addSprite( "player", player )

# Define core colours
black = ( 0, 0, 0 )
white = ( 255, 255, 255 )
red   = ( 255, 0, 0 )
green = ( 0, 255, 0 )
blue  = ( 0, 0, 255 )

# Create clock
clock = pygame.time.Clock( )

# Main Program Loop flag
inLoop = True

# -------- Main Program Loop -----------
while inLoop:
	for event in pygame.event.get( ): # Catch user interactions
		if event.type == pygame.QUIT: # If user clicked close
			inLoop = False
			
		elif event.type == pygame.KEYDOWN:
			player.keyDownListener( event.key )
		
		elif event.type == pygame.KEYUP:
			player.keyUpListener( event.key )
			
		elif event.type == pygame.MOUSEBUTTONDOWN:
			player.mouseDownListener( event.button )
			
		elif event.type == pygame.MOUSEBUTTONUP:
			player.mouseUpListener( event.button )
	
	player.physics( )
	
	# Reset the screen
	screen.fill( white )
	
	# Render the game
	Game.render( screen, int(clock.get_time()), int(pygame.time.get_ticks()) )
	
	# Set clock rate to fps
	clock.tick( Game.fps )
	
	# Update the screen with drawn components
	pygame.display.flip( )

pygame.quit( )