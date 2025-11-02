import cv2
import mediapipe as mp
import time 
import math



class HandDetector():
    def __init__(self, mode=False, numHands=2, detectionCon = 0.5, trackingCon=0.5):
        self.mode=mode
        self.numHands=numHands
        self.detectionCon=detectionCon
        self.trackingCon=trackingCon

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(static_image_mode=self.mode, 
                                         max_num_hands=self.numHands, 
                                         min_detection_confidence=self.detectionCon, 
                                         min_tracking_confidence=self.trackingCon)

        self.tipIds = [4, 8, 12, 16, 20]


    def open_camera(self, indices=(1,0,2), wCam=1280, hCam=720):
        self.wCam = wCam
        self.hCam = hCam

        for i in indices:
            cap = cv2.VideoCapture(i, cv2.CAP_MSMF)
            cap.set(3, self.wCam)
            cap.set(4, self.hCam)
            if cap.isOpened():
                return cap
            cap.release()
        return None

    def findHands(self, frame, draw=True):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        self.results = self.hands.process(rgb)

        rgb.flags.writeable = True
        rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if self.results.multi_hand_landmarks != None:
            for self.handLandmarks in self.results.multi_hand_landmarks:
                if draw: 
                    self.mp_drawing.draw_landmarks(frame, self.handLandmarks, self.mp_hands.HAND_CONNECTIONS)

        return frame
        


    def findPosition(self, frame, handNo=0, draw=True, drawIds=None):
        self.lm_list = []
        xList = []
        yList = []
        bbox = []
        handType = None

        if self.results.multi_hand_landmarks is None or handNo >= len(self.results.multi_hand_landmarks):
            return [], None, []
        
        myHand = self.results.multi_hand_landmarks[handNo]

        try:
            hand_label = self.results.multi_handedness[handNo].classification[0].label
            handType = "Right" if hand_label == "Right" else "Left"

        except: 
            handType = "Left"

        for id, lm in enumerate(myHand.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            
            xList.append(cx)
            yList.append(cy)

            self.lm_list.append([id, cx, cy])
            if draw:
                if drawIds is None:
                    cv2.circle(frame, (cx,cy), 8, (255, 0, 255), cv2.FILLED)
                else:
                    ids = drawIds if isinstance(drawIds, (list, tuple)) else [drawIds]
                    if id in ids:
                        cv2.circle(frame, (cx,cy), 8, (255, 0, 255), cv2.FILLED)

        xmin, xmax = min(xList), max(xList)
        ymin, ymax = min(yList), max(yList)
        bbox = xmin, ymin, xmin, ymax

        if draw:
                cv2.rectangle(
                    frame, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2
                )

        return self.lm_list, handType, bbox
        

    def fingersUp(self, frame):
        fingers = []
        detector = HandDetector()
        fingersLeftHand = 0
        fingersRightHand = 0

        hands = detector.findHands(frame)

        try:
            if detector.results.multi_hand_landmarks:
                for i in range(len(detector.results.multi_hand_landmarks)):        
                    landmarks_list, handType, bbox = detector.findPosition(frame, handNo=i, draw=False)                    
                    if len(landmarks_list) != 0:
                        current_hand_fingers = []

                        if handType == "Right":
                    
                            #polegar
                            if self.lm_list[self.tipIds[0]][1] < self.lm_list[self.tipIds[0]-1][1]:
                                current_hand_fingers.append(1)
                            else:
                                current_hand_fingers.append(0)

                            #dedos
                            for id in range(1,5):
                                if self.lm_list[self.tipIds[id]][2] > self.lm_list[self.tipIds[id]- 2][2]:
                                    current_hand_fingers.append(1)
                                else:
                                    current_hand_fingers.append(0)

                        if handType == "Left":
                    
                            #polegar
                            if self.lm_list[self.tipIds[0]][1] > self.lm_list[self.tipIds[0]-1][1]:
                                current_hand_fingers.append(1)
                            else:
                                current_hand_fingers.append(0)

                            #dedos
                            for id in range(1,5):
                                if self.lm_list[self.tipIds[id]][2] > self.lm_list[self.tipIds[id]- 2][2]:
                                    current_hand_fingers.append(1)
                                else:
                                    current_hand_fingers.append(0)

            print(current_hand_fingers)
        except:
            pass

        return fingers

    def findDistance(self, p1, p2, frame, draw=True, r=15, t=3):
        x1, y1 = self.lm_list[p1][1:]
        x2, y2 = self.lm_list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(frame, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), r, (0, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)


        return length, frame, [x1, y1, x2, y2, cx, cy]
    

def main():
    pTime = 0
    cTime = 0

    wCam = 1280
    hCam = 720

    detector = HandDetector()
    capture = detector.open_camera(wCam=wCam, hCam=hCam)
    if capture is None:
        print("Erro: não foi possivel conectar a camera")
        raise SystemError(1)
    
    try:
        while True:
            ret, frame = capture.read()
            if not ret or frame is None:
                print("Erro: Nenhum retorno da câmera")
                break

            frame = detector.findHands(frame)
            landmarks_list, handType, bbox, = detector.findPosition(frame)
            fingers_up = detector.fingersUp(frame)
            #if len(landmarks_list) != 0:
            #    print(landmarks_list[8])

            print(fingers_up)

            cTime = time.time()
            fps = 1/(cTime - pTime)
            pTime = cTime

            cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 2)
            cv2.imshow("frame", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            
    finally:

        cv2.destroyAllWindows()
        capture.release()



if __name__ == "__main__":
    main()