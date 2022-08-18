from resources import *
from check import *


class Device :

	def __init__(self) :
		self.screen = WIN
		self.screen_rect = self.screen.get_rect()
		self.clock = pygame.time.Clock()
		self.resume = True
		self.current_anim = los
		self.download_rect = pygame.Rect(1000, 780, 444, 80)
		self.abort = False

	def draw(self) :

		while self.resume :

			# Set background color
			self.screen.fill(GREEN)

			# Device render
			self.screen.blit(pygame.transform.scale(render, (1050, 700)), (100, 200))
			"""
			self.screen.blit(pygame.transform.scale(self.current_anim, (300, 170)), (480, 450))
			"""

			# Title
			self.screen.blit(aosp, (850, 200))
			title = count_font.render("Current Android Device", 1, WHITE)
			self.screen.blit(title, (1000, 250))

			# Warning
			warning = warning_font.render("This info is from your ADB device", 1 , WHITE)
			self.screen.blit(warning, (1020, 300))
			warning = warning_font.render("For any error, report to ", 1 , WHITE)
			self.screen.blit(warning, (1020, 325))
			warning = warning_font.render("daviiideveloper@gmail.com", 1 , WHITE)
			self.screen.blit(warning, (1020, 350))

			# Device model
			self.screen.blit(button_dark, (1000, 370))
			self.screen.blit(button, (1200, 370))
			device = smallest_font.render("J5 Model", 1, WHITE	)
			self.screen.blit(device, (1020, 400))
			model = self.catch_device_info("ro.product.model")
			text = small_font.render(model, 1, BLACK)
			self.screen.blit(text, (1210, 400))
			

			# Lineage Version
			self.screen.blit(button_dark, (1000, 470))
			self.screen.blit(button, (1200, 470))
			version = smallest_font.render("LineageOS", 1, WHITE	)
			self.screen.blit(version, (1020, 500))
			los = self.catch_device_info("ro.lineage.build.version")
			text = small_font.render(los, 1, BLACK)
			self.screen.blit(text, (1210, 500))
			

			# Security Patch Level
			self.screen.blit(button_dark, (1000, 570))
			self.screen.blit(button, (1200, 570))
			version = smallest_font.render("Security level", 1, WHITE	)
			self.screen.blit(version, (1020, 600))
			patch = self.catch_device_info("ro.build.version.security_patch")
			text = small_font.render(patch, 1, BLACK)
			self.screen.blit(text, (1210, 600))

			# ID
			self.screen.blit(button_dark, (1000, 670))
			self.screen.blit(button, (1200, 670))
			version = smallest_font.render("Build ID", 1, WHITE	)
			self.screen.blit(version, (1020, 700))
			patch = self.catch_device_info("ro.build.id")
			text = smallest_font.render(patch, 1, BLACK)
			self.screen.blit(text, (1210, 700))

			# Update button
			text = count_font.render("Check for updates", 1, WHITE)
			self.screen.blit(button_green, (1030, 780))
			self.screen.blit(button_green, (1170, 780))
			self.screen.blit(text, (1060, 800))

			#pygame.draw.rect(WIN, BLUE, self.download_rect)

			pygame.display.update()


	def catch_device_info(self, arg) :

		info = subprocess.check_output("cd platform-tools & adb shell getprop %s" % arg, shell=True)
		info = info.decode("utf-8")
		info = str(info)

		while " " in info :
			info = info.replace(" ", "")

		while "\n" in info :
			info = info.replace("\n", "")

		while "\r" in info :
			info = info.replace("\r", "")

		return info

	def anim(self) :
		while self.resume :

			for anim in range(10,139) :
				if self.resume :
					if anim < 100 :
						self.current_anim = pygame.transform.scale(pygame.image.load(os.path.join("assets/anim", "frame_0%d_delay-0.05s.gif" % anim)), (1000, 400))
						self.clock.tick(12)

			for anim in range(100,139) :
				if self.resume :
					self.current_anim = pygame.transform.scale(pygame.image.load(os.path.join("assets/anim", "frame_%d_delay-0.05s.gif" % anim)), (1000, 400))
					self.clock.tick(12)


	def controller(self) :

		while self.resume :

			for event in pygame.event.get() :

				if event.type == pygame.QUIT:
					self.resume = False
					self.abort = True

				elif event.type == pygame.MOUSEBUTTONDOWN :
					self.check_click(event.pos)

	def check_click(self, mouse) :
		if self.download_rect.collidepoint(mouse) :
			self.resume = False


	def os_info(self, codename) :

		# Check if the current device is recognized
		thread_1 = threading.Thread(target = self.controller, name="controller")
		thread_2 = threading.Thread(target = self.draw, name="ui")
		thread_3 = threading.Thread(target = self.anim, name="anim")


		# Start threads
		thread_1.start()
		thread_2.start()
		thread_3.start()

		# Avoid Controller freeze
		start = self.controller()	

		# Wait for all jobs to complete
		while self.resume :
			thread_1.join()
			thread_2.join()
			thread_3.join()

		if not self.abort :
			# Search for updates
			check = Check()
			check.updates(codename)