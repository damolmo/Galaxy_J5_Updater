from resources import *
from device import *

class Detect :


	def __init__(self) :

		self.running = True
		self.clock = pygame.time.Clock()
		self.screen = WIN
		self.screen_rect = self.screen.get_rect()
		self.model = ""
		self.platform_tools_exists = False
		self.loader_rs = [loader_01, loader_02, loader_03, loader_04, loader_05, loader_06, loader_07, loader_08]
		self.loader_anim = loader_01
		self.adb_wait_counter = 0
		self.allow_devices = ["j5nlte", "j5lte", "j5ltechn", "j5xnlte", "j53gxx"]


	# Methods for downloading Google Platform-Tools
	# Needed for ADB support

	# --------------------------------------------------------------------------------------

	def check_adb_tools(self) :

		# Check if platform tools dir exists

		if exists('platform-tools') :
			self.platform_tools_exists = True

		else :
			self.download_adb_tools()

	def download_adb_tools(self) :

		# Static urls for Platform tools from Google server
		adb_windows ="https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
		adb_linux ="https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
		url = adb_windows # Most common

		# Check current OS
		if platform.system() == "Linux" :
			url = adb_linux

		if platform.system() == "Windows" :
			# Download zip file
			os.system("cd binaries & wget.exe -O tools.zip %s" % url)
			os.system("cd binaries & move tools.zip ../tools.zip")

		else :
			wget.download(url, "tools.zip")

		# Extract the file
		self.extract_zip("tools.zip")


	def extract_zip(self, zip_file) :

		# Method to extract the current zip file
		with ZipFile(zip_file) as obj :
			obj.extractall()


	# -------------------------------------------------------------------------------------


	def check_adb_device(self):

		# Check if adb tools dir exists 
		self.check_adb_tools()

		while self.model not in self.allow_devices :
			try:
				my_device_model = subprocess.check_output("cd platform-tools & adb shell getprop ro.build.product", shell=True, )
				my_device_model = my_device_model.decode("utf-8")
				my_device_model = str(my_device_model)
				my_device_model = my_device_model.replace(" ", "")
				my_device_model = my_device_model.replace("\n", "")
				my_device_model = my_device_model.replace("\r", "")
				self.model = my_device_model

			except subprocess.CalledProcessError as e:
				my_device_model = str("No ADB device found")

	def controller(self) :

		while self.model not in self.allow_devices :

			for event in pygame.event.get() :

				if event.type == pygame.QUIT:
					self.model = "bye"

				elif event.type == pygame.MOUSEBUTTONDOWN :
					self.adb_wait_counter = 120

	def draw(self) :
		while self.model not in self.allow_devices :

			# Set background color
			self.screen.fill(GREEN)

			# Device render
			self.screen.blit(pygame.transform.scale(render, (1050, 700)), (100, 200))

			# Searching device dialog
			text = small_font.render("Searching for ADB devices", 1, WHITE)
			self.screen.blit(text, (1000, 350))

			# Loader
			self.screen.blit(self.loader_anim, (1120, 450))

			# Device is busy
			if self.adb_wait_counter >= 120 and self.model not in self.allow_devices :
				text_1 = smallest_font.render("Device not recognized?", 1, WHITE)
				self.screen.blit(text_1, (1060, 580))

				text_2 = smallest_font.render("Enable USB Debugging:", 1, WHITE)
				self.screen.blit(text_2, (1000, 730))

				text_3 = smallest_font.render("1. Settings > About Phone > Build Number (5 taps)", 1, WHITE)
				self.screen.blit(text_3, (1000, 770))
				text_4 = smallest_font.render("2. Settings > System> Developer Options > USB Debugging", 1, WHITE)
				self.screen.blit(text_4, (1000, 800))

			# Update objects on display
			pygame.display.update()

	def loader(self) :
		while self.model not in self.allow_devices :
			for img in self.loader_rs :
				self.loader_anim = img
				self.clock.tick(12)
				self.adb_wait_counter +=1


	def detect_device(self) :

		# Check if the current device is recognized
		thread_1 = threading.Thread(target=self.check_adb_device, name="adb")
		thread_2 = threading.Thread(target = self.controller, name="controller")
		thread_3 = threading.Thread(target = self.draw, name="ui")
		thread_4 = threading.Thread(target= self.loader, name="loader")

		# Start threads
		thread_1.start()
		thread_2.start()
		thread_3.start()
		thread_4.start()

		# Avoid Controller freeze
		start = self.controller()	

		# Wait for all jobs to complete
		while self.model not in self.allow_devices :
			thread_1.join()
			thread_2.join()
			thread_3.join()
			thread_4.join()

		# Show device current into on display
		device = Device()
		device.os_info(self.model)





		
