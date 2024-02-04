
import time
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import mediapipe as mp
from collections import Counter

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
BaseOptions = mp.tasks.BaseOptions

model_path = r'./ASL_model/gesture_recognizer.task'

base_options = BaseOptions(model_asset_path=model_path)
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

class Word():
    LENGTH_CHECK = 5 # The number of charachters which must be added before the stream gets checked for a charachter again. 
    char_counter = 0
    # last = ""
    output = []
    current_word = ""
    buffer = ""
    def get_likely_letter(self):
        """
        params: stream: a stream of letters taken raw from the engine
        returns: tuple: most likely letter/symbol in the stream or None.
        """
        buffer_len = len(self.buffer) 
        if buffer_len < 20:
            return None
        elif buffer_len > 200:
            # Just a failsafe, to try and clear the buffer if some glitch happens in the system.
            self.buffer = ""
            return None
        else:
            c = Counter(self.buffer[0:15]).most_common(1)[0]
            last_c_index = self.buffer.rfind(c)
            if buffer_len - last_c_index < 5:
                return None
            
            


    def add(self, x):
        """
        returns True if a new word has just been added (detected space), False otherwise.
        """
        self.char_counter += 1
        self.buffer = self.buffer + x
        # if x!= self.last:
        #     self.string+=x +" "
        #     self.last = x

        return True
    
    def print(self):
        print(self.string)

    def getLast(self):
        return self.last
    
    def getString(self):
        return self.string

# Create a gesture recognizer instance with the live stream mode:
def result_string(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    """
    Parses 
    """
    x = None
    for gesture in result.gestures:
        x  = ([category.category_name for category in gesture])
    if(x!=None):
        y = x[0]
        if(y!= "None"):
            if (stringObj.add(y)):
                stringObj.print()
        


options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=result_string)



with GestureRecognizer.create_from_options(options) as recognizer:
    stringObj = Word()
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    windowName = "live feed"
    cv.namedWindow('frame', cv.WINDOW_NORMAL)  

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        cv.imshow('frame',frame)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        recognizer.recognize_async(mp_image, mp.Timestamp.from_seconds(time.time()).value )
        

        # Display the resulting frame
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
    
