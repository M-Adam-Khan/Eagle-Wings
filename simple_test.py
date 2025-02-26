from djitellopy import Tello
import time

tello = Tello()
tello.connect()

def battery():
    print(tello.get_battery())

def takeoff():
    tello.takeoff()

def land():
    tello.land()


battery()
takeoff()

time.sleep(3)
land()