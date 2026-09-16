import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import math
import time
import random
import os

def is_palm_open(hand_landmarks):
    wrist = hand_landmarks[0]
    extended = 0
    tips = [8, 12, 16, 20]
    mcps = [5, 9, 13, 17]
    
    for tip, mcp in zip(tips, mcps):
        d_tip_wrist = math.hypot(hand_landmarks[tip].x - wrist.x, hand_landmarks[tip].y - wrist.y)
        d_mcp_wrist = math.hypot(hand_landmarks[mcp].x - wrist.x, hand_landmarks[mcp].y - wrist.y)
        if d_tip_wrist > d_mcp_wrist * 1.3:
            extended += 1
            
    thumb_tip = hand_landmarks[4]
    thumb_ip = hand_landmarks[3]
    if abs(thumb_tip.x - thumb_ip.x) > 0.02 or abs(thumb_tip.y - thumb_ip.y) > 0.02:
        extended += 1

    return extended >= 4

def is_fist(hand_landmarks):
    wrist = hand_landmarks[0]
    curled = 0
    tips = [8, 12, 16, 20]
    mcps = [5, 9, 13, 17]
    
    for tip, mcp in zip(tips, mcps):
        d_tip_wrist = math.hypot(hand_landmarks[tip].x - wrist.x, hand_landmarks[tip].y - wrist.y)
        d_mcp_wrist = math.hypot(hand_landmarks[mcp].x - wrist.x, hand_landmarks[mcp].y - wrist.y)
        if d_tip_wrist < d_mcp_wrist * 1.1:
            curled += 1
            
    return curled >= 3


def get_palm_center(hand_landmarks, w, h):
    wrist = hand_landmarks[0]
    middle_mcp = hand_landmarks[9]
    cx = int((wrist.x + middle_mcp.x) / 2 * w)
    cy = int((wrist.y + middle_mcp.y) / 2 * h)
    return cx, cy


def get_palm_size(hand_landmarks, w, h):
    wrist = hand_landmarks[0]
    middle_mcp = hand_landmarks[9]
    dist = math.sqrt((wrist.x - middle_mcp.x)**2 * w**2 + (wrist.y - middle_mcp.y)**2 * h**2)
    return dist

def check_circle_gesture(points, min_perimeter=300, close_threshold=60):
    if len(points) < 20:
        return False, None, 0
        
    end_pt = points[-1]
    
    path_dist = 0
    for i in range(len(points)-2, -1, -1):
        dx = points[i+1][0] - points[i][0]
        dy = points[i+1][1] - points[i][1]
        path_dist += math.hypot(dx, dy)
        
        if path_dist > min_perimeter:
            dist_to_old = math.hypot(end_pt[0] - points[i][0], end_pt[1] - points[i][1])
            if dist_to_old < close_threshold:
                loop_points = points[i:]
                cx = sum([p[0] for p in loop_points]) / len(loop_points)
                cy = sum([p[1] for p in loop_points]) / len(loop_points)
                radii = [math.hypot(p[0]-cx, p[1]-cy) for p in loop_points]
                avg_radius = sum(radii) / len(radii)
                return True, (int(cx), int(cy)), avg_radius
                
    return False, None, 0

class Spark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2) + 1.0
        self.life = random.uniform(0.3, 0.6)
        self.max_life = self.life
        self.size = random.randint(2, 4)

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.life -= dt
        return self.life > 0

    def draw(self, frame):
        alpha = max(0, self.life / self.max_life)
        color = (int(30 * alpha), int(140 * alpha + 80 * (1 - alpha)), int(255 * alpha))
        cv2.circle(frame, (int(self.x), int(self.y)), self.size, color, -1)

class Particle:
    def __init__(self, cx, cy, radius):
        angle = random.uniform(0, 2 * math.pi)
        r = random.uniform(radius * 0.9, radius * 1.1)
        self.x = cx + r * math.cos(angle)
        self.y = cy + r * math.sin(angle)
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)
        self.life = random.uniform(0.3, 1.0)
        self.max_life = self.life
        self.size = random.randint(1, 3)

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.life -= dt
        return self.life > 0

    def draw(self, frame):
        alpha = max(0, self.life / self.max_life)
        b = int(30 * alpha)
        g = int(140 * alpha + 80 * (1 - alpha))
        r = int(255 * alpha)
        color = (b, g, r)
        cv2.circle(frame, (int(self.x), int(self.y)), self.size, color, -1)

def draw_rune_segments(frame, cx, cy, radius, angle_offset, num_segments, thickness, color, alpha=1.0):
    seg_angle = (2 * math.pi) / num_segments
    arc_len = seg_angle * 0.4

    for i in range(num_segments):
        start_angle = angle_offset + i * seg_angle
        end_angle = start_angle + arc_len
        pts = []
        steps = 10
        for s in range(steps + 1):
            a = start_angle + (end_angle - start_angle) * s / steps
            x = int(cx + radius * math.cos(a))
            y = int(cy + radius * math.sin(a))
            pts.append((x, y))
        for j in range(len(pts) - 1):
            col = tuple(int(c * alpha) for c in color)
            cv2.line(frame, pts[j], pts[j + 1], col, thickness, cv2.LINE_AA)

