from flask import Flask, request, render_template, send_file
from io import BytesIO
from threading import Lock

app = Flask(__name__)

latest_frame = None
lock = Lock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    global latest_frame
    with lock:
        latest_frame = request.files['frame'].read()
    return '', 200

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            with lock:
                if latest_frame is not None:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + latest_frame + b'\r\n')
    return app.response_class(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
