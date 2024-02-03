import argparse
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch
# import PySimpleGUI as sg

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

MAX_RECORDING_SIZE = 3.0
NEW_PHRASE_TIMEOUT = 1.3

phrase_time = None
data_queue = Queue()

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
    Threaded callback function to retrieve audio data (as raw bytes).
    """
    data = audio.get_raw_data()
    data_queue.put(data)

recorder.listen_in_background(source, record_callback, phrase_time_limit=MAX_RECORDING_SIZE)

while True:
    try:
        #Current time to compare
        now = datetime.utcnow()
        if data_queue.empty():
            continue
        
        phrase_complete = True if phrase_time and now - phrase_time > timedelta(seconds=NEW_PHRASE_TIMEOUT) else False
        phrase_time = now
        audio_data = b''.join(data_queue.queue) # gets the audio data as binary from the queue.

        if phrase_complete:
            data_queue.queue.clear()
        data_queue.queue()

        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0 # convert audio to something model can use.
        result = model.transcribe(audio_np, fp16=torch.cuda.is_available())
        text = result['text'].strip()
        print(text)
        # if phrase_complete:
        #     transcript.append(text)
        # else:
        #     transcript[-1] = text
        #
        # print()
        time.sleep(0.2)

    except KeyboardInterrupt:
        break


