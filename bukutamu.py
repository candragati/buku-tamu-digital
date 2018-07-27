# source code inputbox berdasarkan http://code.google.com/p/python-vnc-viewer/
# dimodifikasi oleh candragati@gmail.com untuk proyek pribadi di bulan Agustus 2013.

# file yang harus ada di satu folder yang sama adalah 
# 1. Filxgirl.TTF (font yg digunakan)
# 2. FILE586.JPG (gambar pemberitahuan tidak ada hasil capture kamera)

" This demonstrates how to show an input box on screen and get the player name."
" By Barberic http://web.aanet.com.au/~barberic/"
" with thanks for help from mgibsonbr on stackoverflow.com"

import pygame, sys, os
import pygame.camera
from pygame.locals import *
from time import *

#os.environ['SDL_VIDEODRIVER']='windib' #uncomment apabila terjadi error : No available video device
os.environ['SDL_VIDEO_CENTERED'] = '0'  # pygame tampil di tengah dekstop

pygame.font.init()

DEVICE='/dev/video1'

SCREENWIDTH = 800
SCREENHEIGHT = 600
SIZE=(SCREENWIDTH,SCREENHEIGHT)
tampil = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT),pygame.FULLSCREEN) 
#tampil = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT),0) #apabila ingin fullscreen, samakan dengan baris diatasnya

BASICFONT = pygame.font.Font('Filxgirl.TTF', 35, bold = False, italic=False) # download font http://img.dafont.com/dl/?f=fiolex_girls
TEXTFONT = pygame.font.Font('Filxgirl.TTF', 55, bold = False, italic=False)
WHITE     = (55, 255, 255)
BLACK     = (  0,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  100, 20,  10)
FILE = ''

def camstream():
	pygame.init()
	pygame.font.init()
	pygame.camera.init()
	
	kamera = pygame.camera.Camera(DEVICE, SIZE)
	
	kamera.start()
	layar = pygame.surface.Surface((640,480), 10, tampil)
	capture = True
	
	#windowSurface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT),0)
	windowSurface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT),pygame.FULLSCREEN)
		
	tulis=BASICFONT.render('Selamat Datang...',False,WHITE)
	posisi=tulis.get_rect()
	posisi.bottomleft = (10,450)
	
	while capture:
		layarkamera = kamera.get_image(layar)
		tampil.blit(layarkamera, (80,60)) #posisi preview kamera
		windowSurface.blit(tulis,posisi)
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == QUIT:
				capture = False
			elif event.type == KEYDOWN and event.key == K_RETURN:
				kamera.stop()
				FILE=pygame.image.save(layarkamera, 'simpan.jpg')
				main('Tekan Enter untuk menulis data.') 
				capture = False				
			elif event.type == KEYDOWN and event.key ==K_ESCAPE:
				capture = False
			elif event.type == KEYDOWN and event.key == K_f:
				pygame.display.toggle_fullscreen()			
	kamera.stop()
	pygame.quit()
	return

def main(msg):		
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()				
			elif event.type == KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					terminate()					
				elif event.key == pygame.K_RETURN:
					getname()
					
					#cek ada tidaknya file hasil tangkapan kamera
					if os.path.isfile('simpan.jpg') == True:
						os.remove('simpan.jpg')
					else:
						pass
						
				elif event.key == K_f:
					pygame.display.toggle_fullscreen()
				elif event.key == K_c:
					camstream()
		
		pygame.draw.rect(tampil, DARKGREEN, (00, 520, 1024, 80)) 
		spaceSurf = BASICFONT.render(msg, True, WHITE)
		spaceRect = spaceSurf.get_rect()
		spaceRect.midtop = (SCREENWIDTH / 2, SCREENHEIGHT - 80)
		tampil.blit(spaceSurf, spaceRect)
		pygame.display.update()

def getname():
	name = ask("Nama ")
	alamat = ask("alamat")
	img_cam = ""
	FONT = pygame.font.Font('Filxgirl.TTF', 42, bold = False, italic=False)
	
	# cek ketersediaan file capture
	if os.path.isfile('simpan.jpg') == False:
		sambutan = 'tidak ada gambar kamera, silahkan tekan C'
		pygame.draw.rect(tampil,GREEN,(10,100,100,10))
		img_cam = "FILE586.JPG"
	else:
		ambilgambar = pygame.image.load('simpan.jpg')		
		sambutan = ''
		if (name == "") or (alamat == ""):
			sambutan = 'mohon data diisi yang lengkap'
		else:
			JAM = strftime("%H%M%S")
			pygame.image.save(ambilgambar, JAM + '_' + name + '_'+ alamat +'.jpg')			
			sambutan = 'Selamat Datang '+ name +' dari '+ alamat
			
		img_cam = "simpan.jpg"

	tampil.fill(BLACK)	
	bg = pygame.image.load(img_cam)
	tampil.blit(bg,(80,60))
	pygame.display.flip()
	nameSurf = FONT.render(sambutan, True, WHITE)
	nameRect = nameSurf.get_rect()
	nameRect.midtop = (SCREENWIDTH / 2, 50)
	tampil.blit(nameSurf, nameRect)
	pygame.display.update()

def ask(question):
	"ask(question) -> answer"
	current_string = ""
	display_box(question + ": (max 32 char)" + current_string)
	while 1:
		(inkey, unichr) = get_key()

		if inkey == K_BACKSPACE:  # remove last char
			current_string = current_string[:-1]
		elif inkey == K_RETURN or inkey == K_KP_ENTER:
			break   # break out of the while loop to return current_string
		elif inkey == pygame.K_ESCAPE:
			terminate()
		else:  
			current_string += unichr  # add a new char

		# limit the name length to 32 characters 
		current_string = current_string[:32]
		# show the current name during typing
		display_box(question + ": " + current_string)

	return current_string # this is the answer    

def get_key():
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				return (event.key, event.unicode)

def display_box(message):
	"Print a message in a box in the middle of the screen"
	#tampil.fill(BLACK)
	bg = pygame.image.load("bg_bukutamu800x600.jpg")
	tampil.blit(bg,(0,0))
	
	left = (SCREENWIDTH /3)
	top = (SCREENHEIGHT / 2) 
	
	tampil.blit(BASICFONT.render("Tekan Enter untuk mengakhiri.", True, GREEN),(left-100, top+200)) 
	if len(message) != 0:
		tampil.blit(TEXTFONT.render(message, True, WHITE), (100, top + 50))
	
	pygame.display.update()

def terminate():	
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main('Tekan C untuk kamera')
