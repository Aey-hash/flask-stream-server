from flask import Flask, request, Response, render_template
import threading

app = Flask(__name__)

# Shared memory to store the latest frame
latest_frame = None
frame_lock = threading.Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    global latest_frame
    with frame_lock:
        latest_frame = request.data
    return "Frame received", 200

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            with frame_lock:
                if latest_frame is not None:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