def draw_geometric_symbols(frame, cx, cy, radius, angle_offset, num_symbols, color, alpha=1.0):
    for i in range(num_symbols):
        angle = angle_offset + i * (2 * math.pi / num_symbols)
        sx = cx + radius * math.cos(angle)
        sy = cy + radius * math.sin(angle)
        size = max(3, int(radius * 0.06))

        col = tuple(int(c * alpha) for c in color)

        if i % 3 == 0:
            pts = np.array([
                [int(sx), int(sy - size)],
                [int(sx - size * 0.866), int(sy + size * 0.5)],
                [int(sx + size * 0.866), int(sy + size * 0.5)]
            ], np.int32)
            cv2.polylines(frame, [pts], True, col, 1, cv2.LINE_AA)
        elif i % 3 == 1:
            pts = np.array([
                [int(sx), int(sy - size)],
                [int(sx + size), int(sy)],
                [int(sx), int(sy + size)],
                [int(sx - size), int(sy)]
            ], np.int32)
            cv2.polylines(frame, [pts], True, col, 1, cv2.LINE_AA)
        else:
            cv2.circle(frame, (int(sx), int(sy)), size, col, 1, cv2.LINE_AA)

def draw_magic_circle(frame, cx, cy, radius, t, intensity=1.0):
    orange = (30, 140, 255)
    gold = (50, 180, 255)
    bright_gold = (80, 210, 255)
    white_gold = (150, 230, 255)

    alpha = min(1.0, float(intensity))

    glow_overlay = frame.copy()
    for g in range(3):
        r = int(radius * (1.15 + g * 0.08))
        col = tuple(int(c * alpha * (0.3 - g * 0.08)) for c in orange)
        cv2.circle(glow_overlay, (cx, cy), r, col, 2, cv2.LINE_AA)
    cv2.addWeighted(glow_overlay, 0.5, frame, 0.5, 0, frame)

    cv2.circle(frame, (cx, cy), int(radius), tuple(int(c * alpha) for c in bright_gold), 3, cv2.LINE_AA)
    cv2.circle(frame, (cx, cy), int(radius), (255, 255, 255), 1, cv2.LINE_AA)

    draw_rune_segments(frame, cx, cy, radius * 0.95, t * 0.8, 36, 2, gold, alpha * 0.9)
    draw_rune_segments(frame, cx, cy, radius * 0.90, -t * 0.6, 24, 3, orange, alpha * 0.7)

    pts_oct = []
    for i in range(8):
        angle = t * 0.5 + i * (math.pi / 4)
        x = int(cx + radius * 0.82 * math.cos(angle))
        y = int(cy + radius * 0.82 * math.sin(angle))
        pts_oct.append([x, y])
    cv2.polylines(frame, [np.array(pts_oct, np.int32)], True, tuple(int(c * alpha) for c in bright_gold), 2, cv2.LINE_AA)

    for i in range(12):
        angle = -t * 0.4 + i * (math.pi / 6)
        r_outer = radius * 0.82
        r_inner = radius * 0.65
        x1 = int(cx + r_outer * math.cos(angle))
        y1 = int(cy + r_outer * math.sin(angle))
        x2 = int(cx + r_inner * math.cos(angle))
        y2 = int(cy + r_inner * math.sin(angle))
        cv2.line(frame, (x1, y1), (x2, y2), tuple(int(c * alpha * 0.8) for c in gold), 2, cv2.LINE_AA)
        cv2.circle(frame, (x2, y2), 4, tuple(int(c * alpha) for c in white_gold), -1, cv2.LINE_AA)

    cv2.circle(frame, (cx, cy), int(radius * 0.65), tuple(int(c * alpha) for c in orange), 2, cv2.LINE_AA)

    for offset in [0, math.pi / 4]:
        pts_sq = []
        for i in range(4):
            angle = t * 1.5 + offset + i * (math.pi / 2)
            x = int(cx + radius * 0.50 * math.cos(angle))
            y = int(cy + radius * 0.50 * math.sin(angle))
            pts_sq.append([x, y])
        cv2.polylines(frame, [np.array(pts_sq, np.int32)], True, tuple(int(c * alpha) for c in bright_gold), 2, cv2.LINE_AA)
        
    draw_geometric_symbols(frame, cx, cy, radius * 0.35, -t * 2.0, 6, white_gold, alpha)
    
    pulse = 0.5 + 0.5 * math.sin(t * 8)
    cv2.circle(frame, (cx, cy), int(radius * 0.15), tuple(int(c * alpha * 0.5) for c in gold), -1, cv2.LINE_AA)
    cv2.circle(frame, (cx, cy), int(radius * 0.05 + 5 * pulse), tuple(int(c * alpha) for c in white_gold), -1, cv2.LINE_AA)

