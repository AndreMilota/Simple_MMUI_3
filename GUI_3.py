#GUI.py
from tkinter import scrolledtext
import tkinter as tk
from deepgram_ASR import DeepgramTranscriber  # Assume this is your transcriber file
from command_buffer import Command_Buffer

class Window:
    def __init__(self, title):
        self.gestures = ""

        self.root = tk.Tk()
        self.root.title(title)

        # Create command entry box
        self.command_entry = scrolledtext.ScrolledText(self.root, width=50, height=4)
        self.command_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Put the dialog box under it
        self.dialog_box = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.dialog_box.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Create Button 1
        self.button1 = tk.Button(self.root, text="Button 1", command=self.button1_clicked)
        self.button1.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ne")

        # Create Button 2
        self.button2 = tk.Button(self.root, text="Button 2", command=self.button2_clicked)
        self.button2.grid(row=0, column=1, padx=(0, 10), pady=40, sticky="ne")

        # Create a frame for the bottom buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # Create two new buttons
        self.undo_button = tk.Button(button_frame, text="Undo", command=self.on_undo)
        self.undo_button.pack(side=tk.LEFT, padx=(0, 5))

        self.toggle_ASR_button = tk.Button(button_frame, text="Start Transcription", command=self.on_toggle_transcription)
        self.toggle_ASR_button.pack(side=tk.LEFT, padx=(0, 5))

        # Create "Run" button
        self.run_button = tk.Button(button_frame, text="Run", command=self.run_callback)
        self.run_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Configure grid row and column weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

        self.todo = []

        print("the GUI is up and running")

    def on_undo(self):
        print("New Button 1 clicked")
        # Add your desired functionality here

    def on_toggle_transcription(self):
        print("New Button 2 clicked")
        # Add your desired functionality here

    # widget callbacks ------------------------------
    def run_callback(self):
        command = self.command_entry.get("1.0", "end-1c")
        self.run_callback_function(command, self.gestures)
        self.gestures = ""
        #if self.todo != None:
        #    self.set_button_color(self.todo[0], self.todo[1])
        for command in self.todo:
            command()
        self.todo = [] # clear the todo list

    def button1_clicked(self):
        self.gestures += "button 1 was indicated"
        print("Button 1 clicked")

    def button2_clicked(self):
        self.gestures += "button 2 was indicated"
        print("Button 2 clicked")

    # agent tolls calls ------------------------------
    def get_button_color(self, button_index):
        return self.button1.cget("background")

    def set_button_color(self, button_index, color):
        if button_index == 1:
            self.todo.append(lambda : self.button1.config(background=color))
        elif button_index == 2:
            self.todo.append(lambda : self.button2.config(background=color))


    def set_run_callback(self, run_callback_function):
        self.run_callback_function = run_callback_function

    def run(self):
        self.root.mainloop()

def main():
    # create the window
    gui = Window("GUI_3")
    gui.run()

if __name__ == "__main__":
    main()

