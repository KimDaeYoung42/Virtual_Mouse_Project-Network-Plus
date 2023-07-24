import cv2
import mediapipe as mp
import math

# 손 인식 및 검출파트 (클래스화)
class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.8, tracking_confidence=0.8):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, self.detection_confidence, self.tracking_confidence)
        self.mp_draw = mp.solutions.drawing_utils
        self.tip_ids = [4, 8, 12, 16, 20]   # 손가락 landmark 번호

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return img

    # 손의 랜드마크 리턴 하는 부분 여기서 양 손의 랜드마크를 따로 따로 리턴 해줘야 함.
    def find_positions(self, img, draw=True):
        self.left_lm_list = []
        self.right_lm_list = []

        # x_list = []
        # y_list = []
        # bbox = []
        # self.lm_list = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks
            h, w, c = img.shape
            for _, lm in enumerate(hand):
                for idx in range(0, 21):
                    cx, cy, cz = int(lm.landmark[idx].x * w), int(lm.landmark[idx].y * h), int(lm.landmark[idx].z * c)
                    handedness = self.results.multi_handedness
                    for hand in handedness:
                        if hand.classification[0].label == "Left":
                            self.left_lm_list.append([idx, cx, cy, cz])
                        elif hand.classification[0].label == "Right":
                            self.right_lm_list.append([idx, cx, cy, cz])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                    # print(self.left_lm_list, self.right_lm_list)

        return self.left_lm_list, self.right_lm_list

        # if self.results.multi_hand_landmarks:
        #     my_hand = self.results.multi_hand_landmarks[hand_number]
        #     for id, lm in enumerate(my_hand.landmark):
        #         # print(id, lm)
        #         h, w, c = img.shape
        #         cx, cy = int(lm.x * w), int(lm.y * h)
        #         x_list.append(cx)
        #         y_list.append(cy)
        #         # print(id, cx, cy)
        #         self.lm_list.append([id, cx, cy])
        #         if draw:
        #             cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        #
        #     x_min, x_max = min(x_list), max(x_list)
        #     y_min, y_max = min(y_list), max(y_list)
        #     bbox = x_min, y_min, x_max, y_max
        #
        #     if draw:
        #         cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20), (bbox[2] + 20, bbox[3] + 20), (0, 255, 0), 2)

        # return self.lm_list, bbox



    # 구) 손가락 확인 (초기 핸드트래킹 사용 모듈)
    def fingers_up(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)
        return fingers

    # 구) 손가락 확인 (초기 핸드트래킹 사용 모듈)
    def find_Distance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        return length, img, [x1, y1, x2, y2, cx, cy]
