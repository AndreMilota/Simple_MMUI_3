#GUI.py

import tkinter as tk


class Window:
    def __init__(self, title):
        self.gestures = ""

        self.root = tk.Tk()
        self.root.title(title)

        # Create text entry box
        self.text_entry = tk.Text(self.root, width=50, height=20)
        self.text_entry.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create Button 1
        self.button1 = tk.Button(self.root, text="Button 1", command=self.button1_clicked)
        self.button1.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ne")

        # Create Button 2
        self.button2 = tk.Button(self.root, text="Button 2", command=self.button2_clicked)
        self.button2.grid(row=0, column=1, padx=(0, 10), pady=40, sticky="ne")

        # Create "Run" button
        self.run_button = tk.Button(self.root, text="Run", command=self.run_callback)
        self.run_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        # Configure grid row and column weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=0)

        self.todo = []

        print("the GUI is up and running")

    # widget callbacks ------------------------------
    def run_callback(self):
        command = self.text_entry.get("1.0", "end-1c")
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

    # def set_agent_executor(self, agent_executor):
    #     self.agent_executor = agent_executor

    # agent tolls calls ------------------------------
    def get_button_color(self, button_index):
        return self.button1.cget("background")

    def set_button_color(self, button_index, color):
        if button_index == 1:
            self.todo.append(lambda : self.button1.config(background=color))
        elif button_index == 2:
            self.todo.append(lambda : self.button2.config(background=color))

        # add lamda calls to the todo list
        # if button_index == 1:
        #     #self.button1.config(background=color)
        #     print("Button 1 color set to", color)
        #     self.todo.append(
        # elif button_index == 2:
        #     print("about to set Button 2 color to", color)
        #     self.button2.config(background=color)
        #     print("Button 2 color set to", color)

    # ----------------------------------------------
    def set_run_callback(self, run_callback_function):
        self.run_callback_function = run_callback_function

    def run(self):
        self.root.mainloop()