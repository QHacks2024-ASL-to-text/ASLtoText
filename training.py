import cv2 as cv
import os
from mediapipe_model_maker import gesture_recognizer

datasetPath = r"c:\Users\Nicholas\Documents\bbbbb"
labels = [] 
for i in os.listdir(datasetPath):
    if os.path.isdir(os.path.join(datasetPath)):
        labels.append(i)
print(labels)

data = gesture_recognizer.Dataset.from_folder(
    dirname=datasetPath,
    hparams=gesture_recognizer.HandDataPreprocessingParams()
)

train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.5)


hparams = gesture_recognizer.HParams(export_dir="ASL_model")
options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)
model = gesture_recognizer.GestureRecognizer.create(
    train_data=train_data,
    validation_data=validation_data,
    options=options
)

loss, acc = model.evaluate(test_data, batch_size=1)
print(f"Test loss:{loss}, Test accuracy:{acc}")

model.export_model() 


