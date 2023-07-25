import cv2
import mediapipe as mp
import math
import numpy as np
from tensorflow.keras.models import load_model


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
        self.tip_ids = [4, 8, 12, 16, 20]  # 손가락 landmark 번호

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
    def find_positions(self, img):
        self.lm_list = []
        self.label = '?'

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks
            h, w, c = img.shape
            for _, lm in enumerate(hand):
                for idx in range(0, 21):
                    cx, cy, cz = int(lm.landmark[idx].x * w), int(lm.landmark[idx].y * h), int(lm.landmark[idx].z * c)
                    self.lm_list.append([idx, cx, cy, cz])
                    handedness = self.results.multi_handedness
                    for hand in handedness:
                        if hand.classification[0].label == "Left":
                            self.label = 'left'
                        elif hand.classification[0].label == "Right":
                            self.label = 'right'

        return self.lm_list, self.label

    # 손을 보고 어떤 제스쳐인지 추측하는 파트 ( LSTM 방식의 학습 모델을 활용)
    def action_estimation(self, img):

        self.this_action = 'aaaa'
        actions = ['none', 'move', 'click', 'ok']
        seq_length = 30

        model = load_model('models/model.h5')

        seq = []
        action_seq = []

        if self.results.multi_hand_landmarks:
            for res in self.results.multi_hand_landmarks:
                joint = np.zeros((21, 4))
                for j, lm in enumerate(res.landmark):
                    joint[j] = [lm.x, lm.y, lm.z, lm.visibility]

                # Compute angles between joints
                v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :3]  # Parent joint
                v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :3]  # Child joint
                v = v2 - v1  # [20, 3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                # Get angle using arcos of dot product
                angle = np.arccos(np.einsum('nt,nt->n',
                                            v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                                            v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]

                angle = np.degrees(angle)  # Convert radian to degree

                d = np.concatenate([joint.flatten(), angle])

                seq.append(d)

                print(len(seq))  # seq의 길이가 안늘어난다.....!!   배열의 크기가 늘어나는게 아닌 배열의 값만 바뀜.
                # 여기를 못지나감. 즉 len(seq) > seq_length
                if len(seq) < seq_length:
                    continue

                input_data = np.expand_dims(np.array(seq[-seq_length:], dtype=np.float32), axis=0)

                y_pred = model.predict(input_data).squeeze()

                i_pred = int(np.argmax(y_pred))
                conf = y_pred[i_pred]

                if conf < 0.9:
                    continue

                action = actions[i_pred]
                action_seq.append(action)

                if len(action_seq) < 3:
                    continue

                # action이 3개 연속일 때
                if action_seq[-1] == action_seq[-2] == action_seq[-3]:
                    self.this_action = action

                cv2.putText(img, f'{self.this_action.upper()}',
                            org=(int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0] + 20)),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

        return self.this_action

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