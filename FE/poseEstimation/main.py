import cv2
import mediapipe as mp
import time
import math
import json

from handshake import *
from ipport import *

# 连接服务器
# token = ""
# HSK =HandShake(cmObj.send_to_ip, cmObj.send_to_port,cmObj.local_ip, cmObj.local_port)
# HSK.send_message({
#     "command": "conn",
#     "id": cmObj.client_id,
#     "server": cmObj.server_id,
#     "timestamp": time.time()
# })
# token=HSK.back_data["token"]

cap = cv2.VideoCapture(0)

mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()

pTime = 0
itea = 0
while(cap.isOpened()):
    itea += 1
    success, img = cap.read()  # 读取给他们两个

    # 转换颜色【因为mediapipe需要RGB】
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 把图片发送给模型
    results = pose.process(imgRGB)

    # 获取结果
    # print(results.pose_landmarks)

    # 显示结果【点】
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks,
                              mpPose.POSE_CONNECTIONS)
        dataList = [
            {"name": "left_mouth", "id": 10, "x": 0, "y": 0},
            {"name": "right_mouth", "id": 9, "x": 0, "y": 0},
            {"name": "left_shoulder", "id": 12, "x": 0, "y": 0},
            {"name": "right_shoulder", "id": 11, "x": 0, "y": 0},
            {"name": "left_hip", "id": 24, "x": 0, "y": 0},
            {"name": "right_hip", "id": 23, "x": 0, "y": 0},
        ]
        # 提取想要的结果
        for id, lm in enumerate(results.pose_landmarks.landmark):
            for data in dataList:
                if data["id"] == id:
                    data["x"] = lm.x
                    data["y"] = lm.y
        # print(dataList)   # 打印结果
        mouth_x = (dataList[0]["x"]+dataList[1]["x"])/2
        mouth_y = (dataList[0]["y"]+dataList[1]["y"])/2
        shoulder_x = (dataList[2]["x"]+dataList[3]["x"])/2
        shoulder_y = (dataList[2]["y"]+dataList[3]["y"])/2
        head_angle = math.atan2(mouth_y-shoulder_y, mouth_x-shoulder_x)

        print(head_angle)
        print(results.pose_landmarks.landmark)

    # 显示帧率
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    cv2.imshow("img", img)
    if cv2.waitKey(1) == ord("q"):  # 按q键退出
        break

    if itea % 10 == 0:
        with open("../temp.json", "w")as fobj:
            json.dump({"angle":180+head_angle*180/3.14}, fobj)

cap.release()  # 释放摄像头的资源
cv2.destroyAllWindows()
