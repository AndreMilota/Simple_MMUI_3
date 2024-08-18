#  In this version we can have more buttons and the callbacks are done with lambda functions
from tkinter import scrolledtext
import tkinter as tk
from deepgram_ASR import DeepgramTranscriber  # Assume this is your transcriber file
from command_buffer import Command_Buffer
from back_end import Back_End


class Window(Back_End):
    def __init__(self, title="GUI 4", transcriber=None, number_of_buttons=3):
        super().__init__(number_of_buttons=number_of_buttons)
        self.gestures = ""

        self.root = tk.Tk()
        self.root.title(title)

        self.dialog_box = scrolledtext.ScrolledText(self.root, width=50, height=20)
        self.dialog_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.command_entry = scrolledtext.ScrolledText(self.root, width=50, height=4)
        self.command_entry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.buttons = []
        # comput spacing for the buttons
        pad_incroment = 300 / number_of_buttons
        for i in range(number_of_buttons):
            button = tk.Button(self.root, text=f"Button {i}", command=lambda j=i: self.button_clicked(j))
            button.grid(row=0, column=1, padx=(0, 10), pady=10 + i * pad_incroment, sticky="ne")
            # set the color, so it is consistent with the back end
            button.config(background=super().get_button_color(i))
            self.buttons.append(button)

        # Create a frame for the bottom buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # Create two new buttons
        self.undo_button = tk.Button(button_frame, text="Undo", command=self.on_undo)
        self.undo_button.pack(side=tk.LEFT, padx=(0, 5))

        self.toggle_ASR_button = tk.Button(button_frame, text="Start Transcription", command=self.toggle_transcription)
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

        # when I trued it without the delayed_action list it did now work
        self.delayed_action = []

        # Bind F4 key events
        self.root.bind('<KeyPress-F4>', self.on_f4_press)
        self.root.bind('<KeyRelease-F4>', self.on_f4_release)
        self.root.bind('<KeyPress-F1>', self.on_f1_press)
        self.root.bind('<KeyPress-F5>', self.on_f5_press)

        # Initialize the transcriber
        if transcriber is None:
            self.transcriber = DeepgramTranscriber()
        else:
            self.transcriber = transcriber  # use the one it was given
        self.transcriber.set_on_result(self.update_text)
        self.is_transcribing = False

        self.Command_Buffer = Command_Buffer()

        print("the GUI is up and running")

    def on_f4_press(self, event):
        if not self.is_transcribing:
            print("F4 pressed")
            self.toggle_transcription()

    def on_f4_release(self, event):
        print("F4 released")
        if self.is_transcribing:
            self.toggle_transcription()
        # self.transcriber.pause()
        # self.toggle_button.config(text="Start Transcription")

    def on_f1_press(self, event):
        print("F1 pressed")
        # pop a command off the command buffer
        self.Command_Buffer.undo()
        # display the text
        pending_command = self.Command_Buffer.get_command()
        # replace the text in the text box with the pending command
        self.command_entry.delete('1.0', tk.END)
        self.command_entry.insert(tk.END, pending_command)

    def on_f5_press(self, event):
        print("F5 pressed")
        pending_command = self.Command_Buffer.get_command()
        # TODO insert run action here
        self.Command_Buffer.clear_buffer()
        self.text_area.delete('1.0', tk.END)

    # process typing in the text box
    def update_text(self, text):
        # add the text to the command
        self.Command_Buffer.add_command(text)
        # display the text
        pending_command = self.Command_Buffer.get_command()
        # replace the text in the text box with the pending command
        self.command_entry.delete('1.0', tk.END)
        self.command_entry.insert(tk.END, pending_command)
        # self.text_area.insert(tk.END, text + "\n")
        # self.text_area.see(tk.END)  # Scroll to the end

    def on_undo(self):
        # pop a command off the command buffer
        self.Command_Buffer.undo()
        # display the text
        pending_command = self.Command_Buffer.get_command()
        # replace the text in the text box with the pending command
        self.command_entry.delete('1.0', tk.END)
        self.command_entry.insert(tk.END, pending_command)

    def toggle_transcription(self):
        if self.is_transcribing:
            self.transcriber.pause()
            self.toggle_ASR_button.config(text="Start Transcription")
            self.is_transcribing = False
        else:
            self.transcriber.unpause()
            self.toggle_ASR_button.config(text="Stop Transcription")
            self.is_transcribing = True

    # widget callbacks ------------------------------

    def take_action(self, command):
        self.run_callback_function(command, self.gestures)
        self.gestures = ""
        #if self.todo != None:
        #    self.set_button_color(self.todo[0], self.todo[1])
        print("todo list size ", len(self.delayed_action))
        for command in self.delayed_action:
            command()
        self.delayed_action = []  # clear the todo list

    def run_callback(self):
        command = self.command_entry.get("1.0", "end-1c")
        print(f"Running command: {command}")
        self.take_action(command)

    def button_clicked(self, button_index):
        description = f"Button {button_index} was indicated"
        self.gestures += description
        print(description)

    def get_button_color(self, button_index):
        print("Getting button color", button_index)
        memory_color = super().get_button_color(button_index)
        return memory_color

    def set_button_color(self, button_index, color):
        # Capture the class and instance in the lambda
        cls = super(Window, self)
        # todo see if we still need delayed actioins or if we can just do it now
        # todo add code to check color and reject invalid colors
        # todo add code to repor if calling this made any change
        self.delayed_action.append(lambda: cls.set_button_color(button_index, color))
        self.delayed_action.append(lambda: self.buttons[button_index].config(background=color))

    def set_run_callback(self, run_callback_function):
        print("Setting run callback function")
        self.run_callback_function = run_callback_function

    def run(self):
        self.root.mainloop()

def main():
    # create the window
    transcriber = DeepgramTranscriber()
    gui = Window("GUI_3", transcriber=transcriber)
    gui.run()

if __name__ == "__main__":
    main()
