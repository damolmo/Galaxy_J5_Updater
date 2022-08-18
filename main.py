from resources import *
from detect import *

class Main :

	def __init__(self) :
		self.screen = WIN
		self.running = True
		self.screen_rect = self.screen.get_rect()
		self.clock = pygame.time.Clock()
		self.version = "1.3"
		self.version_url = "https://github.com/daviiid99/Galaxy_J5_Updater/raw/master/version.txt"
		self.check_for_updates = False
		self.update_rect = pygame.Rect(1375, 250, 231, 83)

	def update_app(self) :
		while self.running :

			if self.check_for_updates :
				# This method will check for updates and download the latest app version

				# Remove previous version if exists
				os.system("del installer.exe")

				# Download version text file
				if platform.system() == "Windows" :
					os.system("cd binaries & wget.exe -O version.txt %s" % self.version_url)

				else :
					wget.download(self.version_url)

				# Read the file and save the text into a variable
				version = Path('version.txt').read_text()

				# Compare the current version vs the new version
				if version < self.version :
					# This means we're outdated
					# We'll download the newest version
					url = "https://github.com/daviiid99/Galaxy_J5_Updater/releases/download/v%s/Galaxy.J5.Updater.-.Installer.exe" % version
					os.system("cd binaries & wget.exe -O installer.exe %s" % url)
					os.system("cd binaries & move installer.exe ../installer.exe")
					os.system("start installer.exe")
					self.check_for_updates = False

				else :
					self.check_for_updates = False


	def draw_title_screen(self) :

		while self.running :

			# Background color
			self.screen.fill(GREEN)

			# Set SAMSUNG Logo
			self.screen.blit(logo, (600, 120))

			# Draw J5 render
			self.screen.blit(render, (350, 350))

			# Credits

			# Update string
			text = SMALLEST_FONT.render("v.%s" % self.version, 1, WHITE)
			self.screen.blit(text, (400, 250))

			# Update buton
			text = SMALLEST_FONT.render("Check Updates", 1, WHITE)
			self.screen.blit(text, (1375, 250))

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

		if self.screen_rect.collidepoint(mouse) and not self.update_rect.collidepoint(mouse) :
			self.running = False
			device = Detect()
			device.detect_device()

		if self.update_rect.collidepoint(mouse) :
			self.check_for_updates = True


	def start_program(self) :
		# Create new threads
		thread_1 = threading.Thread(target= self.draw_title_screen, name="ui")
		thread_2 = threading.Thread(target = self.controller, name="mouse")
		thread_3 = threading.Thread(target = self.update_app, name="mouse")

		# Start threads
		thread_1.start()
		thread_2.start()
		thread_3.start()

		# Avoid UI crash
		start = self.controller()

		# Wait for all threads to end
		while self.running :
			thread_1.join()
			thread_2.join()
			thread_3.join()



start = Main()
start.start_program()
