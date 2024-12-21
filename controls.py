import pyautogui
import time
import win32gui
import win32con
from globals import g

# Ensure failsafe mode (move mouse to top-left corner to stop)
pyautogui.FAILSAFE = True

# Global game window boundaries
GAME_WINDOW = {
    'x': 0,         # Top-left x-coordinate of the game window
    'y': 0,         # Top-left y-coordinate of the game window
    'bottom_x': 0,  # Bottom-right x-coordinate of the game window
    'bottom_y': 0   # Bottom-right y-coordinate of the game window
}

def update_window_coordinates():

    window_name = g.window_name
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd) and window_name in win32gui.GetWindowText(hwnd):
            rect = win32gui.GetWindowRect(hwnd)
            extra['x'] = rect[0]
            extra['y'] = rect[1]
            extra['bottom_x'] = rect[2]
            extra['bottom_y'] = rect[3]

    coords = {'x': 0, 'y': 0, 'bottom_x': 0, 'bottom_y': 0}
    win32gui.EnumWindows(callback, coords)

    if coords['x'] == 0 and coords['y'] == 0:
        raise ValueError(f"Window '{window_name}' not found!")

    GAME_WINDOW.update(coords)

def adjust_coordinates(x, y):
    """Ensure coordinates are within the game window boundaries."""
    x = int(x)
    y = int(y)
    adj_x = min(max(GAME_WINDOW['x'], x), GAME_WINDOW['bottom_x'])
    adj_y = min(max(GAME_WINDOW['y'], y), GAME_WINDOW['bottom_y'])
    return adj_x, adj_y

# ========== MOUSE CONTROL FUNCTIONS ========== #
def move_mouse(x, y, duration=0):
    """Move mouse to (x, y) coordinates within the game window."""
    x = int(x)
    y = int(y)
    duration = float(duration)
    adj_x, adj_y = adjust_coordinates(x, y)
    pyautogui.moveTo(adj_x, adj_y, duration=duration)

def hold_mouse_button(button='left', duration=1):
    """Hold a mouse button down for a duration."""
    duration = float(duration)
    pyautogui.mouseDown(button=button)
    time.sleep(duration)
    pyautogui.mouseUp(button=button)

def scroll_mouse(amount):
    """Scroll the mouse wheel up or down."""
    amount = int(amount)
    pyautogui.scroll(amount)

def drag_mouse_to(x, y, duration=2.0, button='left'):
    """Drag the mouse to specified (x, y) coordinates within the game window."""
    x = int(x)
    y = int(y)
    duration = float(duration)
    adj_x, adj_y = adjust_coordinates(x, y)
    pyautogui.mouseDown(button=button)
    pyautogui.moveTo(adj_x, adj_y, duration=duration)
    pyautogui.mouseUp(button=button)

# ========== MOUSE CONTROL FUNCTIONS ========== #
def move_mouse(x, y, duration=0):
    """Move mouse to (x, y) coordinates within the game window."""
    x = int(x)
    y = int(y)
    duration = float(duration)
    adj_x, adj_y = adjust_coordinates(x, y)
    pyautogui.moveTo(adj_x, adj_y, duration=duration)

def click_mouse(button='left', clicks=1, interval=0.1):
    """Click the mouse with specified button and number of clicks."""
    pyautogui.click(button=button, clicks=clicks, interval=interval)

def hold_mouse_button(button='left', duration=1):
    """Hold a mouse button down for a duration."""
    duration = float(duration)
    pyautogui.mouseDown(button=button)
    time.sleep(duration)
    pyautogui.mouseUp(button=button)

def scroll_mouse(amount):
    """Scroll the mouse wheel up or down."""
    amount = int(amount)
    pyautogui.scroll(amount)

def drag_mouse_to(x, y, duration=2.0, button='left'):
    """Drag the mouse to specified (x, y) coordinates within the game window."""
    x = int(x)
    y = int(y)
    duration = float(duration)
    adj_x, adj_y = adjust_coordinates(x, y)
    pyautogui.mouseDown(button=button)
    pyautogui.moveTo(adj_x, adj_y, duration=duration)
    pyautogui.mouseUp(button=button)

