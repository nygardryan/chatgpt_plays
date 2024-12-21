import os
import time
import pygetwindow as gw
import openai
from reasoning import describe_screenshot, decide_next_action, decide_strategy
from image.image import capture_screenshot, image_difference
from globals import g
import controls
import pyautogui
from projects_secrets import ChatGPTApiKey

# Ensure you have your OpenAI API key set in your environment

pyautogui.FAILSAFE = False

api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = ChatGPTApiKey

def attempt_action(next_action):
    print(next_action)
    action_text = next_action.get('action')
    action_arguments = next_action.get('arguments')
    
    argument_dict = {}

    for argument in action_arguments:
        if '=' in argument:
            key_, value_ = argument.split('=')
            argument_dict[key_] = value_
        

    if action_text:
        action = getattr(controls, action_text)
        action(*action_arguments, **argument_dict)
    
    return action_text, action_arguments



def main():    
    prev_action = []
    prev_arguments = []
    previous_screenshot = None
    difference_threshold = 300  # Adjust this threshold as needed

    strategy = decide_strategy()
    
    controls.update_window_coordinates()
    controls.center_mouse()
    

    while True:

        current_screenshot = capture_screenshot()
        print("Loop")
        if previous_screenshot is not None:
            diff = image_difference(previous_screenshot, current_screenshot)
            print(diff)
            description = describe_screenshot(current_screenshot)
            if diff >= difference_threshold:

                next_action = decide_next_action(current_screenshot, strategy, description)
                prev_action = []
                prev_arguments = []
                previous_action, previous_arguments = attempt_action(next_action)
                    
            else:
                prompt = ""
                if prev_action:
                    prompt = f"""Your previous actions of {prev_action}  failed to change the state of the game, use a different function.\n"""
                    print(prev_action)
                next_action = decide_next_action(current_screenshot, strategy, description, prompt)
                previous_action, previous_arguments = attempt_action(next_action)
                prev_action.append(previous_action)
                previous_arguments.append(previous_arguments)
                




        previous_screenshot = current_screenshot
        # Wait a bit before next capture to avoid hitting API rate limits and reduce cost
        time.sleep(1)

if __name__ == "__main__": 
    main()