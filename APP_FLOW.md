# 🔄 App Flow & User Journey - Dr Strange Action

## 1. Flow Diagram

```mermaid
graph TD
    A[Launch App / Server] --> B[Webcam Capture Starts]
    B --> C[MediaPipe Extracts 21 Hand Landmarks]
    C --> D{Gesture Recognized?}
    D -- Open Palm --> E[Render Rotating Eldritch Magic Circles]
    D -- Left Fist + Right Index Circle --> F[Trace Spark Trail & Ignite Portal]
    D -- No Gesture --> G[Render Default Feed]
    E --> H[Composite & Display Output Frame]
    F --> H
    G --> H
```
