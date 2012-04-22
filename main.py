# Un-named Project
# @compo Ludum Dare 23
# @theme Tiny World
# @author Gelatin Design, Laurence Roberts

# Defines
project_title = "Un-named Project"
screen_size = screen_width, screen_height = 1280, 768

# Initialise pygame
import pygame, pygame._view
pygame.init()

# Import game files
from game.Game import Game
from game.AnimatedSprite import AnimatedSprite
from game.World import *
from game.Player import Player
from game.BitmapFont import *

# Setup screen
size = [ screen_width, screen_height ]
screen = pygame.display.set_mode( size )
pygame.display.set_caption( project_title )

# Load fonts
font_1 = BitmapFont( "fonts/accent_36.png", ["ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ", 8, 5] )
font_2 = BitmapFont( "fonts/accent_36_red.png", ["ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ", 8, 5] )

# Start game
Game.screen_width = screen_width
Game.screen_height = screen_height

Game.screen_move_x = Game.screen_width / 2.2

Game.addSpriteGroup( "background" )
Game.addSpriteGroup( "world" )
Game.addSpriteGroup( "tiny-worlds" )
Game.addSpriteGroup( "enemies" )
Game.addSpriteGroup( "player" )
Game.addSpriteGroup( "player-weapon" )
Game.addSpriteGroup( "player-paint" )

score_text = BitmapText( font_1, [20, 20] )
score_text.setSurface( screen )

level_text = BitmapText( font_1, [Game.screen_width - 200, 20] )
level_text.setSurface( screen )

dead_text = BitmapText( font_2, [(Game.screen_width / 2)-50, 100] )
dead_text.setSurface( screen )

restart_text = BitmapText( font_2, [(Game.screen_width / 2)-200, 200] )
restart_text.setSurface( screen )

Game.level = 1

world = World( )
player = Player( )

pygame.mouse.set_visible( False )

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
			player.mouseDownListener( event )
			
		elif event.type == pygame.MOUSEBUTTONUP:
			player.mouseUpListener( event )
			
		elif event.type == pygame.MOUSEMOTION:
			#if player.paintgun.visible:
			player.paintgun.mouseMotionListener( event )
			#elif player.hoover.visible:
			player.hoover.mouseMotionListener( event )
	
	# Player physics
	player.physics( )
	
	# Reset the screen
	screen.fill( white )
	
	# Render the game
	world.update( player )
	Game.render( screen, int(clock.get_time()), int(pygame.time.get_ticks()) )
	
	# Print text
	score_text.printText( "Collected " + str(Game.score) + " of " + str(Game.score_required) )
	level_text.printText( "Level " + str(Game.real_level) )
	if player.dead:
		dead_text.printText( "You died" )
		restart_text.printText( "Click to restart level" )
		
		Game.score = 0
		
		pressed = pygame.mouse.get_pressed()
		if pressed[0] or pressed[2]:
			world.resetLevel( )
			player.reset( )
	else:
		if Game.score >= Game.score_required:
			Game.score = 0
			#Game.score_required += 1
			Game.level += 1
			Game.real_level += 1
			
			if Game.level > Game.max_level:
				Game.level = 1
			
			world.clearLevel( )
			world.clearBg( )
			world = None
			world = World( )
			player.clear( )
			player = Player( )
	
	# Set clock rate to fps
	clock.tick( Game.fps )
	
	# Update the screen with drawn components
	pygame.display.flip( )

pygame.quit( )