from resources import *
from logcat import catch_device_info

class Install :

    def __init__(self) :
        self.running = True
        self.rebooting = True
        self.installing = False
        self.sideload = False
        self.sideloading = False
        self.clock = pygame.time.Clock()
        self.screen = WIN
        self.screen_rect = self.screen.get_rect()
        self.loader_anim = loader_01
        self.loader_rs = [loader_01, loader_02, loader_03, loader_04, loader_05, loader_06, loader_07, loader_08]
        self.model = ''
        self.allow_devices = ["j5nlte", "j5nltexx ", "j5lte", "j5ltedx", "j5ltedo", "j5ltekx" , "j5lteub" , "j5ltexx" , "j5ltezt" , "j5ylte" , "j5ltechn" , "j5ltezm" , "j5xnlte", "j5xlte," "j53gxx", "j53g"]
        self.sideload_counter = 0
        self.reboot_system = False
        self.reboot_counter = 500
        self.start_sideloading = False
        self.sideload_rect = pygame.Rect(1000, 800, 231, 83)
        self.exit_rect = pygame.Rect(840, 700, 231, 83)


    def loader(self) :
        while self.running :

            if self.rebooting or self.sideload or self.installing or self.reboot_system:

                for img in self.loader_rs :
                    self.loader_anim = img
                    self.clock.tick(12)

                    if self.installing :
                        self.sideload_counter +=1

    def controller(self) :

        while self.running :

            for event in pygame.event.get() :

                if event.type == pygame.MOUSEBUTTONDOWN :
                    if self.sideload_rect.collidepoint(event.pos) :
                        self.start_sideloading = True
                        self.reboot_counter = 0

                    if self.exit_rect.collidepoint(event.pos) :
                        if self.reboot_system :
                            self.running = False

    def reboot_recovery(self) :

        while self.running :

            if self.rebooting :
                os.system("cd platform-tools & adb reboot recovery")
                self.rebooting = False # Avoids multiple reboots
                self.sideload = True


    def adb_detect(self) :
        # Search again for the device after the reboot
        # If the device isn't recognized, the app will continue searching for it 

        while self.running :

            if self.sideload :

                try:
                    my_device_model = catch_device_info("ro.build.product")
                    self.model = my_device_model

                    if self.model in self.allow_devices :
                        self.sideload = False
                        self.installing = True

                except subprocess.CalledProcessError as e:
                    my_device_model = str("No ADB device found")


    def adb_sideload(self, file) :
        # This process needs user interaction with the device
        # Help info will be provided into the display after some time

        while self.running :

            if self.installing :

                while self.reboot_counter > 0 :
                    text = small_font.render("Aborting Operation in : %d" % self.reboot_counter, 1, WHITE)
                    self.screen.blit(text, (1250, 250))
                    self.reboot_counter -=1
                    self.clock.tick(1)

                if self.reboot_counter == 0 :
                    push = os.system("cd platform-tools & adb sideload ../%s" % file)
                    self.installing = False
                    self.reboot_system = True



    def draw_windows(self) :

        while self.running :            

            # Device render
            if self.rebooting :
                self.screen.fill(BLACK)
                self.screen.blit(pygame.transform.scale(render, (500, 350)), (700, 350))
                self.screen.blit(self.loader_anim, (895, 710))
                text = small_font.render("Rebooting into recovery", 1, WHITE)
                self.screen.blit(text, (800, 815))


            if not self.rebooting and self.sideload :

                self.screen.fill(GREEN)
                self.screen.blit(pygame.transform.scale(render, (1050, 700)), (100, 200))

                # Searching device dialog
                text = small_font.render("Searching ADB devices", 1, WHITE)
                self.screen.blit(text, (980, 350))
                self.screen.blit(self.loader_anim, (1085, 400))

            if self.installing :
                self.screen.fill(GREEN)
                self.screen.blit(pygame.transform.scale(render, (1050, 700)), (100, 200))
                self.screen.blit(self.loader_anim, (1085, 400))

                text = small_font.render("Aborting Operation in : %d" % self.reboot_counter, 1, WHITE)
                self.screen.blit(text, (1250, 250))

                # Searching device dialog
                if not self.start_sideloading :
                    text = small_font.render("Connecting to ADB sideload", 1, WHITE)
                    self.screen.blit(text, (980, 350))

                else :
                    text = small_font.render("Flashing OTA file", 1, WHITE)
                    self.screen.blit(text, (1015, 350))

                    text = smallest_font.render("Check your device screen for installation progress", 1, WHITE)
                    self.screen.blit(text, (1015, 600))
                    text = smallest_font.render("Don't close the application until installation succeeds", 1, WHITE)
                    self.screen.blit(text, (1015, 640))

                    self.screen.blit(self.loader_anim, (1085, 400))

                if self.sideload_counter >=20 and not self.sideloading and not self.start_sideloading  :
                    text_1 = smallest_font.render("Are you stuck?", 1, WHITE)
                    self.screen.blit(text_1, (1070, 550))

                    text_2 = smallest_font.render("Enable ADB Sideload:", 1, WHITE)
                    self.screen.blit(text_2, (1000, 650))

                    text_3 = smallest_font.render("1. TWRP > Advanced > ADB Sideload", 1, WHITE)
                    self.screen.blit(text_3, (1000, 690))
                    text_4 = smallest_font.render("2, Press the 'Install' button", 1, WHITE)
                    self.screen.blit(text_4, (1000, 720))

                    text = count_font.render("Install", 1, WHITE)
                    self.screen.blit(button_lineage, (1000, 800))
                    self.screen.blit(text, (1065, 820))

            if self.reboot_system :
                self.screen.fill(BLACK)
                self.current_anim = pygame.transform.scale(pygame.image.load(os.path.join("assets/anim", "frame_139_delay-0.05s.gif")), (1000, 400))
                self.screen.blit(pygame.transform.scale(self.current_anim, (800, 470)), (570, 300))

                text = small_font.render("Your OTA installation completed!", 1, WHITE)
                self.screen.blit(text, (780, 650))

                # Install button
                text = count_font.render("Exit", 1, WHITE)
                self.screen.blit(button_lineage, (850, 700))
                self.screen.blit(text, (930, 720))

            pygame.display.update()


    def start_installation(self, file) :

        # Create new threads
        thread_1 = threading.Thread(target = self.draw_windows, name="ui")
        thread_2 = threading.Thread(target = self.loader)
        thread_3 = threading.Thread(target = self.controller)
        thread_4 = threading.Thread(target = self.reboot_recovery)
        thread_5 = threading.Thread(target = self.adb_detect)
        thread_6 = threading.Thread(target = self.adb_sideload, args=([file]))


        # Start threads
        thread_1.start()
        thread_2.start()
        thread_3.start()
        thread_4.start()
        thread_5.start()
        thread_6.start()

        start = self.controller()

        # Wait
        while self.running :
            thread_1.join()
            thread_2.join()
            thread_3.join()
            thread_4.join()
            thread_5.join()
            thread_6.join()

