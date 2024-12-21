import pyautogui
import pygetwindow as gw
from PIL import Image, ImageChops
from globals import g

app_window = gw.getWindowsWithTitle(g.window_name)

left, top, width, height = 0,0,0,0

if app_window:
    app_window = app_window[0]
    left = app_window.left
    top = app_window.top
    width = app_window.width
    height = app_window.height

new_width = int(width / 5)
new_height = int(height / 5)

assert left + top + width + height

def capture_screenshot():
    # Capture current screen
    screenshot = pyautogui.screenshot()
    cropped_screenshot = screenshot.crop((left, top, left + width, top + height))
    resized_screenshot = cropped_screenshot.resize((new_width, new_height), Image.Resampling.LANCZOS)
    resized_screenshot.save("tomato.png")
    return resized_screenshot

def image_difference(img1, img2):
    """
    Returns a numerical difference between two images.
    A simple approach is to use the bounding box of ImageChops.difference.
    A non-zero bounding box indicates changes. 
    For more sensitive detection, consider summing pixel differences.
    """
    diff = ImageChops.difference(img1, img2)
    # Calculate a simple metric: sum of all pixel differences
    stat = diff.getbbox()
    if stat is None:
        return 0
    else:
        # Another method: sum of channel differences as a rough metric
        # Convert difference image to grayscale and sum pixel values
        gray_diff = diff.convert('L')
        total_diff = sum(gray_diff.getdata())
        return total_diff