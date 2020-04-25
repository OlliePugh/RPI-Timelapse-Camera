import sys
from picamera import PiCamera
import time
import datetime as dt

class TimelapseCamera:
    directory = "not-in-db"
    cameraWarmUpTime = 2

    def __init__(self, interval):
        self.interval=interval # how many minutes between each photo
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
    tlCamera = TimelapseCamera(60)  #make static list of all threads that can be closed
    while True:
        tlCamera.take_photo()
        time.sleep(tlCamera.interval-TimelapseCamera.cameraWarmUpTime)

if __name__ == "__main__":
    main()
