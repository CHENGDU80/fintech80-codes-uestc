import sys
from PyQt5 import QtWidgets, QtGui, uic, QtCore, QtWebEngineWidgets
import img_rc
import qt_models
from config import *


class SignInWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('signin.ui', self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 无边框

        # 鼠标拖动窗口移动
        self.m_flag = False
        self.m_Position = None
        self.setMouseTracking(True)

        # 设置stackedWidget默认显示第一个界面（登录界面）
        self.stackedWidget.setCurrentIndex(0)

        # 设置关闭按钮的点击事件
        self.closeButton.clicked.connect(self.close)

        # 登录/注册按钮关闭当前窗口
        self.signinButton.clicked.connect(self.close)
        self.signupButton.clicked.connect(self.close)

        # 设置登录/注册页面切换按钮的点击事件
        self.goSigninButton.clicked.connect(self.goSigninPage)
        self.goSignupButton.clicked.connect(self.goSignupPage)

    # 鼠标拖动窗口移动
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    # 登录/注册页面切换
    def goSigninPage(self):
        self.stackedWidget.setCurrentIndex(0)

    def goSignupPage(self):
        self.stackedWidget.setCurrentIndex(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    signInWindow = SignInWindow()
    # mainWindow = MainWindow()

    signInWindow.show()
    # mainWindow.show()

    # 登录/注册按钮打开主窗口
    # signInWindow.signinButton.clicked.connect(mainWindow.show)
    # signInWindow.signupButton.clicked.connect(mainWindow.show)

    sys.exit(app.exec_())