import numpy as np
import speech_recognition as sr
import whisper
import torch
import PySimpleGUI as sg

from datetime import datetime, timedelta
from queue import Queue
from time import sleep

MAX_RECORDING_SIZE = 6.0
NEW_PHRASE_TIMEOUT = 4.0

phrase_time = None
data_queue = Queue()
old_data = Queue()
recorder = sr.Recognizer()
recorder.energy_threshold = 1000
recorder.dynamic_energy_threshold = False

source = sr.Microphone(sample_rate=16000)
model = whisper.load_model("base.en")

transcript = [""]

with source:
    recorder.adjust_for_ambient_noise(source)


def record_callback(_, audio:sr.AudioData):
    """
    Threaded function to retrieve audio data (as raw bytes).
    """
    data = audio.get_raw_data()
    data_queue.put(data)
    old_data.put(data)

recorder.listen_in_background(source, record_callback, phrase_time_limit=MAX_RECORDING_SIZE)

while True:
    try:
        #Current time to compare
        now = datetime.utcnow()
        if data_queue.empty():
            continue
        phrase_complete = True if phrase_time and now - phrase_time > timedelta(seconds=NEW_PHRASE_TIMEOUT) else False
        if phrase_complete:
            audio_data = b''.join(data_queue.queue)
            old_data.queue.clear()
        else:
            audio_data = b''.join(old_data.queue)
            # print("hi")

        if phrase_time:
            print(now - phrase_time, ">", timedelta(seconds=NEW_PHRASE_TIMEOUT), phrase_complete)
        phrase_time = now
            
        data_queue.queue.clear()
        #     print("hi")
        # data_queue.queue()

        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0 # convert audio to something model can use.
        result = model.transcribe(audio_np, fp16=torch.cuda.is_available())
        text = result['text'].strip()
        print(text)
        print('', end='', flush=True)

        # if phrase_complete:
        #     transcript.append(text)
        # else:
        #     transcript[-1] = text
        #
        # print()

        #Sleep a bit for the CPU's sake.
        sleep(0.1)

    except KeyboardInterrupt:
        break


