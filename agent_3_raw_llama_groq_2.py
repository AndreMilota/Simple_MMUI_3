# this is an agent implemented with llama and Groq but not langchain
import os
import json
from groq import Groq
import GUI_4 as GUI
import GUI_stub_wrapper as GUI_Offline # for testing
import offline_tests as OT

# load the key for the Groq API
groq_key = os.environ.get('GROQ_KEY')
MODEL = 'llama3-groq-70b-8192-tool-use-preview'
# get the key and create a client
client = Groq(api_key=groq_key, )

class MMUI:
    def __init__(self, gui=None, window_name=None):
        if not gui:
            if not window_name:
                # get the python file name
                window_name = os.path.basename(__file__).split(".")[0]
            gui = GUI.Window(number_of_buttons=3, title=window_name)
        self.gui = gui
        self.nunber_of_buttons = gui.get_number_of_buttons()

    def reset(self):
        self.gui.reset()

    def get_gui(self):
        return self.gui

    def callback_function(command, gestures):
        # all the work goes here
        pass
    def run(self):
        self.gui.set_run_callback(self.callback_function)
        self.gui.run()


def main():
    # to run it normaly
    mmui = MMUI()

    # to run it with offline tests
    # gui = GUI_Offline.Window("window_name")
    # mmui = MMUI(gui=gui)

    mmui.run()

if __name__ == "__main__":
    main()