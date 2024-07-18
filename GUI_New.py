import tkinter as tk
from tkinter import scrolledtext, ttk

# import matplotlib.pyplot as plt
# import numpy as np
# import sounddevice as sd
# import soundfile as sf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

from NonFilter import SpectrumAnalyzer


class App:
    """
    Main GUI.
    """

    def __init__(self, root):
        self.root = root
        self.root.minsize(300, 300)
        self.root.title("Audio GUI with python-sounddevice")
        self.root.columnconfigure([0, 1], weight=1, minsize=50)
        self.root.rowconfigure(0, weight=1, pad=10)
        self.root.rowconfigure(1, weight=1, minsize=50)
        self.root.rowconfigure(2, weight=1, minsize=50)

        # audio player1 component
        self.audio_player_canvas = tk.Frame(self.root)
        self.audio_player_canvas.grid(row=0, column=0, sticky="NSEW", rowspan=2)
        self.audio_player_spectrum = SpectrumAnalyzer()
        self.audio_record = tk.Button(
            self.audio_player_canvas, text="Record", command=self.record_or_stop_clicked
        )
        self.audio_record.pack(side=tk.LEFT)

        # tab control component
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.grid(row=2, column=0, sticky="NSEW")

        # image component for tab(1) control
        self.image_frame_tab1 = tk.Frame(self.tab_control)
        self.image_frame_top = tk.Frame(self.image_frame_tab1)
        self.image_frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.image_frame_bottom = tk.Frame(self.image_frame_tab1)
        self.image_frame_bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(
            self.image_frame_top, text="Input the image please."
        )
        self.image_label.pack(side=tk.LEFT)
        self.image_btn = tk.Button(
            self.image_frame_top, text="Select Image", command=self.select_image_clicked
        )
        self.image_btn.pack(side=tk.LEFT)
        self.img = ImageTk.PhotoImage(Image.open("image.jpg"))
        self.image = tk.Label(self.image_frame_bottom, image=self.img)
        self.image.pack(fill=tk.BOTH, expand=True)

        # 2 buttons component
        self.btn_frame_tab2 = tk.Frame(self.tab_control)
        self.button1 = tk.Button(
            self.btn_frame_tab2, text="Button 1", command=self.tab_btn1_clicked
        )
        self.button1.pack(side=tk.LEFT)
        self.button2 = tk.Button(
            self.btn_frame_tab2, text="Button 2", command=self.tab_btn2_clicked
        )
        self.button2.pack(side=tk.LEFT)

        self.tab_control.add(self.image_frame_tab1, text="Image")
        self.tab_control.add(self.btn_frame_tab2, text="Buttons")
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # model choice component
        self.llm_model_frame = tk.Frame(self.root)
        self.llm_model_frame.grid(row=0, column=1, sticky="NE")
        self.model_combobox = ttk.Combobox(self.llm_model_frame)
        self.model_combobox["values"] = ["GPT-3", "GPT-4"]
        self.model_combobox.current(0)
        self.model_combobox.pack(side=tk.RIGHT)

        self.model_btn = tk.Button(
            self.llm_model_frame, text="Submit", command=self.model_submit
        )
        self.model_btn.pack(side=tk.RIGHT)

        # Speech Text component
        self.speech_text_frame = tk.Frame(self.root)
        self.speech_text_frame.grid(row=1, column=1, sticky="NSEW")
        self.speech_text = scrolledtext.ScrolledText(self.speech_text_frame)
        self.speech_text.pack(fill=tk.BOTH, expand=True)
        self.speech_text.config(state=tk.DISABLED)

        # AI responded component
        self.ai_responded_frame = tk.Frame(self.root)
        self.ai_responded_frame.grid(row=2, column=1, sticky="NSEW")
        self.ai_responded = scrolledtext.ScrolledText(self.ai_responded_frame)
        self.ai_responded.pack(fill=tk.BOTH, expand=True)

    def record_or_stop_clicked(self):
        if self.audio_record["text"] == "Record":
            self.audio_record["text"] = "Stop"
            self.audio_player_spectrum.start()
            # self.ai_audio_player.play_audio()
        else:
            self.audio_record["text"] = "Record"
            # self.ai_audio_player.stop_audio()
            self.audio_player_spectrum.stop()

    def select_image_clicked(self):
        pass

    def model_submit(self):
        pass

    def tab_btn1_clicked(self):
        pass

    def tab_btn2_clicked(self):
        pass

    def on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        self.speech_text.config(state=tk.NORMAL)
        self.speech_text.insert(tk.END, f"Switched to: {tab_text}\n")
        self.speech_text.see(tk.END)
        self.speech_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
