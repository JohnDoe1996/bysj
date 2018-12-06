import cv2
import os


class Frame:
    @staticmethod
    def BGR2RGB(frame):
        newFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 颜色由BGR转为RGB
        return newFrame

    @staticmethod
    def BGR2Gray(frame):
        newFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 颜色由BGR转为灰度
        return newFrame

    @staticmethod
    def RGB2Gray(frame):
        newFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)  # 颜色由RGB转为灰度
        return newFrame

    @staticmethod
    def cuter(frame, x, y, width, height, size_x, size_y):  # 图片裁剪
        newFrame = cv2.resize(
            frame[y:(y + height), x:(x + width)],
            (size_x, size_y)
        )
        return newFrame

    @staticmethod
    def line(frame, pos_list, color_tuple ):    # 连线
        posHull = cv2.convexHull(pos_list)
        cv2.drawContours(frame, [posHull], -1, color_tuple, 1)
        return frame

    @staticmethod
    def readCache():    # 读取缓存文件
        newFrame = cv2.imread("cache/frame.jpg")
        return newFrame

    @staticmethod
    def saveCache(frame):   # 写入缓存文件
        cv2.imwrite("cache/frame.jpg", frame)

    @staticmethod
    def flipHorizintal(frame):
        newFrame = cv2.flip(frame, 1)
        return newFrame

    @staticmethod
    def flipVertical(frame):
        newFrame = cv2.flip(frame, 0)
        return newFrame


class Camera(Frame):
    frame = None

    def __init__(self):
        self.delCacheFile()
        self.cap = cv2.VideoCapture(0)  # 创建摄像头句柄

    @staticmethod
    def delCacheFile():
        if os.path.exists("cache/frame.jpg"):
            os.remove("cache/frame.jpg")
        if os.path.exists("cache/people.json"):
            os.remove("cache/people.json")

    def getFrame(self):
        success, frame = self.cap.read()  # 读取当前帧
        self.frame = frame
        return frame

    def flipHorizintal(self):
        self.frame = super().flipHorizintal(self.frame)
        return self.frame

    def flipVertical(self):
        self.frame = super().flipVertical(self.frame)
        return self.frame

    def getRGBFrame(self):
        RGBFrame = self.BGR2RGB(self.frame)
        return RGBFrame

    def getGrayFrame(self):
        GrayFrame = self.BGR2Gray(self.frame)
        return GrayFrame

    def getFaceFrame(self, x, y, width, height):
        Frame_128x128 = self.cuter(self.getRGBFrame(), x, y, width, height, 128, 128)
        return Frame_128x128

    def getFaceFrameAndLine(self, x, y, width, height,
                            left_eye_pos, right_eye_pos, mouth_pos):
        lineFrame = self.getFaceFrame(x, y, width, height)
        self.line(lineFrame, left_eye_pos, (0, 255, 0))
        self.line(lineFrame, right_eye_pos,(0, 255, 0))
        self.line(lineFrame,mouth_pos,(0, 0, 255))
        return lineFrame

    def __del__(self):
        self.delCacheFile()
        self.cap.release()
