from flask import Flask, request, jsonify, render_template
import aiml
import os


app = Flask(__name__)

kernel = aiml.Kernel()

aiml_folder = "D:/PYTHON/EAGLE WINGS CHATBOT/AIML FILES"

for filename in os.listdir(aiml_folder):
    if filename.endswith(".aiml"):
        kernel.learn(os.path.join(aiml_folder, filename))

def takeoff():
    print("Drone is taking off!")

def land():
    print("Drone is landing!")

def move_forward():
    print("Drone is moving forward!")

def move_backward():
    print("Drone is moving backward!")

def move_left():
    print("Drone is moving left!")

def move_right():
    print("Drone is moving right!")

def ascend():
    print("Drone is ascending!")

def descend():
    print("Drone is descending!")

def flip():
    print("Drone is performing a flip!")

def rotate(direction):
    print(f"Drone is rotating {direction}!")

def roll(direction):
    if direction == "left":
        print("Drone is rolling to the left!")
    elif direction == "right":
        print("Drone is rolling to the right!")

def pitch(direction):
    if direction == "forward" or "front":
        print("Drone is pitching forward!")
    elif direction == "backward" or "back":
        print("Drone is pitching backward!")

def battery_status():
    print("Checking battery status...")

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

    get_bot_response(user_message)

    drone_state = kernel.getPredicate("direction").lower()

    if drone_state:
        perform_action(drone_state)
        kernel.setPredicate("direction", "none")

    bot_reply = get_bot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
