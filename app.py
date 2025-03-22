from flask import Flask, Response, render_template
import threading
import time

app = Flask(__name__)
frame_lock = threading.Lock()
latest_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        global latest_frame
        while True:
            with frame_lock:
                if latest_frame:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
            time.sleep(0.1)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    global latest_frame
    from flask import request
    with frame_lock:
        latest_frame = request.data
    return 'Frame received', 200
