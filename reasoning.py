import pyautogui
import openai
import base64
from io import BytesIO
from globals import g
from image.dimensions import height_of_screen, width_of_screen
from pydantic import BaseModel
import json

model = 'gpt-4o-mini'


functions_code = ""
with open("controls.py") as f:
    functions_code = f.read()


class Action(BaseModel):
    action: str
    arguments: list[str]
    thoughts: str
    reasoning: str


def describe_screenshot(img):

    buffered = BytesIO()
    img.save(buffered, format="jpeg")
    img_bytes = buffered.getvalue()
    base64_image = base64.b64encode(img_bytes).decode('utf-8')

    prompt = f"From this image from the game {g.window_name}, list out all percentages of stats and attributes displayed and all important information for the player to know."


    print("Describing")
    response = openai.chat.completions.create(
        model=model, 
        messages=[{"role": "user", "type": "text", "content": prompt},
                  {"role": "user", "content": [{"type": "image_url", "image_url": {"url":  f"data:image/jpeg;base64,{base64_image}"}}]}], 
        temperature=1
    )

    print("Describe Response")

    description = response.choices[0].message.content.strip()
    return description


def decide_next_action(img, strategy, description, additional_prompt=""):
    """
    Convert image to base64 for sending if you want ChatGPT to reason about the image.
    Alternatively, you could provide text descriptions or use a vision-language model.
    """
    # Convert image to PNG in memory
    buffered = BytesIO()
    img.save(buffered, format="jpeg")
    img_bytes = buffered.getvalue()
    base64_image = base64.b64encode(img_bytes).decode('utf-8')

    prompt = ""

    if additional_prompt:
        prompt += additional_prompt

    prompt += f"You are playing {g.window_name} and you must choose an action to interact with the game. You should attempt to follow your strategy and react to the current game state"

    prompt += f"""
    <strategy>
    {strategy}
    </strategy>
"""
    
    prompt += f"""
    <game_state>
    {description}
    </game_state>
"""

    prompt += f"""Call one of the actions from the following list of python functions\n
                <code>
                {functions_code}
                </code>"""
    
    prompt += f"""
    <controls>
    {g.controls}

    Avoid using the mouse when possible, use keyboard shortcuts when possible.
    </controls>
    """

    prompt += f""" 

    <screen_details>
    your screensize is {width_of_screen}x{height_of_screen}
    </screen_details>
    """

    prompt += """
    <examples>
    {'action': 'click_mouse', 'arguments': ['left'], 'thoughts': 'clicking left will let me choose ...', 'reasoning': 'By choosing ...'}
    </examples
    """

    print("Describing")
    response = openai.beta.chat.completions.parse(
        model=model, 
        messages=[{"role": "user", "type": "text", "content": prompt},
                  {"role": "user", "content": [{"type": "image_url", "image_url": {"url":  f"data:image/jpeg;base64,{base64_image}"}}]}], 
        response_format=Action,
        temperature=1
    )

    print("Decide Action")

    next_action = response.choices[0].message.content.strip()
    return json.loads(next_action)


def describe_how_to_play():
    
    prompt = f"Describe how to play {g.window_name} and all of it's mechanics"

    response = openai.chat.completions.create(
        model=model, 
        messages=[{"role": "user", "type": "text", "content": prompt,}],
        temperature=1
    )

    return response

def describe_controls():
    prompt = f"The all of the controls in the game {g.window_name} on PC"

    response = openai.chat.completions.create(
        model=model, 
        messages=[{"role": "user", "type": "text", "content": prompt}],
        temperature=1
    )

    return response

def decide_strategy():
    prompt = f"Of all of the strategies within the game {g.window_name} choose one to pursue"

    response = openai.chat.completions.create(
        model=model, 
        messages=[{"role": "user", "type": "text", "content": prompt}],
        temperature=0.5
    )

    return response