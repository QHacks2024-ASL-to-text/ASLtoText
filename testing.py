
import time

import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
BaseOptions = mp.tasks.BaseOptions

model_path = r'ASL_model/gesture_recognizer.task'

base_options = BaseOptions(model_asset_path=model_path)
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

class Word():
    last = ""
    word = ""
    string = ""
    def add(self, x):
        if x!= self.last:
            self.word+=x
            self.last = x
            print(self.word)
        elif x == "space": 
            self.string+=self.word+" "
        #elif x == "del":
        #    self.getString()

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
            stringObj.add(y)
            
        


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
        elif cv.waitKey(1) == ord('p'):
            stringObj.print()
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()
    
    