import sys
import mysql.connector
from mysql.connector import errorcode
from picamera import PiCamera
import time
import datetime as dt
from db_credentials import config as db_config
import threading

class TimelapseCamera:
    directory = "not-in-db"
    cameraWarmUpTime = 5

    def __init__(self, interval):
        self.interval=interval # how many minutes between each photo
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)

        self.thread = threading.Thread(target = self.thread_routine)
        self.thread.daemon = True
        self.thread.start()

    def thread_routine(self):
        while True:
            self.take_photo()
            time.sleep(self.interval*60-TimelapseCamera.cameraWarmUpTime)


    def take_photo(self):
        print("Taking photo")
        self.camera.start_preview()
        time.sleep(TimelapseCamera.cameraWarmUpTime)
        self.camera.capture(TimelapseCamera.directory + "/" + str(time.time())+".jpg")
        self.camera.stop_preview()
        print("Finished taking photo with name: " + str(time.time()) + ".jpg")

def main():
    tlCamera = TimelapseCamera(1)  #make static list of all threads that can be closed

if __name__ == "__main__":
    main()
    while True:
        pass