# ========== KEYBOARD CONTROL FUNCTIONS ========== #
def press_key(key):
    """Press a single key."""
    pyautogui.press(key)

def hold_key(key, duration=1):
    """Hold down a key for a certain duration."""
    duration = float(duration)
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)

def press_multiple_keys(keys, interval=0.1):
    """Press multiple keys in succession."""
    interval = float(interval)
    for key in keys:
        pyautogui.press(key)
        time.sleep(interval)

def hotkey_combination(*keys):
    """Press a combination of keys (e.g., Ctrl + C)."""
    pyautogui.hotkey(*keys)

# ========== ACTION WRAPPERS ========== #
def jump():
    """Simulate jump action."""
    press_key('space')

def crouch(duration=1):
    """Simulate crouch action (hold key)."""
    hold_key('ctrl', duration=duration)

def move_forward(duration=1):
    """Move forward by holding the 'W' key."""
    hold_key('w', duration=duration)

def move_backward(duration=1):
    """Move backward by holding the 'S' key."""
    hold_key('s', duration=duration)

def strafe_left(duration=1):
    """Strafe left by holding the 'A' key."""
    hold_key('a', duration=duration)

def strafe_right(duration=1):
    """Strafe right by holding the 'D' key."""
    hold_key('d', duration=duration)

def shoot():
    """Simulate shooting by left-clicking."""
    click_mouse(button='left')

def aim():
    """Simulate aiming by holding the right mouse button."""
    hold_mouse_button(button='right', duration=2.0)


def swipe_left(duration=2.0):
    """Simulate a left swipe by dragging mouse from center to left."""
    center_x = (GAME_WINDOW['x'] + GAME_WINDOW['bottom_x']) // 2
    center_y = (GAME_WINDOW['y'] + GAME_WINDOW['bottom_y']) // 2
    center_mouse()
    drag_mouse_to(center_x - 200, center_y, duration=duration)

def swipe_right(duration=2.0):
    """Simulate a right swipe by dragging mouse from center to right."""
    center_x = (GAME_WINDOW['x'] + GAME_WINDOW['bottom_x']) // 2
    center_y = (GAME_WINDOW['y'] + GAME_WINDOW['bottom_y']) // 2
    center_mouse()
    drag_mouse_to(center_x + 200, center_y, duration=duration)

def center_mouse():
    center_x = (GAME_WINDOW['x'] + GAME_WINDOW['bottom_x']) // 2
    center_y = (GAME_WINDOW['y'] + GAME_WINDOW['bottom_y']) // 2
    move_mouse(center_x, center_y)

def click_card():
    """Click on the center card to view more details."""
    center_x = (GAME_WINDOW['x'] + GAME_WINDOW['bottom_x']) // 2
    center_y = (GAME_WINDOW['y'] + GAME_WINDOW['bottom_y']) // 2
    click_mouse(button='left')

# ========== EXAMPLE USE CASES ========== #
if __name__ == "__main__":
    window_name = "Game Window"  # Replace with the actual title of your game window
    print(f"Retrieving coordinates for window: {window_name}")

    print("Starting game automation test in 3 seconds...")
    time.sleep(3)
    
    # Move mouse to center of game window and shoot
    center_x = (GAME_WINDOW['x'] + GAME_WINDOW['bottom_x']) // 2
    center_y = (GAME_WINDOW['y'] + GAME_WINDOW['bottom_y']) // 2
    print("Moving mouse and shooting...")
    move_mouse(str(center_x), str(center_y), duration=str(0.5))
    shoot()

    # Move forward for 2 seconds
    print("Moving forward...")
    move_forward(duration=str(2))

    # Jump and crouch
    print("Jumping and crouching...")
    jump()
    time.sleep(0.5)
    crouch(duration=str(1))

    print("Test complete.")
