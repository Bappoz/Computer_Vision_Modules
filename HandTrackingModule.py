import cv2
import mediapipe as mp
import time 



class HandDetector():
    def __init__(self, mode=False, numHands=2, detectionCon = 0.7, trackingCon=0.7):
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
        lm_list = []
        handType = None

        if handNo >= len(self.results.multi_hand_landmarks):
            return [], None
        
        myHand = self.results.multi_hand_landmarks[handNo]

        try:
            hand_label = self.results.multi_handedness[handNo].classification[0].label
            handType = "Right" if hand_label == "Right" else "Left"

        except: 
            handType = "Left"

        for id, lm in enumerate(myHand.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            #print(id, cx, cy)
            lm_list.append([id, cx, cy])
            if draw:
                if drawIds is None:
                    cv2.circle(frame, (cx,cy), 8, (255, 0, 255), cv2.FILLED)
                else:
                    ids = drawIds if isinstance(drawIds, (list, tuple)) else [drawIds]
                    if id in ids:
                        cv2.circle(frame, (cx,cy), 8, (255, 0, 255), cv2.FILLED)

        return lm_list, handType
        


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
            landmarks_list = detector.findPosition(frame)
            if len(landmarks_list) != 0:
                print(landmarks_list[4])

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