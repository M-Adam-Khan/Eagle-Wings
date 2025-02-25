from djitellopy import Tello
import time

tello = Tello()
tello.connect()

def takeoff():
    tello.takeoff()

def land():
    tello.land()

takeoff()
time.sleep(3)
land()