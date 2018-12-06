from imutils import face_utils
import numpy as np
import pandas as pd
import imutils
import dlib
import cv2
import os


SHAPE_5_FACE_FILE = "model/shape_predictor_5_face_landmarks.dat"
SHAPE_68_FACE_FILE = "model/shape_predictor_68_face_landmarks.dat"
DLIB_FACE_MODEL_FILE = "model/dlib_face_recognition_resnet_model_v1.dat"


class Face:
    detector = dlib.get_frontal_face_detector()
    predictor_5 = dlib.shape_predictor(SHAPE_5_FACE_FILE)
    predictor_68 = dlib.shape_predictor(SHAPE_68_FACE_FILE)
    facerec = dlib.face_recognition_model_v1(DLIB_FACE_MODEL_FILE)

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]  # 左眼的点即（37,42）
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]  # 有眼的点即（43,48）

    def __init__(self):
        self.faceFrame = None

    ''' 获取人脸的位置 '''
    def getFaceSite(self, rects, w, h):
        height = 0
        width = 0
        pos_start = (0, 0)
        pos_end = (0, 0)
        if len(rects) != 0:
            for k, d in enumerate(rects):
                if (d.bottom() - d.top()) * (d.right() - d.left()) > height * width \
                        and d.left()-50 >= 0 and d.top()-50 >= 0  and d.right()+50 <= w and d.bottom()+50 <= h :
                    height = d.bottom() - d.top() + 100
                    width = d.right() - d.left() + 100
                    pos_start = tuple([d.left()-50, d.top()-50])
                    pos_end = tuple([d.right()+50, d.bottom()+50])
            return [pos_start, pos_end, height, width]
        else:
            return None

    def checkFace(self, img_data):
        gray = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
        size = gray.shape
        rects = self.detector(gray)
        count = len(rects)
        if rects is not None and count > 0:
            if count == 1:
                ret = self.getFaceSite(rects, size[1], size[0])
                if ret[2]+ret[3] > 0:
                    return 0, ret
                else:
                    return -1, ret
            else:
                return 1, None
        else:
            return -1, None

    def cutFace(self, img_data):
        suc, res = self.checkFace(img_data)
        if suc != 0:
            return suc, res
        else:
            (x, y) = res[0]
            height = res[2]
            width = res[3]
            new_img = cv2.resize(img_data[y:(y+height), x:(x+width)], (128, 128))
            return suc, new_img

    ''' 获取最近的一张脸关键点 '''
    def getOneFace(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        rects = self.detector(gray, 0)  # 获取人脸
        if rects is not None:
            shape = face_utils.shape_to_np(self.predictor_68(gray, rects[0]))  # 获取脸部68个关键点位置
        else:
            shape = None
        return shape

    ''' 计算欧氏距离 '''
    @staticmethod
    def calDistance(vec1, vec2):
        dist = np.sqrt(np.sum(np.square(np.subtract(vec1, vec2))))
        return dist

    @staticmethod
    def byte2Img(img_byte):
        img_data = np.asanyarray(bytearray(img_byte.read()),dtype="uint8")
        img_data = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        return img_data

    @staticmethod
    def saveImg(img_data, file_name):
        # cv2.imwrite(file_name, img_data) # 中文路径不可用
        cv2.imencode(".jpg", img_data)[1].tofile(file_name)

    ''' 计算眼睛张度 '''
    def eyeAspectRatio(self,eyes):
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

    ''' 通过嘴巴关键点坐标返回嘴巴张度 '''
    def getMouth(self, shape):
        mouth = shape[60:68]
        er = self.getMouthRatio(mouth)
        return er

    ''' 返回单张图像的128D特征 '''
    def get128dFeatures(self, img):
        # img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_RGB = img
        dets = self.detector(img_RGB, 1)
        if len(dets) != 0:
            shape = self.predictor_5(img_RGB, dets[0])
            faceDescriptor = self.facerec.compute_face_descriptor(img_RGB, shape)
        else:
            faceDescriptor = 0
        return list(faceDescriptor)

    ''' 计算128维特征均值 '''
    def computeTheMean(self, face_des_list):
        # print(face_des_list)
        feature_mean = np.array(face_des_list)
        return np.mean(feature_mean, axis=0)
