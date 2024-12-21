import pyautogui
import pygetwindow as gw
from PIL import Image, ImageChops

game_name = "Sid Meier's Civilization V (DX9)"
app_window = gw.getWindowsWithTitle(game_name)

left, top, width, height = 0,0,0,0


if app_window:
    app_window = app_window[0]
    left = app_window.left
    top = app_window.top
    width = app_window.width
    height = app_window.height


height_of_screen = top + height
width_of_screen = width + left