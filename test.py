# IMPORTING REQUIRED PACKAGES.
import aiml
import os

# INITIALIZING THE AIML KERNEL.
bot = aiml.Kernel()

# SETTING UP THE AIML FILES DIRECTORY.
aiml_directory = "AIML FILES"

# LOADING ALL AIML FILES INTO THE KERNEL.
for file in os.listdir(aiml_directory):
    if file.endswith(".aiml"):
        bot.learn(os.path.join(aiml_directory, file))

# DEFINING DUMMY FUNCTIONS FOR TESTING PURPOSES (WITHOUT DRONE CONTROL).

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

def rotate():
    print("Drone is rotating!")

def battery_status():
    print("Checking battery status...")

# FUNCTION TO PERFORM ACTIONS BASED ON THE DRONE STATE.
def perform_action(drone_state):
    if drone_state == "takeoff":
        takeoff()
    elif drone_state == "land":
        land()
    elif drone_state == "forward":
        move_forward()
    elif drone_state == "backward":
        move_backward()
    elif drone_state == "left":
        move_left()
    elif drone_state == "right":
        move_right()
    elif drone_state == "up":
        ascend()
    elif drone_state == "down":
        descend()
    elif drone_state == "flip":
        flip()
    elif drone_state == "rotate":
        rotate()
    elif drone_state == "battery_status":
        battery_status()
    else:
        print(f"Unknown drone state: {drone_state}")

# FUNCTION TO GET THE CHATBOT'S RESPONSE.
def get_bot_response(user_input):
    response = bot.respond(user_input)
    return response if response else "Sorry, I don't understand that."

# MAIN FUNCTION.
if __name__ == "__main__":
    # ENTERING THE CHAT LOOP.
    while True:
        # TAKING USER INPUT.
        user_input = input("You: ").strip().lower()

        # CHECKING IF THE USER WANTS TO END THE CHAT.
        if user_input in ["end", "bye"]:
            print("Bot: Goodbye! Have a great day ahead.")
            break  # EXIT THE LOOP

        # GETTING THE BOT'S RESPONSE TO THE USER INPUT.
        response = get_bot_response(user_input)
        print(f"Bot: {response}")

        # ONLY IF THE COMMAND IS NOT 'end' or 'bye', CHECK FOR A DRONE COMMAND.
        if user_input not in ["end", "bye"]:
            # CHECKING IF A VALID DRONE COMMAND WAS ISSUED.
            drone_state = bot.getPredicate("drone_state")

            # IF A VALID DRONE COMMAND WAS ISSUED, PERFORM IT.
            if drone_state:
                perform_action(drone_state)
                # RESET DRONE STATE AFTER ACTION.
                bot.setPredicate("drone_state", "")
            else:
                print("No valid command found. Please try again.")
