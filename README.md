# 🌀 Doctor Strange Hand Runes & Portal Effect (MediaPipe & OpenCV)

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Landmarker-00979D?style=for-the-badge&logo=google&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Localhost%20Web-000000?style=for-the-badge&logo=flask&logoColor=white)

An interactive, real-time Computer Vision application that uses AI-powered hand landmark tracking to cast **Doctor Strange-style Eldritch Magic Runes** and open glowing **Spark Portals** right on your webcam feed, available via **Desktop OpenCV Window** or **Localhost Web Streaming (http://localhost:5000)**!

---

## ✨ Features

- **🌐 Localhost Web Dashboard**: Stream live webcam feed with Doctor Strange magic overlays directly to your web browser at `http://localhost:5000`.
- **⚡ Real-Time Hand Tracking**: Uses Google MediaPipe Hand Landmarker to track 21 3D points on both hands simultaneously with minimal latency.
- **🪄 Eldritch Magical Runes**: Dynamic rotating geometric symbols, sacred geometry concentric rings, and outer glyph segments that align with your open palms.
- **🌀 Interactive Portal Summoning**: Make a **left-hand fist** anchor while drawing a **circle with your right index finger** in the air to ignite an energetic orange portal surrounded by floating sparks and dynamic particle physics.
- **🎆 Particle Engine**: Custom particle emission systems simulating sparks (`Spark` class) and fiery portal embers (`Particle` class) with realistic velocity, gravity decay, and color fading.
- **🎥 Auto-Camera Fallback**: Automatically scans camera indexes `[0, 1, 2]` to find and initialize your active webcam without configuration headaches.

---

## 🖐️ Gesture & Magic Guide

| Gesture | Action | Visual Effect |
| :--- | :--- | :--- |
| **Open Palm** | Hold hand flat towards camera | Rotating golden eldritch magic circle around palm |
| **Left Fist + Draw Circle** | Hold left fist & circle right index finger | Traces glowing magic trail; triggers portal expansion |
| **Release Fist** | Open left hand or lower hands | Portal smoothly shrinks and dissipates |
| **`Q` / `ESC`** | Keyboard input | Exit application |

---

## 🚀 How to Run

### 🌐 Option 1: Localhost Web Stream (http://localhost:5000)
Run the Flask server:
```bash
python server.py
```
Open **[http://localhost:5000](http://localhost:5000)** in any web browser to view your live webcam stream with Doctor Strange effects!

### 🖥️ Option 2: Native Desktop GUI Window
Run the OpenCV window app:
```bash
python app.py
```

---

## 📂 Project Structure

```
dr_strange_mediapipe/
├── server.py               # Flask web server for http://localhost:5000 stream
├── app.py                  # Main engine, gesture detection & desktop window mode
├── hand_landmarker.task    # Google MediaPipe 1.x vision model bundle
├── requirements.txt        # Python package dependencies
└── README.md               # Documentation & overview
```

---

## 📜 License

Distributed under the MIT License. Feel free to modify and expand with custom magical spells! 🪄✨
