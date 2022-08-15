from resources import *
from detect import *

class Main :

	def __init__(self) :
		self.screen = WIN
		self.running = True
		self.screen_rect = self.screen.get_rect()
		self.clock = pygame.time.Clock()


	def draw_title_screen(self) :

		while self.running :

			# Background color
			self.screen.fill(GREEN)

			# Set SAMSUNG Logo
			self.screen.blit(logo, (600, 120))

			# Draw J5 render
			self.screen.blit(render, (350, 350))

			# Credits

			text = SMALLEST_FONT.render("Lineage logo and brand are", 1, WHITE)
			self.screen.blit(text, (400, 800))

			text = SMALLEST_FONT.render("property of LineageOS", 1, WHITE)
			self.screen.blit(text, (400, 830))

			text_2 = SMALLEST_FONT.render("©2022 daviiid99", 1, WHITE)
			self.screen.blit(text_2, (400, 860))

			# Press to start
			self.screen.blit(mouse, (1250, 800))
			text = SMALLEST_FONT.render("Press to start", 1, WHITE)
			self.screen.blit(text, (1340, 820))


			pygame.display.update()

	def controller(self) :

		while self.running :

			for event in pygame.event.get() :

				if event.type == pygame.QUIT:
					self.running = False

				elif event.type == pygame.MOUSEBUTTONDOWN :
					self.check_mouse(event.pos)

	def check_mouse(self, mouse) :

		if self.screen_rect.collidepoint(mouse) :
			self.running = False
			device = Detect()
			device.detect_device()


	def start_program(self) :
		# Create new threads
		thread_1 = threading.Thread(target= self.draw_title_screen, name="ui")
		thread_2 = threading.Thread(target = self.controller, name="mouse")

		# Start threads
		thread_1.start()
		thread_2.start()

		# Avoid UI crash
		start = self.controller()

		# Wait for all threads to end
		while self.running :
			thread_1.join()
			thread_2.join()



start = Main()
start.start_program()
