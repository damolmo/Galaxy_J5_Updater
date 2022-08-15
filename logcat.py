from resources import *

def catch_device_info(arg) :

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