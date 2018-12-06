from imutils import face_utils
from camera import Frame
import numpy as np
import pandas as pd
import imutils
import dlib
import os
import json
import multiprocessing

SHAPE_5_FACE_FILE = "model/shape_predictor_5_face_landmarks.dat"
SHAPE_68_FACE_FILE = "model/shape_predictor_68_face_landmarks.dat"
DLIB_FACE_MODEL_FILE = "model/dlib_face_recognition_resnet_model_v1.dat"

CSV_FILE = "data/features_all.csv"

SHAPE_CACHE_FILE = "cache/shape.tuple"
JSON_CACHE_FILE = "cache/people.json"


class Face:
    detector = dlib.get_frontal_face_detector()
    predictor_5 = dlib.shape_predictor(SHAPE_5_FACE_FILE)
    predictor_68 = dlib.shape_predictor(SHAPE_68_FACE_FILE)
    facerec = dlib.face_recognition_model_v1(DLIB_FACE_MODEL_FILE)

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]  # 左眼的点即（37,42）
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]  # 有眼的点即（43,48）

    def __init__(self):
        self.features_known_arr = []
        self.features_name_arr = []
        self.loadCSV()
        self.faceFrame = None
        self.process = multiprocessing.Process(target=self.pipe)

    ''' 打开进程 '''
    def processStar(self):
        if not self.process.is_alive():
            self.process.start()

    ''' 停止进程 '''
    def processStop(self):
        self.process.terminate()
        self.process.join()

    ''' 管道方法，利用文件缓存传递参数 '''
    def pipe(self):
        people_dict = {}
        while True:
            # print(self.faceFrame)
            # frame = self.readShape()
            frame = Frame.readCache()
            if frame is not None:
                try:
                    people_dict['name'] = self.getPeople(frame)
                    self.savePeople(people_dict)
                except Exception as e:
                    pass
                    # print("pip:",e)

    ''' 计算欧氏距离 '''
    @staticmethod
    def calDistance(vec1, vec2):
        dist = np.sqrt(np.sum(np.square(np.subtract(vec1, vec2))))
        return dist

    ''' 获取人脸的位置 '''
    def getFaceSite(self, gray):
        rects = self.detector(gray, 0)
        height = 0
        width = 0
        pos_start = (0, 0)
        pos_end = (0, 0)
        if len(rects) != 0:
            for k, d in enumerate(rects):
                if (d.bottom() - d.top()) * (d.right() - d.left()) > height * width:
                    height = d.bottom() - d.top() + 100
                    width = d.right() - d.left() + 100
                    pos_start = tuple([d.left()-50, d.top()-50])
                    pos_end = tuple([d.right()+50, d.bottom()+50])
            return pos_start, pos_end, height, width
        else:
            return None

    ''' 获取最近的一张脸 '''
    def getOneFace(self, frame):
        gray = Frame.RGB2Gray(frame)
        rects = self.detector(gray, 0)  # 获取人脸
        if rects is not None:
            shape = self.predictor_68(gray, rects[0])  # 获取脸部68个关键点位置
        else:
            shape = None
        return shape

    ''' 获取眼睛和嘴巴的位置 '''
    def getEyesAndMouthPos(self, frame):
        shape = self.getOneFace(frame)
        if shape is not None:
            shape = face_utils.shape_to_np(shape)  # 转成numpy数组
            leftEye = shape[self.lStart:self.lEnd]  # 获取左眼相关的坐标
            rightEye = shape[self.rStart:self.rEnd]  # 获取右眼相关的坐标
            mouth = shape[49:61]  # 获取嘴巴相关的坐标
            return leftEye, rightEye, mouth
        else:
            return None, None, None

    # ''' 获取最大的人脸——最近的人脸 '''
    # def selectMaxFace(self,gray,rects):
    #     maxDist = 0
    #     maxFace = np.empty((64,2))
    #     for rect in rects:
    #         shape1 = self.predictor_68(gray,rect)     # 转成68个关键点
    #         shape = face_utils.shape_to_np(shape1)    # 转成numpy数组
    #         face_left = shape[0]        # 脸部左上角点
    #         face_reght = shape[16]      # 脸部右上角点
    #         face_buttom = shape[8]      # 脸部最下点
    #         dist = self.calDistance(face_left,face_reght) \
    #                + self.calDistance(face_reght,face_buttom) \
    #                + self.calDistance(face_left,face_buttom)        # 通过这三点的欧氏距离计算最大的脸
    #         if dist > maxDist:
    #             maxDist = dist
    #             maxFace = shape1
    #     if maxDist <= 0:
    #         return None
    #     else:
    #         return maxFace

    ''' 通过frame读取 '''
    def getFaceData(self, frame):
        result = {}
        frame = imutils.resize(frame, width=450)  # 按比例调整图片宽度450
        Frame.saveCache(frame)
        shape = self.getOneFace(frame)
        # gray = Frame.BGR2Gray(frame)                # 图片转灰度
        # rects = self.detector(gray)                 # 监听人脸，返回列表  有多少个人脸返回多少个
        # print(frame)
        # Frame.saveCache(frame)
        # shape = self.selectMaxFace(gray, rects)     # 获得最近的一张人脸
        if shape is not None:  # 判断时候有脸部
            # self.saveShape(shape)
            np_shape = face_utils.shape_to_np(shape)
            result['eyes'] = self.getEyes(np_shape)
            result['mouth'] = self.getMouth(np_shape)
            self.processStar()
        # print(result)
        return result

    ''' 计算眼睛张度 '''
    def eyeAspectRatio(self, eyes):
        w = self.calDistance(eyes[0], eyes[3])
        h1 = self.calDistance(eyes[1], eyes[5])
        h2 = self.calDistance(eyes[2], eyes[4])
        return (h1 + h2) / (2 * w)

    ''' 通过眼睛关键点坐标返回眼睛平均张度 '''
    def getEyes(self, shape):
        leftEye = shape[self.lStart:self.lEnd]  # 提取左眼关键点坐标
        rightEye = shape[self.rStart:self.rEnd]  # 提取右眼关键点坐标
        leftEr = self.eyeAspectRatio(leftEye)
        rightEr = self.eyeAspectRatio(rightEye)
        er = (leftEr + rightEr) / 2
        return er

    ''' 计算嘴巴张度 '''
    def getMouthRatio(self, mouth):
        w = self.calDistance(mouth[0], mouth[4])
        w1 = self.calDistance(mouth[1], mouth[3])
        w2 = self.calDistance(mouth[7], mouth[5])
        h1 = self.calDistance(mouth[1], mouth[7])
        h2 = self.calDistance(mouth[2], mouth[6])
        h3 = self.calDistance(mouth[3], mouth[5])
        return (h1 + h2 + h3 + w1 + w2) / (5 * w)
        # w = self.calDistance(mouth[0], mouth[6])
        # w1 = self.calDistance(mouth[1], mouth[5])
        # w2 = self.calDistance(mouth[2], mouth[4])
        # w3 = self.calDistance(mouth[11], mouth[7])
        # w4 = self.calDistance(mouth[10], mouth[8])
        # h1 = self.calDistance(mouth[11], mouth[1])
        # h2 = self.calDistance(mouth[10], mouth[2])
        # h3 = self.calDistance(mouth[9], mouth[3])
        # h4 = self.calDistance(mouth[8], mouth[4])
        # h5 = self.calDistance(mouth[7], mouth[5])
        # return (h1 + h2 + h3 + h4 + h5 + w1 + w2 + w3 + w4) / (9 * w)

    ''' 通过嘴巴关键点坐标返回嘴巴张度 '''
    def getMouth(self, shape):
        mouth = shape[60:68]
        # mouth = shape[49:61]
        er = self.getMouthRatio(mouth)
        return er

    ''' 读取人脸CSV模型 '''
    def loadCSV(self):
        csv_rd = pd.read_csv(CSV_FILE, header=None)  # 读取CSV模型的数据
        # known faces
        for i in range(csv_rd.shape[0]):
            features_someone_arr = []
            self.features_name_arr.append(str(csv_rd.ix[i, :][0]))
            for j in range(1, len(csv_rd.ix[i, :])):
                features_someone_arr.append(csv_rd.ix[i, :][j])
                # print(features_someone_arr)
            self.features_known_arr.append(features_someone_arr)
        # print("Faces in Database：", len(self.features_known_arr))

    ''' 获取人脸特征最相近的人的姓名 '''
    def getPeople(self, frame):
        shape = self.getOneFace(frame)
        featuresCap = self.facerec.compute_face_descriptor(frame, shape)
        peopleName = "unknown"
        for i in range(len(self.features_known_arr)):
            compare = self.calDistance(featuresCap, np.array(self.features_known_arr[i]))
            if compare < 0.4:
                peopleName = self.features_name_arr[i]

        # print(peopleName)
        return peopleName

    # ''' 把shape保存到缓存文件 '''
    # @staticmethod
    # def saveShape(shape):
    #     with open(SHAPE_CACHE_FILE,"w+") as f:
    #         f.write()
    #
    # ''' 读取缓存文件，并转换为元祖 '''
    # @staticmethod
    # def readShape():
    #     if os.path.exists(SHAPE_CACHE_FILE):
    #         with open(SHAPE_CACHE_FILE,"r+") as f:
    #             shape = tuple(f.read())
    #         return shape
    #     return None

    @staticmethod
    def savePeople(dict_data):
        json_str = json.dumps(dict_data)
        with open(JSON_CACHE_FILE,"w+") as f:
            f.write(json_str)

    @staticmethod
    def readPeople():
        if os.path.exists(JSON_CACHE_FILE):
            with open(JSON_CACHE_FILE, "r+") as f:
                json_str = f.read()
            dict_data = json.loads(json_str)
        else:
            dict_data = None
        return dict_data

    def __del__(self):
        try:
            self.processStop()
            del self.process
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    import cv2

    cameraCapture = cv2.VideoCapture(0)
    f = Face()
    while cameraCapture.isOpened():
        success, frame = cameraCapture.read()
        cv2.imshow("Frame", frame)
        global frame1
        frame1 = frame
        f.getFace(frame)
        # f.getEyes(frame)
        # f.getMouth(frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
