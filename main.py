# Un-named Project
# @compo Ludum Dare 23
# @theme Tiny World
# @author Gelatin Design, Laurence Roberts

# Load preferences
prefs_file = open( "prefs.txt", 'r' )
prefs_s = prefs_file.read().split("\n");
prefs = { }
for p in prefs_s:
	pref = p.split(" ")
	prefs[pref[0]] = pref[1]

# Defines
project_title = "I Painted a Tiny World"
screen_size = screen_width, screen_height = int(prefs["screen_width"]), int(prefs["screen_height"])

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
pygame.display.set_icon( pygame.image.load( "icon.png" ).convert_alpha( ) )

screen.convert( )

# Load fonts
font_1 = BitmapFont( "fonts/accent_36.png", ["ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ", 8, 5] )
font_2 = BitmapFont( "fonts/accent_36_red.png", ["ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ", 8, 5] )

# Load music
pygame.mixer.init( )
music = []
music.append( pygame.mixer.Sound( "sounds/music-1.wav" ) )
music.append( pygame.mixer.Sound( "sounds/music-2.wav" ) )
music.append( pygame.mixer.Sound( "sounds/music-3.wav" ) )

music_track = 0
music[music_track].play( )

music_length = music[music_track].get_length( )
music_length_played = 0.0
music_start_time = 0

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

game_start_text1 = BitmapText( font_2, [(Game.screen_width / 2)-300, 50] )
game_start_text1.setSurface( screen )
game_start_text2 = BitmapText( font_1, [(Game.screen_width / 2)-300, 100] )
game_start_text2.setSurface( screen )
game_start_text3 = BitmapText( font_1, [(Game.screen_width / 2)-300, 260] )
game_start_text3.setSurface( screen )

score_text = BitmapText( font_1, [20, 20] )
score_text.setSurface( screen )

level_text = BitmapText( font_1, [Game.screen_width - 200, 20] )
level_text.setSurface( screen )

lives_text = BitmapText( font_2, [Game.screen_width - 200, 50] )
lives_text.setSurface( screen )

gameover_text = BitmapText( font_1, [(Game.screen_width / 2)-300, 100] )
gameover_text.setSurface( screen )

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
	
	# Update music
	if clock.get_time() < Game.fps:
		#print pygame.time.get_ticks() / 1000
		
		music_length_played = (pygame.time.get_ticks() / 1000) - music_start_time
		
		if music_length_played >= music_length - 6: # fade out last 10 seconds
			music[music_track].fadeout( 5000 )
		
		if music_length_played >= music_length - 5:
			music_track += 1
			if music_track > len(music) - 1:
				music_track = 0
			music_start_time = pygame.time.get_ticks() / 1000
			music[music_track].play(0, 0, 3000)
			music_length = music[music_track].get_length( )	
	
	# Reset the screen
	screen.fill( white )	
			
	# Menu or Game
	if Game.mode == "menu":
		Game.render( screen, int(clock.get_time()), int(pygame.time.get_ticks()) )
		
		game_start_text1.printText( "I painted a tiny world" )
		game_start_text2.printText( "Click to play" )
		game_start_text3.printText( "by gelatin design" )
		
		player.visible = False
		player.paintgun.visible = False
		player.hoover.visible = False
		
		
		pressed = pygame.mouse.get_pressed()
		if pressed[0] or pressed[2]:
			Game.mode = "game"
			player.visible = True
			player.paintgun.visible = True
	else:		
		
		# Player physics
		player.physics( )
		
		# Render the game
		world.update( player )
		Game.render( screen, int(clock.get_time()), int(pygame.time.get_ticks()) )
		
		# Print text
		score_text.printText( "Collected " + str(Game.score) + " of " + str(Game.score_required) )
		level_text.printText( "Level " + str(Game.real_level) )
		lives_text.printText( "Lives " + str(Game.lives) )
		
		if player.dead:
			if Game.lives < 0:
				gameover_text.printText( "You collected " + str(Game.score) + " tiny worlds")
				restart_text.printText( "Spacebar to play again" )
				Game.level = 1
				Game.real_level = 1
				Game.score_required = 1
				Game.score_level = 0
				pressed = pygame.key.get_pressed()
				if pressed[pygame.K_SPACE]:
					Game.score = 0
					Game.lives = 3
					world.clearLevel( )
					world.clearBg( )
					world = None
					world = World( )
					player.clear( )
					player = Player( )
				
			else:
				dead_text.printText( "You died" )
				restart_text.printText( "Spacebar to restart level" )
				Game.score = Game.score_level
				Game.score_required_inc = 1
				pressed = pygame.key.get_pressed()
				if pressed[pygame.K_SPACE]:
					world.resetLevel( )
					player.reset( )
		else:
			if Game.score >= Game.score_required:
				#Game.score = 0
				Game.score_required_inc += 1
				Game.score_required += Game.score_required_inc
				Game.score_level = Game.score
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
	
	#print clock.get_fps( )
	
	# Update the screen with drawn components
	pygame.display.flip( )

pygame.quit( )