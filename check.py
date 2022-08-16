from resources import *
from logcat import catch_device_info
from install import *

class Check:

    def __init__(self) :
        self.checking = True
        self.screen = WIN
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.codename = ''
        self.os = ''
        self.timestamp = 0
        self.R = False
        self.S = False
        self.json_file = downloads
        self.update_available = False
        self.up_to_date = False
        self.downloading = False
        self.ota_complete = False
        self.current_anim = los
        self.ota_path = "downloads"
        self.filename = "ota.zip"
        self.progress_message = ''
        self.install_rect = pygame.Rect(840, 700, 231, 83)
        self.exit_rect = pygame.Rect(840, 700, 231, 83)
        self.final_anim = False


    def check_for_latest_update(self) :

        if "11" in self.os :
            # We're running android 11 release, doesn't matter if it's not LineageOS
            # Since upgrading from one os to a higher version is experimental, we'll not show a 12 entry
            self.R = True

        else :
            self.S = True


    def download_latest_json(self) :

        # Remove previous json is exists
        
        if exists("%s.json" % self.codename) :
            if platform.system() == "Windows" :
                os.system("del /f %s.json" % self.codename)
            else :
                os.system("rm %s.json" % self.codename)


        # Download LineageOS 18.1 JSON
        if self.R :

            # Download latest json
            wget.download(downloads["DEVICES"][self.codename]["R"])

        else :

            # Download latest json
            wget.download(downloads["DEVICES"][self.codename]["S"])

            # Save and load json
            self.json_file = open("%s.json" % self.codename)
            self.json_file = json.load(self.json_file)

            # Download latest ota
            self.download_latest_ota()

    def download_latest_ota(self) :

        # Assign timestamp from installed build
        self.timestamp = catch_device_info("ro.system.build.date.utc")

        # Compare new timestamp with old timestamp
        if self.timestamp < str(self.json_file["response"]["datetime"]) :
            self.update_available = True

        else :
            self.update_available = False
            self.up_to_date = True

    """
    def bar_progress(self, current, total, width=80):
        self.progress_message = "Download LineageOS OTA: %d%%" % (current / total * 100)
        # Don't use print() as it will print in new line every time.
        sys.stdout.write("\r" + self.progress_message)
        sys.stdout.flush()

    """


    def download_ota_file(self) :

        while self.checking :

            if self.update_available :

                # Check if file doesn't exist before downloading
                self.filename = self.json_file["response"]["filename"]
                if exists("%s/%s" % (self.ota_path, self.filename)) :
                    if platform.system() == "Windows" :
                        os.system("cd downloads & del /f %s" % self.filename)

                    else :
                        os.system("rm %s" % self.filename)

                # Download OTA file
                self.ota_path = self.ota_path + "/" + self.filename
                self.downloading = True

                if platform.system()== "Windows" :
                    file = os.system("cd binaries & wget.exe -O %s.zip %s" % (self.filename, self.json_file["response"]["url"]))
                    os.system("cd binaries & move %s.zip ../%s" % (self.filename, self.ota_path))
                else :
                    wget.download("%s" % self.json_file["response"]["url"], "ota.zip" )

                # Stop downloading the ota :) We're inside a loop
                self.update_available = False
                self.ota_complete = True
                self.final_anim = True


    def controller(self) :

        while self.checking :

            for event in pygame.event.get() :

                if event.type == pygame.QUIT:
                    self.resume = False

                elif event.type == pygame.MOUSEBUTTONDOWN :
                    if self.install_rect.collidepoint(event.pos) :
                        if self.ota_complete :
                            self.checking = False


                    if self.exit_rect.collidepoint(event.pos) :
                        if self.up_to_date :
                            self.checking = False


    def draw_windows(self) :

        while self.checking :

            # Set background color
            self.screen.fill(BLACK)

            # LineageOS loading animation
            if not self.up_to_date and not self.ota_complete:
                self.screen.blit(pygame.transform.scale(self.current_anim, (800, 470)), (570, 300))

            elif self.up_to_date :
                self.current_anim = pygame.transform.scale(pygame.image.load(os.path.join("assets/anim", "frame_139_delay-0.05s.gif")), (1000, 400))
                self.screen.blit(pygame.transform.scale(self.current_anim, (800, 470)), (570, 300))

                text = small_font.render("Your system is up-to-date", 1, WHITE)
                self.screen.blit(text, (800, 650))
                # Install button
                text = count_font.render("Exit", 1, WHITE)
                self.screen.blit(button_lineage, (840, 700))
                self.screen.blit(text, (920, 720))


            if not self.update_available and not self.up_to_date and not self.downloading :
                text = small_font.render("Looking for updates..", 1, WHITE)
                self.screen.blit(text, (830, 650))

            if self.update_available and not self.up_to_date and not self.downloading :
                text = small_font.render("A new update was found..", 1, WHITE)
                self.screen.blit(text, (800, 650))


            # Download message
            if self.downloading and not self.ota_complete :
                text = small_font.render("Downloading LineageOS OTA", 1, WHITE)
                self.screen.blit(text, (780, 650))


            # Ota downloaded message
            if self.ota_complete :

                if self.final_anim :
                    self.screen.blit(pygame.transform.scale(self.current_anim, (800, 470)), (570, 300))

                if not self.final_anim :
                    self.screen.blit(pygame.transform.scale(self.current_anim, (800, 470)), (570, 300))
                    text = small_font.render("OTA file is ready to install!", 1, WHITE)
                    self.screen.blit(text, (800, 650))

                    # Install button
                    text = count_font.render("Install", 1, WHITE)
                    self.screen.blit(button_lineage, (840, 700))
                    self.screen.blit(text, (905, 720))


            pygame.display.update()

    def anim(self) :
        while self.checking :

            if not self.up_to_date and not self.final_anim and not self.ota_complete :

                for anim in range(20,38) :
                    if self.checking :
                        self.current_anim = pygame.transform.scale(pygame.image.load(os.path.join("assets/anim", "frame_0%d_delay-0.05s.gif" % anim)), (1000, 400))
                        self.clock.tick(12)

            if self.final_anim :
                for anim in range(20,140) :
                    if self.checking :
                        if anim < 100 :
                            self.current_anim = pygame.transform.scale(pygame.image.load(os.path.join("assets/anim", "frame_0%d_delay-0.05s.gif" % anim)), (1000, 400))
                            self.clock.tick(12)

                        else :
                            self.current_anim = pygame.transform.scale(pygame.image.load(os.path.join("assets/anim", "frame_%d_delay-0.05s.gif" % anim)), (1000, 400))
                            self.clock.tick(12)

                            if anim == 139 :
                                self.final_anim = False



    def updates(self, codename) :

        # Current device codename
        self.codename = codename

        # Current device android version 
        self.os = catch_device_info("ro.system_ext.build.version.release_or_codename")

        # Create new threads
        los_anim_thread = threading.Thread(target = self.anim, name="anim")
        check_updates_thread = threading.Thread(target = self.check_for_latest_update, name="check")
        download_json_thread = threading.Thread(target = self.download_latest_json)
        download_ota_thread = threading.Thread(target = self.download_ota_file, name="ota")
        draw_windows_thread = threading.Thread(target = self.draw_windows, name="ui")
        controller_thread = threading.Thread(target = self.controller, name="mouse")

        # Start new threads
        los_anim_thread.start()
        check_updates_thread.start()
        download_json_thread.start()
        download_ota_thread.start()
        draw_windows_thread.start()
        controller_thread.start()

        start = self.controller()

        # Wait for all threads to complete
        while self.checking :
            los_anim_thread.join()
            check_updates_thread.join()
            download_json_thread.join()
            download_ota_thread.join()
            draw_windows_thread.join()
            controller_thread.join()

        # Install the OTA file
        if not self.up_to_date :
            install = Install()
            install.start_installation(self.ota_path)







