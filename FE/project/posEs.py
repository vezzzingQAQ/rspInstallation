import cv2
import mediapipe as mp
import time

class PoseEstimator:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()

        self.pTime = 0

    def start(self):
        while(self.cap.isOpened()):
            success, img = self.cap.read()  # 读取给他们两个

            # 转换颜色【因为mediapipe需要RGB】
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 把图片发送给模型
            results = self.pose.process(imgRGB)

            # 获取结果
            # print(results.pose_landmarks)

            # 显示结果【点】
            if results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, results.pose_landmarks,
                                    self.mpPose.POSE_CONNECTIONS)
                # 提取想要的结果
                left_shoulder_x = 0
                left_shoulder_y = 0
                right_shoulder_x = 0
                right_shoulder_y = 0
                left_hip_x = 0
                left_hip_y = 0
                right_hip_x = 0
                right_hip_y = 0

                left_shoulder_value = False
                right_shoulder_value = False
                left_hip_value = False
                right_hip_value = False

                for id, lm in enumerate(results.pose_landmarks.landmark):
                    # 左肩
                    if id == 12:
                        # print(lm)
                        left_shoulder_x = lm.x
                        left_shoulder_y = lm.y
                        left_shoulder_value = True
                    # 右肩
                    if id == 11:
                        right_shoulder_x = lm.x
                        right_shoulder_y = lm.y
                        right_shoulder_value = True
                    # 左臀
                    if id == 24:
                        left_hip_x = lm.x
                        left_hip_y = lm.y
                        left_hip_value = True
                    # 右臀
                    if id == 23:
                        right_hip_x = lm.x
                        right_hip_y = lm.y
                        right_hip_value = True

                c_height = (left_shoulder_y+right_shoulder_y) / \
                    2-(left_hip_y+right_hip_y)/2
                print(c_height)
            # 显示帧率
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)), (70, 50),
                        cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

            cv2.imshow("img", img)
            if cv2.waitKey(1) == ord("q"):  # 按q键退出
                break

        self.cap.release()  # 释放摄像头的资源
        cv2.destroyAllWindows()

es=PoseEstimator()
es.start()