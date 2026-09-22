# 🌀 Product Requirement Document (PRD) - Dr Strange Action (Portal & Hand Runes)

## 1. Executive Summary
Dr Strange Action is a real-time Computer Vision application that utilizes Google MediaPipe AI Hand Tracking and custom particle physics rendering to superimpose Doctor Strange-style Eldritch Magic Runes and dynamic portal effects onto a webcam stream.

---

## 2. Product Goals & Feature Requirements
- **Real-Time Landmark Detection**: Detect 21 3D hand landmarks per hand with sub-30ms latency.
- **Dynamic Eldritch Magic Runes**: Render concentric, rotating geometric runes around open palms.
- **Interactive Portal Summoning**: Anchor left fist while tracing right finger circle to ignite glowing orange spark portals.
- **Dual Display Modes**: Desktop OpenCV window mode (`app.py`) and Flask MJPEG web streaming mode (`http://localhost:5000`).

---

## 3. Success Metrics
- **Frame Rate Target**: $\ge 30$ FPS rendering output at 720p HD resolution.
- **Gesture Recognition Latency**: $\le 100$ ms detection time for open palm and fist gestures.
