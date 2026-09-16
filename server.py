import cv2
import time
import os
from flask import Flask, render_template_string, Response
from app import DoctorStrangeProcessor

app = Flask(__name__)
processor = None
camera = None

def get_camera():
    global camera
    if camera is None or not camera.isOpened():
        for cam_idx in [0, 1, 2]:
            cap = cv2.VideoCapture(cam_idx)
            if cap.isOpened():
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                camera = cap
                print(f"[SERVER] Connected to webcam at index {cam_idx}")
                break
            cap.release()
    return camera

def generate_frames():
    global processor
    if processor is None:
        processor = DoctorStrangeProcessor()

    cam = get_camera()
    if cam is None or not cam.isOpened():
        print("[SERVER ERROR] No camera available.")
        return

    while True:
        success, frame = cam.read()
        if not success:
            time.sleep(0.03)
            continue

        try:
            processed_frame = processor.process_frame(frame)
            ret, buffer = cv2.imencode('.jpg', processed_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
            if not ret:
                continue
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except Exception as e:
            print(f"[SERVER FRAME ERROR]: {e}")
            time.sleep(0.03)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Doctor Strange Portal & Magic Runes | Localhost</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #08070d;
            --card-bg: rgba(22, 18, 36, 0.75);
            --gold: #ffb830;
            --orange: #ff6b00;
            --cyan: #00f2fe;
            --text-light: #e2e8f0;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 107, 0, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(255, 184, 48, 0.12) 0%, transparent 40%);
            color: var(--text-light);
            font-family: 'Outfit', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 1rem;
        }

        header {
            text-align: center;
            margin-bottom: 2rem;
        }

        h1 {
            font-family: 'Cinzel', serif;
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffe082 0%, var(--gold) 50%, var(--orange) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(255, 184, 48, 0.3);
            letter-spacing: 2px;
            margin-bottom: 0.5rem;
        }

        p.subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
        }

        .container {
            max-width: 1200px;
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 2rem;
        }

        @media (max-width: 968px) {
            .container {
                grid-template-columns: 1fr;
            }
        }

        .video-wrapper {
            position: relative;
            background: #000;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 0 40px rgba(255, 107, 0, 0.25), inset 0 0 2px rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 184, 48, 0.3);
            aspect-ratio: 16 / 9;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .video-wrapper img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .badge-live {
            position: absolute;
            top: 1rem;
            left: 1rem;
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid var(--orange);
            color: var(--gold);
            padding: 0.4rem 0.9rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            backdrop-filter: blur(8px);
        }

        .pulse-dot {
            width: 10px;
            height: 10px;
            background-color: var(--orange);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--orange);
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 15px var(--gold); }
            100% { transform: scale(0.95); opacity: 0.8; }
        }

        .sidebar {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .card {
            background: var(--card-bg);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }

        .card h2 {
            font-family: 'Cinzel', serif;
            font-size: 1.25rem;
            color: var(--gold);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid rgba(255, 184, 48, 0.2);
            padding-bottom: 0.5rem;
        }

        .gesture-item {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1.2rem;
        }

        .gesture-item:last-child {
            margin-bottom: 0;
        }

        .gesture-icon {
            font-size: 1.8rem;
            background: rgba(255, 184, 48, 0.1);
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255, 184, 48, 0.3);
            flex-shrink: 0;
        }

        .gesture-text h3 {
            font-size: 1rem;
            color: #f8fafc;
            margin-bottom: 0.2rem;
        }

        .gesture-text p {
            font-size: 0.85rem;
            color: #94a3b8;
            line-height: 1.4;
        }

        .info-box {
            background: rgba(0, 242, 254, 0.05);
            border: 1px solid rgba(0, 242, 254, 0.2);
            border-radius: 12px;
            padding: 1rem;
            font-size: 0.85rem;
            color: #cbd5e1;
            line-height: 1.5;
        }

        footer {
            margin-top: auto;
            padding-top: 2rem;
            color: #64748b;
            font-size: 0.9rem;
            text-align: center;
        }
    </style>
</head>
<body>

    <header>
        <h1>DOCTOR STRANGE PORTAL</h1>
        <p class="subtitle">Real-Time Computer Vision & Hand Landmark Magic Engine</p>
    </header>

    <div class="container">
        <div class="video-wrapper">
            <div class="badge-live">
                <div class="pulse-dot"></div>
                LIVE WEBCAM STREAM
            </div>
            <img src="/video_feed" alt="Doctor Strange Portal Feed">
        </div>

        <div class="sidebar">
            <div class="card">
                <h2>Mystic Gestures</h2>
                
                <div class="gesture-item">
                    <div class="gesture-icon">✋</div>
                    <div class="gesture-text">
                        <h3>Open Palm</h3>
                        <p>Hold your hand flat facing the camera to summon rotating golden Eldritch magic runes.</p>
                    </div>
                </div>

                <div class="gesture-item">
                    <div class="gesture-icon">✊</div>
                    <div class="gesture-text">
                        <h3>Left Fist + Circle</h3>
                        <p>Hold a fist with your left hand while drawing a circle with your right index finger to ignite a Portal!</p>
                    </div>
                </div>

                <div class="gesture-item">
                    <div class="gesture-icon">✨</div>
                    <div class="gesture-text">
                        <h3>Particle Physics</h3>
                        <p>Real-time spark decay and portal ember acceleration physics.</p>
                    </div>
                </div>
            </div>

            <div class="card">
                <h2>System Specs</h2>
                <div class="info-box">
                    <strong>Model:</strong> MediaPipe 1.x Hand Landmarker<br>
                    <strong>Resolution:</strong> 1280 x 720 HD<br>
                    <strong>Host:</strong> Localhost (Port 5000)<br>
                    <strong>Framework:</strong> OpenCV + Flask
                </div>
            </div>
        </div>
    </div>

    <footer>
        Doctor Strange MediaPipe Portal App | Running locally on <strong>http://localhost:5000</strong>
    </footer>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    print("==========================================================")
    print("DOCTOR STRANGE LOCALHOST WEB SERVER RUNNING")
    print("Open in your web browser: http://localhost:5000")
    print("==========================================================")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
