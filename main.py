import sys
from picamera import PiCamera
import time
import datetime as dt
import db_uploader
import threading

class TimelapseCamera:
    directory = "not-in-db"
    cameraWarmUpTime = 2

    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)

    def take_photo(self):
        print("Taking photo")
        self.camera.start_preview()
        time.sleep(TimelapseCamera.cameraWarmUpTime)
        unix = time.time()
        timestamp = dt.datetime.fromtimestamp(unix).strftime('%d-%m-%Y %H:%M:%S')
        filename = TimelapseCamera.directory+"/"+timestamp+".jpg"
        self.camera.capture(filename)
        self.camera.stop_preview()
        print("Finished taking photo with name: " + filename)

def main():
    tlCamera = TimelapseCamera()  #make static list of all threads that can be closed
    tlCamera.take_photo()
    db_uploader.send_images_to_db()

if __name__ == "__main__":
    main()
