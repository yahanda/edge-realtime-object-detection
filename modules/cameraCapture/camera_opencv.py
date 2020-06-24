import os
import cv2
import requests
import json
from base_camera import BaseCamera
import numpy as np
import datetime

CONF_THRESH = 0.3

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        cameraw = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        camerah = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            imgencoded = cv2.imencode('.jpg', img)[1].tobytes()

            # Send an image to the custom vision server
            # Return the JSON response from the server with the prediction result
            res = requests.post(url='http://localhost:8080/objectDetector/image',
                    data=imgencoded,
                    headers={'Content-Type': 'application/octet-stream'})
            
            predictions = res.json()['predictions']

            # for debug
            #print(predictions) 

            if len(predictions) > 0 and len(predictions[0]) > 0:
                det_probability = det_tag_id =  det_tag_name = det_left = det_top = det_width = det_height = []

                for prediction in predictions:
                    det_probability = np.append(det_probability, prediction.get("probability"))
                    det_tag_id = np.append(det_tag_id, prediction.get("tagId"))
                    det_tag_name = np.append(det_tag_name, prediction.get("tagName"))
                    det_left = np.append(det_left, prediction.get("boundingBox").get("left"))
                    det_top = np.append(det_top, prediction.get("boundingBox").get("top"))
                    det_width = np.append(det_width, prediction.get("boundingBox").get("width"))
                    det_height = np.append(det_height, prediction.get("boundingBox").get("height"))
                
                top_indices = [i for i, conf in enumerate(det_probability) if float(conf) >= CONF_THRESH]
                top_probability = det_probability[top_indices]
                top_label_indices = det_tag_name[top_indices].tolist()
                top_tag_id = det_tag_id[top_indices]
                top_left = det_left[top_indices]
                top_top = det_top[top_indices]
                top_width = det_width[top_indices]
                top_height = det_height[top_indices]

                for i in range(top_probability.shape[0]):
                    xmin = int(round(float(top_left[i]) * cameraw))
                    ymin = int(round(float(top_top[i]) * camerah))
                    xmax = int(round((float(top_left[i]) + float(top_width[i])) * cameraw))
                    ymax = int(round((float(top_top[i]) + float(top_height[i])) * camerah))

                    # Draw the box on top of the image
                    #class_num = int(top_tag_id[i])
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

                    text = top_label_indices[i] + " " + ('%.2f' % float(top_probability[i]))
                    text_top = (xmin, ymin-10)
                    text_bot = (xmin + 80, ymin + 5)
                    text_pos = (xmin + 5, ymin)
                    cv2.rectangle(img, text_top, text_bot, (0, 255, 0), -1)
                    cv2.putText(img, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0,0), 1)
                    print(datetime.datetime.now(), text)

            yield cv2.imencode('.jpg', img)[1].tobytes()
