 # This class wraps the GUI application But provides mock functions that we can use to run this thing offline. Unlike
 # GUI_stub it  inherits from the actual GUI and so if we add  elements to the  application  we  won't always have to
 # re-implement them in this class. For instance we might want to add something to the GUI that tracks the history of
 # all the buttons.

import GUI_4 as GUI

class Window(GUI.Window):
    def __init__(self, title):
        super().__init__(title)
        self.button_colors = ['white', 'white', 'white']
        self.run_callback_function = None

    # def set_button_color(self, button_index, color):
    #     self.todo.append(lambda: self.button_colors[button_index] (background=color))

    # def get_button_color(self, button_index):
    #     out = super().get_button_color(button_index)
    #     return out
    def set_run_callback(self, run_callback_function):
        self.run_callback_function = run_callback_function

    def run(self):
        None

    # def button1_clicked(self):
    #     self.gestures += "button 1 was indicated"
    #
    # def button2_clicked(self):
    #     self.gestures += "button 2 was indicated"

    def click_button(self, button_index):
        self.button_clicked(button_index)
        # if button_index == 1:
        #     self.button1_clicked()
        # elif button_index == 2:
        #     self.button2_clicked()
    # def take_action(self, command):
    #     self.run_callback_function(command, self.gestures)
    #     self.gestures = ""
    #     # if self.todo != None:
    #     #    self.set_button_color(self.todo[0], self.todo[1])
    #     for c in self.todo:
    #         c()
    #     self.todo = []  # clear the todo list

def main():
    # create the window
    gui = Window("malkup")
    gui.run()