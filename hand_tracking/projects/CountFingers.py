import cv2
import time
import sys
import os

# Adiciona o diretório pai ao sys.path para encontrar o módulo hand_tracking
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from hand_tracking.modules.HandTrackingModule import HandDetector
import pyautogui

pTime = 0
cTime = 0

tipIds = [4, 8, 12, 16, 20]
totalFingers = 0

wCam = 640
hCam = 360


detector = HandDetector()
capture = detector.open_camera(wCam=wCam, hCam=hCam)
if capture is None:
    print("Erro: não foi possivel conectar a camera")
    raise SystemError(1)

try:
    while True:
        ret, frame = capture.read()
        frame = cv2.flip(frame,1)
        if not ret or frame is None:
            print("Erro: Nenhum retorno da câmera")
            break

        totalFingersRight = 0
        totalFingersLeft = 0

        frame = detector.findHands(frame)
        if detector.results.multi_hand_landmarks:
            for i in range(len(detector.results.multi_hand_landmarks)):

                landmarks_list, handType, bbox = detector.findPosition(frame, handNo=i, draw=False)
                if len(landmarks_list) != 0:

                    current_hand_fingers = []

                    if handType == "Right":        
                        if landmarks_list[tipIds[0]][1] < landmarks_list[tipIds[0] - 1][1]:
                            current_hand_fingers.append(1)
                        else:
                            current_hand_fingers.append(0)

                        for id_left in range(1, 5):
                            tip_id = tipIds[id_left]
                            if landmarks_list[tip_id][2] < landmarks_list[tip_id - 2][2]:
                                current_hand_fingers.append(1)
                            else:
                                current_hand_fingers.append(0)
                        totalFingersRight = current_hand_fingers.count(1)

                    if handType == "Left":
                        if landmarks_list[tipIds[0]][1] > landmarks_list[tipIds[0] - 1][1]:
                            current_hand_fingers.append(1)
                        else:
                            current_hand_fingers.append(0)
                                            
                        for id_right in range(1, 5):
                            tip_id = tipIds[id_right]
                            if landmarks_list[tip_id][2] < landmarks_list[tip_id - 2][2]:
                                current_hand_fingers.append(1)
                            else:
                                current_hand_fingers.append(0)
                        totalFingersLeft = current_hand_fingers.count(1)

        totalFingers = totalFingersRight + totalFingersLeft
        cv2.putText(frame, f'Finger Left: {totalFingersLeft}', (10, 340), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 1)
        cv2.putText(frame, f'Finger Right: {totalFingersRight}', (10, 320), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 1)
        cv2.putText(frame, f'Finger Sum: {totalFingers}', (430, 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)



        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0), 2)
        cv2.imshow("frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        
finally:

    cv2.destroyAllWindows()
    capture.release()