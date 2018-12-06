from face import Face
import os
import cv2
import csv
import numpy as np


class Ai(Face):
    DATA_DIR = "./data/"

    def train(self, tel, nickname_list):
        userDir = self.DATA_DIR + tel + "/"
        # peopleDirList = []
        peopleData = {}
        for nickname in nickname_list:
            peopleDir = userDir + nickname + "/"
            # peopleDirList.append(peopleDir)
            print(peopleDir)
            faceData, face128d = self.getFaceData(peopleDir)
            # peopleData[nickname]['key'] = faceData
            peopleData[nickname] = {}
            peopleData[nickname]['eyes'] = self.getEyesThreshold(self.getEyesData(faceData))
            peopleData[nickname]['mouth'] = self.getMouthThreshold(self.getMouthData(faceData))
            peopleData[nickname]['128d'] = self.getFaceMean(face128d)
        # print(peopleData)
        return  self.saveData(userDir,peopleData)

    def deleteData(self, tel):
        userDir = self.DATA_DIR + tel + "/"
        csvPath = userDir + "features_all.csv"
        try:
            if not os.path.exists(csvPath):
                return 1
            else:
                os.remove(csvPath)
                return 0
        except Exception as e:
            print(e)
            return -1

    def getModelData(self, tel):
        userDir = self.DATA_DIR + tel + "/"
        csvPath = userDir + "features_all.csv"
        try:
            if not os.path.exists(csvPath):
                return 1, []
            else:
                csvFile = csv.reader(open(csvPath,"r"))
                csvList = list(csvFile)
                return 0, csvList
        except Exception as e:
            print(e)
            return -1, []

    @staticmethod
    def cv_imread(file_path):
        cv_img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
        return cv_img

    def getFaceData(self, people_dir):
        faceData = []
        face128d = []
        for i in range(4):
            # peopleFace = cv2.imread(people_dir + str(i) + ".jpg")
            peopleFace = self.cv_imread(people_dir + str(i) + ".jpg")
            faceData.append(self.getOneFace(peopleFace))
            face128d.append(self.get128dFeatures(peopleFace))
        return faceData, face128d

    def getEyesData(self, face_data):
        eyesData = []
        for data in face_data:
            peopleEyes = self.getEyes(data)
            eyesData.append(peopleEyes)
        return eyesData

    def getEyesThreshold(self, eyes_data):
        max = (eyes_data[0] + eyes_data[2]) / 2
        min = (eyes_data[1] + eyes_data[3]) / 2
        threshold = (max - min) * 0.5 + min
        return threshold

    def getMouthData(self, face_data):
        mouthData = []
        for data in face_data:
            peopleMouth = self.getMouth(data)
            mouthData.append(peopleMouth)
        return mouthData

    def getMouthThreshold(self, mouth_data):
        min = (mouth_data[0] + mouth_data[1]) / 2
        max = (mouth_data[2] + mouth_data[3]) / 2
        threshold = (max - min) * 0.8 + min
        return threshold

    def getFaceMean(self, face_128d):
        ret = self.computeTheMean(face_128d)
        return ret

    def saveData(self, user_dir, people_data):
        csvPath = user_dir + "features_all.csv"
        try:
            with open(csvPath, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                for key in people_data:
                    featureList = [key, people_data[key]['eyes'], people_data[key]['mouth']]
                    featureList.extend(people_data[key]['128d'].tolist())
                    writer.writerow(featureList)
            return csvPath
        except Exception as e:
            print(e)
            return ""



if __name__ == '__main__':
    ai = Ai()
    ai.train("15692023145",["周航","John"])
