# 🧠 Brain & AI Architecture Specification - Dr Strange Action

## 1. Computer Vision & Landmark Brain
The vision engine tracks 21 3D hand coordinates ($x, y, z$) per hand and evaluates finger extension ratios to distinguish palms from fists.

---

## 2. Mathematical Gesture Classifiers
- **Palm Open Test**:
$$d(\text{tip}, \text{wrist}) > 1.3 \times d(\text{mcp}, \text{wrist})$$
- **Fist Test**:
$$d(\text{tip}, \text{wrist}) < 1.1 \times d(\text{mcp}, \text{wrist})$$
- **Circle Detection**: Evaluates closed loop path distance and average radius from centroid.
