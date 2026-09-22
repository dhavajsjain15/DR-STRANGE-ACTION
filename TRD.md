# ⚙️ Technical Requirement Document (TRD) - Dr Strange Action

## 1. System Architecture
The application runs a continuous vision processing loop using OpenCV and MediaPipe 1.x `HandLandmarker` Task API.

```
+-------------------+     +-------------------------+     +------------------------+
| Camera Frame      | --> | MediaPipe HandLandmark  | --> | Gesture Classifier     |
| (cv2.VideoCapture)|     | (hand_landmarker.task)  |     | (is_palm_open/is_fist) |
+-------------------+     +-------------------------+     +------------------------+
                                                                      |
                                                                      v
+-------------------+     +-------------------------+     +------------------------+
| Render Output     | <-- | Particle Physics Engine | <-- | Magic Circle Renderer  |
| (cv2.imshow/Flask)|     | (Spark/Particle Engine) |     | (Geometry & Glows)     |
+-------------------+     +-------------------------+     +------------------------+
```

---

## 2. Technical Stack Specifications
- **Language**: Python 3.9 - 3.14
- **Computer Vision**: OpenCV (`opencv-python`)
- **AI Task API**: Google MediaPipe `HandLandmarker` (`hand_landmarker.task`)
- **Web Server**: Flask (MJPEG streaming on port 5000)
- **Math/Physics**: NumPy & `math` module
