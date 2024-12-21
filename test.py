import pyautogui


pyautogui.FAILSAFE = False

from controls import center_mouse, update_window_coordinates

update_window_coordinates()

center_mouse()