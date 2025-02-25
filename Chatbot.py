from flask import Flask, request, jsonify, render_template
import aiml
import os
from djitellopy import Tello

app = Flask(__name__)
kernel = aiml.Kernel()

tello = Tello()
tello.connect()

aiml_folder = "D:/PYTHON/EAGLE WINGS CHATBOT/AIML FILES"

for filename in os.listdir(aiml_folder):
    if filename.endswith(".aiml"):
        kernel.learn(os.path.join(aiml_folder, filename))

def takeoff():
    tello.takeoff()

def land():
    tello.land()

def move_forward():
    tello.move_forward(50)

def move_backward():
    tello.move_back(50)

def move_left():
    tello.move_left(50)

def move_right():
    tello.move_right(50)

def ascend():
    tello.move_up(50)

def descend():
    tello.move_down(50)

def flip():
    tello.flip("f")

def rotate(direction):
    if direction == "left":
        tello.rotate_counter_clockwise(45)
    elif direction == "right":
        tello.rotate_clockwise(45)

def roll(direction):
    if direction == "left":
        tello.move_left(50)
    elif direction == "right":
        tello.move_right(50)

def pitch(direction):
    if direction in ["forward", "front"]:
        tello.move_forward(50)
    elif direction in ["backward", "back"]:
        tello.move_back(50)

def battery_status():
    battery = tello.get_battery()
    print(f"Battery status: {battery}%")

def perform_action(drone_state):
    if "yaw" in drone_state:
        direction = drone_state.split()[-1]
        rotate(direction)
    elif "roll" in drone_state:
        direction = drone_state.split()[-1]
        roll(direction)
    elif "pitch" in drone_state:
        direction = drone_state.split()[-1]
        pitch(direction)
    elif "forward" in drone_state:
        move_forward()
    elif "backward" in drone_state or "back" in drone_state:
        move_backward()
    elif "left" in drone_state:
        move_left()
    elif "right" in drone_state:
        move_right()
    elif "up" in drone_state:
        ascend()
    elif "down" in drone_state or "downward" in drone_state:
        descend()
    elif "take off" in drone_state:
        takeoff()
    elif "land" in drone_state:
        land()
    elif drone_state == "flip":
        flip()
    elif drone_state == "battery_status":
        battery_status()
    else:
        print(f"Unknown drone state: {drone_state}")

def get_bot_response(user_input):
    response = kernel.respond(user_input)
    return response if response else "Sorry, I don't understand that."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form.get("message")
    bot_reply = get_bot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

