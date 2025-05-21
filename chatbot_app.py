from flask import Flask, request, jsonify, render_template
import aiml
import os
import threading

app = Flask(__name__)
kernel = aiml.Kernel()

aiml_folder = "D:/PYTHON/EAGLE WINGS CHATBOT/AIML FILES"
for filename in os.listdir(aiml_folder):
    if filename.endswith(".aiml"):
        kernel.learn(os.path.join(aiml_folder, filename))

def perform_action(drone_state):
    def execute_command():
        if "take off" in drone_state:
            print(" Taking Off!")

        elif "land" in drone_state:
            print(" Landing!")

        elif "forward" in drone_state:
            print("⬆ Moving Forward")

        elif "backward" in drone_state:
            print("⬇ Moving Backward")

        elif drone_state == "flip":
            print("Doing Flip")

        elif "left" in drone_state:
            print("⬅ Moving Left")

        elif "right" in drone_state:
            print("➡ Moving Right")

        elif "up" in drone_state:
            print(" Moving Up")

        elif "down" in drone_state:
            print(" Moving Down")

        elif "flip" in drone_state:
            print(" Flipping")

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