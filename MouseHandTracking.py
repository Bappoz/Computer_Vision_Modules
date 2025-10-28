import cv2
import time
import HandTrackingModule as htm
import pyautogui

pTime = 0
cTime = 0

tipIds = [4, 8, 12, 16, 20]

state = None

wCam = 1280
hCam = 720


detector = htm.HandDetector()
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
        landmarks_list = detector.findPosition(frame, draw=False)
        if len(landmarks_list) != 0:
            fingers = []
            for id in range(1, 5):
                if landmarks_list[id][2] < landmarks_list[id - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            print(totalFingers)

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