import json

from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from model_detection.camera import VideoCamera


# Create your views here.
def index(request):
    return render(request, 'model_detection/index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.username = "Anonymous"
        self.accept()
        self.send(text_data=json.dumps(
            {'message': f'[Welcome {self.username}!]'}
        ))

    def receive(self, *, text_data):
        text_data = json.loads(text_data)['message']
        if text_data.startswith('/name'):
            self.username = text_data[5:].strip()
            self.send(text_data=json.dumps(
                {'message': f'[set your username to {self.username}]'}
            ))
        else:
            self.send(text_data=json.dumps(
                {'message': self.username + ": " + text_data}
            ))

    def disconnect(self, message):
        pass
