from flask import Flask, request, jsonify, render_template
import aiml
import os
from djitellopy import Tello
import threading

app = Flask(__name__)
kernel = aiml.Kernel()

tello = Tello()

def connect_tello():
    try:
        tello.connect()
        print(" Tello Connected!")
    except Exception as e:
        print(f" Tello Connection Failed: {e}")

threading.Thread(target=connect_tello, daemon=True).start()


aiml_folder = "D:/PYTHON/EAGLE WINGS CHATBOT/AIML FILES"
for filename in os.listdir(aiml_folder):
    if filename.endswith(".aiml"):
        kernel.learn(os.path.join(aiml_folder, filename))


def perform_action(drone_state):
    def execute_command():
        if "take off" in drone_state:
            print(" Taking Off!")
            tello.takeoff()

        elif "land" in drone_state:
            print(" Landing!")
            tello.land()

        elif "forward" in drone_state or "pitch up" in drone_state:
            print("⬆ Moving Forward")
            tello.move_forward(30)

        elif "backward" in drone_state or "pitch down" in drone_state:
            print("⬇ Moving Backward")
            tello.move_back(30)

        elif "left" in drone_state and "yaw" not in drone_state and "roll" not in drone_state:
            print("⬅ Moving Left")
            tello.move_left(30)

        elif "right" in drone_state and "yaw" not in drone_state and "roll" not in drone_state:
            print("➡ Moving Right")
            tello.move_right(30)

        elif "up" in drone_state:
            print("⬆ Ascending")
            tello.move_up(50)

        elif "down" in drone_state:
            print("⬇ Descending")
            tello.move_down(30)

        elif "flip" in drone_state:
            print(" Flipping")
            tello.flip_back()

        elif "yaw left" in drone_state:
            print("↪ Rotating Counter Clockwise")
            tello.rotate_counter_clockwise(45)

        elif "yaw right" in drone_state:
            print("↩ Rotating Clockwise")
            tello.rotate_clockwise(45)

        elif "roll left" in drone_state:
            print("↙ Rolling Left")
            tello.move_left(30)

        elif "roll right" in drone_state:
            print("↘ Rolling Right")
            tello.move_right(30)

        else:
            print(f"⚠ Unknown drone command: {drone_state}")

    command_thread = threading.Thread(target=execute_command)
    command_thread.start()



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

    drone_state = kernel.getPredicate("direction").lower()
    if drone_state:
        perform_action(drone_state)
        kernel.setPredicate("direction", "none")  # Reset after execution

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
