from flask import Flask, render_template, Response
import os

app = Flask(__name__)

# Global variable to store the latest frame
latest_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        global latest_frame
        while True:
            if latest_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    global latest_frame
    if 'frame' in flask.request.files:
        file = flask.request.files['frame']
        latest_frame = file.read()
        return 'Frame received', 200
    return 'No frame found', 400

if __name__ == '__main__':
    app.run()