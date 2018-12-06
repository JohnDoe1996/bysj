import os
import sys
from PySide2.QtCore import QTimer
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow

from camera import Camera
from face import Face
# from PyQt5.QtWidgets import QApplication, QMainWindow
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtCore import QTimer
from gui import Ui_MainWindow


class MyMainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.face = Face()
        self.single()
        self.camera = Camera()
        self.setTimer()

    def single(self):
        self.actionExit.triggered.connect(self.closeWindows)

    def setName(self):
        peopleData = self.face.readPeople()
        if peopleData is not None:
            self.labelName.setText(peopleData['name'])

    def setTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.showCamera)
        self.timer.start()           # 实时刷新
        self.timer.setInterval(100)  # 刷新间隔

    def showCamera(self):
        self.camera.getFrame()
        if self.actionFlipH.isChecked():
            self.camera.flipHorizintal()
        if self.actionFlipV.isChecked():
            self.camera.flipVertical()
        show = self.camera.getRGBFrame()
        showFrame = QImage(show.data, show.shape[1], show.shape[0],QImage.Format_RGB888)
        self.labelFrame.setPixmap(QPixmap.fromImage(showFrame))
        gray = self.camera.getGrayFrame()
        ret = self.face.getFaceSite(gray)
        if ret is not None:
            pos_start, pos_end, height, width = ret
            (x, y) = pos_start
            try:
                faceFrame = self.camera.getFaceFrame(x, y, width, height)
                data = self.face.getFaceData(faceFrame)
                self.setEyesAndMouth(data['eyes'], data['mouth'])
                if self.actionLine.isChecked():
                    leftEye, rightEye, mouth = self.face.getEyesAndMouthPos(faceFrame)
                    faceFrame = self.camera.getFaceFrameAndLine(x, y, width, height, leftEye, rightEye, mouth)
                showFrame = QImage(faceFrame.data, faceFrame.shape[1], faceFrame.shape[0],QImage.Format_RGB888)
                self.labelFace.setPixmap(QPixmap.fromImage(showFrame))
                self.setName()
            except Exception as e:
                pass
                # print("ui:", e)
        else:
            self.labelFace.clear()
            self.labelName.setText("unknown")
            self.labelEyes.setText("0")
            self.labelMouth.setText("0")

    def setEyesAndMouth(self, dataEyes, dataMouth):
        self.labelEyes.setText("%.12f" % dataEyes)
        self.labelMouth.setText("%.12f" % dataMouth)

    def closeWindows(self):
        try:
            del self.face
            del self.camera
            self.close()
            os._exit(0)
        except Exception as e:
            print(e)

    # def closeEvent(self, *args, **kwargs):
    #     super().closeEvent(args,kwargs)
    #     self.closeWindows()

    def close(self, *args, **kwargs):
        super().close(args, kwargs)
        self.closeWindows()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())