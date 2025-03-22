from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

frame_holder = {"frame": None}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            if frame_holder["frame"] is not None:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_holder["frame"] + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    from flask import request
    file = request.files['frame']
    frame_holder["frame"] = file.read()
    return 'Frame received', 200
