from settings import *  # Importerer alt fra settings.py (til og med pygames, så trenger å importere den i hver fil)
from sys import exit  # Denne kan brukes for å avslutte all type kode

# Components
from game import Game
from score import Score
from preview import Preview

class Main:
	def __init__(self):

		# General 
		pygame.init()
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
		self.clock = pygame.time.Clock()
		pygame.display.set_caption('Tetris By Ellie Marie')

		# Components
		self.game = Game()
		self.score = Score()
		self.preview = Preview()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# Display 
			self.display_surface.fill(GRAY)

			# Components
			self.game.run()
			self.score.run()
			self.preview.run()

			# Oppdaterer spillet
			pygame.display.update()
			self.clock.tick()  # kan skrive f.eks: tick(60) og da vil spillet kjøre på 60 FPS

if __name__ == '__main__':
	main = Main()
	main.run()