class DoctorStrangeProcessor:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')
        
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=2,
            min_hand_detection_confidence=0.6,
            min_hand_presence_confidence=0.6,
            min_tracking_confidence=0.6
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        self.portal_active = False
        self.portal_center = (0, 0)
        self.portal_radius = 0.0
        self.portal_intensity_val = 0.0
        self.drawing_points = []
        self.spark_particles = []
        self.portal_particles = []
        self.start_time = time.time()
        self.last_time = self.start_time

    def process_frame(self, image):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        t = now - self.start_time

        image = cv2.flip(image, 1)
        h, w, _ = image.shape

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        results = self.detector.detect(mp_image)

        dark_bg = np.full((h, w, 3), (5, 3, 1), dtype=np.uint8)
        blend = cv2.addWeighted(image, 0.55, dark_bg, 0.45, 0)

        left_fist_present = False
        right_hand_landmarks = None

        if results.hand_landmarks and results.handedness:
            for idx, hand_landmarks in enumerate(results.hand_landmarks):
                label = results.handedness[idx][0].category_name
                is_left_hand = (label == 'Right')
                is_right_hand = (label == 'Left')

                palm_open = is_palm_open(hand_landmarks)
                fist = is_fist(hand_landmarks)

                cx, cy = get_palm_center(hand_landmarks, w, h)
                palm_size = get_palm_size(hand_landmarks, w, h)

                if is_left_hand:
                    if fist:
                        left_fist_present = True
                    elif palm_open and not self.portal_active and len(self.drawing_points) == 0:
                        draw_magic_circle(blend, cx, cy, palm_size * 1.5, t, 0.8)

                if is_right_hand:
                    right_hand_landmarks = hand_landmarks
                    if palm_open and not self.portal_active and len(self.drawing_points) == 0:
                        draw_magic_circle(blend, cx, cy, palm_size * 1.5, t, 0.8)

        if left_fist_present:
            if not self.portal_active:
                if right_hand_landmarks:
                    index_tip = right_hand_landmarks[8]
                    ix, iy = int(index_tip.x * w), int(index_tip.y * h)
                    self.drawing_points.append((ix, iy))
                    
                    for _ in range(4):
                        self.spark_particles.append(Spark(ix, iy))
                        
                    if len(self.drawing_points) > 100:
                        self.drawing_points.pop(0)
                        
                    is_circle, center, avg_radius = check_circle_gesture(self.drawing_points, min_perimeter=250, close_threshold=50)
                    if is_circle:
                        self.portal_active = True
                        self.portal_center = center
                        self.portal_radius = max(avg_radius, 120) * 1.2
                        self.drawing_points = []
            else:
                self.portal_intensity_val = min(1.0, self.portal_intensity_val + dt * 2.0)
                self.drawing_points = []
        else:
            self.portal_intensity_val = max(0.0, self.portal_intensity_val - dt * 2.0)
            if self.portal_intensity_val <= 0:
                self.portal_active = False
            self.drawing_points = []

        if len(self.drawing_points) > 1:
            for i in range(1, len(self.drawing_points)):
                cv2.line(blend, self.drawing_points[i-1], self.drawing_points[i], (50, 180, 255), 2, cv2.LINE_AA)

        if self.portal_active or self.portal_intensity_val > 0.05:
            draw_magic_circle(blend, int(self.portal_center[0]), int(self.portal_center[1]), self.portal_radius, t, self.portal_intensity_val)
            if random.random() < 0.8 * self.portal_intensity_val:
                for _ in range(2):
                    self.portal_particles.append(Particle(self.portal_center[0], self.portal_center[1], self.portal_radius))
                
        alive_sparks = []
        for p in self.spark_particles:
            if p.update(dt):
                p.draw(blend)
                alive_sparks.append(p)
        self.spark_particles = alive_sparks

        alive_portal = []
        for p in self.portal_particles:
            if p.update(dt):
                p.draw(blend)
                alive_portal.append(p)
        self.portal_particles = alive_portal

        if len(self.spark_particles) > 300:
            self.spark_particles = self.spark_particles[-200:]
        if len(self.portal_particles) > 400:
            self.portal_particles = self.portal_particles[-300:]

        return blend

def main():
    processor = DoctorStrangeProcessor()

    cap = None
    for cam_idx in [0, 1, 2]:
        cap = cv2.VideoCapture(cam_idx)
        if cap.isOpened():
            print(f"[INFO] Successfully opened camera index {cam_idx}")
            break
        cap.release()

    if cap is None or not cap.isOpened():
        print("[ERROR] Cannot open any camera (tried indices 0, 1, 2).")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("╔════════════════════════════════════════════════╗")
    print("║        Doctor Strange Portal Effect *          ║")
    print("╠════════════════════════════════════════════════╣")
    print("║  1. Open Palm -> Magical Hand Runes            ║")
    print("║  2. Left Fist + Right Hand Circles -> PORTAL   ║")
    print("║  Press 'q' / ESC to Quit                       ║")
    print("╚════════════════════════════════════════════════╝")

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        blend = processor.process_frame(image)
        cv2.imshow('Doctor Strange Portal', blend)

        key = cv2.waitKey(1) & 0xFF
        if key == 27 or key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
