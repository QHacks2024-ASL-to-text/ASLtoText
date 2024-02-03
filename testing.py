#from google.colab import files
#import os
#import tensorflow as tf
#assert tf.__version__.startswith('2')

#from mediapipe_model_maker import gesture_recognizer

#import matplotlib.pyplot as plt

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = '/absolute/path/to/gesture_recognizer.task'

base_options = BaseOptions(model_asset_path=model_path)

import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
