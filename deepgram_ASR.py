import os
import pyaudio
import asyncio
import websockets
import json
import threading
import time
from deepgram import DeepgramClient
import keyboard # pip install keyboard

class DeepgramTranscriber:
    def __init__(self):
        self.DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
        self.deepgram = DeepgramClient(self.DEEPGRAM_API_KEY)

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 8000

        self.audio_queue = asyncio.Queue()
        self.running = False
        self.paused = True
        self.transcriber_thread = None
        self.on_result = None
        self.ws = None

    def callback(self, input_data, frame_count, time_info, status_flags):
        if not self.paused:
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

        while self.running:
            await asyncio.sleep(0.1)

        stream.stop_stream()
        stream.close()

    async def process(self):
        while self.running:
            try:
                extra_headers = {
                    'Authorization': 'token ' + self.DEEPGRAM_API_KEY
                }

                async with websockets.connect('wss://api.deepgram.com/v1/listen?encoding=linear16&sample_rate=16000&channels=1',
                                              extra_headers=extra_headers) as ws:
                    self.ws = ws
                    async def sender(ws):
                        try:
                            while self.running:
                                if not self.paused and not self.audio_queue.empty():
                                    data = await self.audio_queue.get()
                                    await ws.send(data)
                                else:
                                    await asyncio.sleep(0.1)
                        except Exception as e:
                            print('Error while sending: ', str(e))

                    async def receiver(ws):
                        async for msg in ws:
                            if not self.running or self.paused:
                                break
                            msg = json.loads(msg)
                            transcript = msg['channel']['alternatives'][0]['transcript']

                            if transcript:
                                if self.on_result:
                                    self.on_result(transcript)


                    await asyncio.gather(sender(ws), receiver(ws))
            except websockets.exceptions.ConnectionClosedError:
                if self.running and not self.paused:
                    print("Connection closed. Attempting to reconnect...")
                    await asyncio.sleep(1)
                else:
                    break

    async def run(self):
        self.running = True
        await asyncio.gather(self.microphone(), self.process())
    #
    # def start(self):
    #     self.transcriber_thread = threading.Thread(target=self._start_async)
    #     self.transcriber_thread.start()

    def start(self):
        if not self.transcriber_thread or not self.transcriber_thread.is_alive():
            self.transcriber_thread = threading.Thread(target=self._start_async)
            self.transcriber_thread.daemon = True  # This allows the thread to be terminated when the main program exits
            self.transcriber_thread.start()
    def _start_async(self):
        asyncio.run(self.run())

    def stop(self):
        self.running = False
        self.paused = True
        if self.transcriber_thread:
            self.transcriber_thread.join()
        print("Transcriber stopped.")

    def set_on_result(self, on_result):
        self.on_result = on_result

    def pause(self):
        if not self.paused:
            self.paused = True
            print("Transcription paused.")

    # def unpause(self):
    #     if self.paused:
    #         self.paused = False
    #         print("Transcription unpaused.")
    #         if self.ws is None or self.ws.closed:
    #             #print("Reconnecting...")
    #             self.transcriber_thread = threading.Thread(target=self._start_async)
    #             self.transcriber_thread.start()
    def unpause(self):
        self.paused = False
        print("Transcription unpaused.")
        if self.ws is None or self.ws.closed:
            print("Reconnecting...")
            self.start()  # This will start a new thread if needed
def main():
    transcriber = DeepgramTranscriber()
    transcriber.set_on_result(lambda text: print(f"Transcribed text: {text}"))

    def on_key_event(e):
        if e.event_type == keyboard.KEY_DOWN and e.name == 'f4':
            transcriber.unpause()
        elif e.event_type == keyboard.KEY_UP and e.name == 'f4':
            transcriber.pause()

    keyboard.hook(on_key_event)

    try:
        print("Press F4 to start/stop transcription. Press Ctrl+C to exit.")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping transcriber...")
        transcriber.stop()
        print("Main program finished.")

if __name__ == '__main__':
    main()
