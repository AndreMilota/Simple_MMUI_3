#GUI.py

import tkinter as tk
import os
import pyaudio # had to install this from the pychamr terminal it would not work on the GUI
import asyncio
import websockets # installed from the GUI and it worked
import json
import threading
from tkinter import scrolledtext
from deepgram import DeepgramClient #pip install deepgram-sdk --upgrade

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

        # ASR stuff

        self.DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
        deepgram: DeepgramClient = DeepgramClient(self.DEEPGRAM_API_KEY)

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 8000
        self.asr_enabled = False
        self.audio_queue = asyncio.Queue()
        self.running = True
        self.loop = None

        print("ASR stuff is up and running")

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

    def set_run_callback(self, run_callback_function):
        self.run_callback_function = run_callback_function

    # more ASR stuff ------------------------------

    def callback(self, input_data, frame_count, time_info, status_flags):
        if self.running:
            self.audio_queue.put_nowait(input_data)
        return (input_data, pyaudio.paContinue)

    async def microphone(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            stream_callback=self.callback
        )

        stream.start_stream()

        try:
            while self.running:
                await asyncio.sleep(0.1)
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

    async def process(self):
        extra_headers = {
            'Authorization': 'token ' + self.DEEPGRAM_API_KEY
        }

        async with websockets.connect('wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1',
                                      extra_headers=extra_headers) as ws:
            async def sender(ws):
                try:
                    while self.running:
                        data = await self.audio_queue.get()
                        if self.asr_enabled:  # Check ASR enabled before sending
                            await ws.send(data)
                except asyncio.CancelledError:
                    pass
                except Exception as e:
                    print('Error while sending: ', str(e))

            async def receiver(ws):
                try:
                    async for msg in ws:
                        if not self.running:
                            break

                        msg = json.loads(msg)

                        try:  # Check if the message has a transcript
                            transcript = msg['channel']['alternatives'][0]['transcript']
                            if transcript:
                                print(f'Transcript = {transcript}')
                        except (KeyError, IndexError):
                            print("No transcript found in message")
                except asyncio.CancelledError:
                    pass
                except websockets.exceptions.ConnectionClosedOK:
                    pass

            await asyncio.gather(sender(ws), receiver(ws))

    async def ASR_run(self):
        await asyncio.gather(self.microphone(), self.process())

    def start_async_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.ASR_run())

    def on_closing(self):
        print("on_closing")
        self.running = False
        self.root.destroy()
        if self.loop:
            for task in asyncio.all_tasks(self.loop):
                task.cancel()
            print("Tasks cancelled, scheduling loop stop")
            self.loop.call_soon_threadsafe(self.loop.stop)
            print("just called loop.call_soon_threadsafe(loop.stop)")

    def on_f4_press(self, event):
        self.asr_enabled = True
        # print("F4 key pressed down")

    def on_f4_release(self, event):
        self.asr_enabled = False
        # print("F4 key released")
    def run(self):
        #TODO start the asr loops

        # Bind F4 key down and up events
        self.root.bind("<KeyPress-F4>", self.on_f4_press)
        self.root.bind("<KeyRelease-F4>", self.on_f4_release)

        self.loop = asyncio.new_event_loop()
        thread = threading.Thread(target=self.start_async_loop, args=(self.loop,))
        thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.mainloop()

        self.loop.run_until_complete(self.loop.shutdown_asyncgens())
        self.loop.close()