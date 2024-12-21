
import pygetwindow as gw

class Globals:
    window_name: str
    _controls: str = None
    

    def __init__(self, window_name=None):
        if not window_name:
            window_list = gw.getAllTitles()
            options = ""
            for x, title in enumerate(window_list):
                options += f"{x}: {title}\n"

        
            window_index = input("\nChoose a window\n" + options)
            self.window_name = window_list[int(window_index)]
        else:
            self.window_name = window_name

        print(f"Game window {self.window_name} Selected")


    @property
    def controls(self):
        if not self._controls:
            from reasoning import describe_controls, describe_how_to_play
            self._controls = describe_controls()
        return self._controls




g = Globals()
# g = Globals('Reigns')
