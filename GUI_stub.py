# this is an offline test class for the simple GUI
# it should have all the functions that the agents uses
class Window():
    def __init__(self, title):
        self.button_colors = ['white', 'white', 'white']
        self.run_callback_function = None
    def set_button_color(self, button_index, color):
        self.button_colors[button_index] = color
    def set_run_callback(self, run_callback_function):
        self.run_callback_function = run_callback_function
    def run(self):
        None