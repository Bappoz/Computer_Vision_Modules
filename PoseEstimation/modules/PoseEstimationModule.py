import cv2 
import mediapipe as mp
import time


class PoseDetector(object):

    def __init__(self,
                mode=False,
                smooth=True,
                detectionCon=0.5,
                trackingCon=0.5):
        
        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpDraw= mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,
                                     smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon, 
                                     min_tracking_confidence=self.trackingCon)
        
    def findPose(self, img, draw=True):
        """
        Find postion of mediapipe computer vision machine and draw it on video
        """
        
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        
        if self.results.pose_landmarks:
            if  draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, 
                                            self.mpPose.POSE_CONNECTIONS)  




        return img

    def get_position(self, img, draw=True):
        lmList = []

        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id, cx, cy])
        
        return lmList




def main():
    cap = cv2.VideoCapture('../videos_ex/guy_dancing.mp4')

    output_width = 640
    output_height = 360
    pTime = 0

    detector = PoseDetector()

    while True:

        sucess, img = cap.read()
        if not sucess:
            break
        
        img_resized = cv2.resize(img, (output_width, output_height))
        
        img = detector.findPose(img_resized)
        lmList = detector.get_position(img)
        if len(lmList) != 0:
            print(lmList)
        
        # Check FPS
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 3)

        cv2.imshow("image", img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Erro: {e}")