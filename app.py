from flask import Flask, request, render_template, Response
import threading

app = Flask(__name__)

# Store latest frame
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
    return 'Frame received', 200

def generate_frames():
    global latest_frame
    while True:
        with frame_lock:
            if latest_frame:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
        # Optional: Add short sleep to prevent overload
        # time.sleep(0.05)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')