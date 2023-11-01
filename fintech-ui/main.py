import sys
from PyQt5 import QtWidgets, QtGui, uic, QtCore, QtWebEngineWidgets
import img_rc
from config import *
import Ui_main
import Ui_signin


# class SignInWindow(QtWidgets.QMainWindow):
class SignInWindow(QtWidgets.QMainWindow, Ui_signin.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        # uic.loadUi('signin.ui', self)
        self.setupUi(self)
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


# class MainWindow(QtWidgets.QMainWindow):
class MainWindow(QtWidgets.QMainWindow, Ui_main.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        # uic.loadUi('main.ui', self)
        self.setupUi(self)

        # 各个组件的基本设置
        self.setMainWindow()
        self.setStackedWidget()
        self.setPage1()
        self.setPage2()
        self.setPage3()

    # 设置主窗口
    def setMainWindow(self):
        def search_clicked():
            self.listNavi.setCurrentRow(-1)
            self.listNavi_2.setCurrentRow(0)
            self.stackedWidget.setCurrentIndex(2)
        # 设置窗口背景透明和无边框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # 居中显示(不算任务栏)
        screen = QtWidgets.QApplication.desktop().screenGeometry()
        screen.setHeight(screen.height() - 50)
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                  (screen.height() - size.height()) // 2)
        # 鼠标拖动窗口移动
        self.m_flag = False
        self.m_Position = None
        self.setMouseTracking(True)
        # 设置关闭按钮的点击事件
        self.closeButton.clicked.connect(self.close)
        # 设置搜索框的图标
        self.searchEdit.addAction(QtGui.QIcon(':/img/search.svg'),
                                  QtWidgets.QLineEdit.LeadingPosition)
        # 绑定搜索框图标的回车事件
        self.searchEdit.returnPressed.connect(search_clicked)


    # 设置堆栈窗口
    def setStackedWidget(self):
        # 设置默认选择listNavi中的第一个item
        self.listNavi.setCurrentRow(0)
        # 清除listNavi_2的默认选择
        self.listNavi_2.setCurrentRow(-1)
        # 设置默认显示第一个界面（主页）
        self.stackedWidget.setCurrentIndex(0)
        # 设置titleLabel的文本
        self.titleLabel.setText(self.listNavi.item(0).text())
        # 绑定listNavi和stackedWidget
        self.listNavi.currentRowChanged.connect(
            self.stackedWidget.setCurrentIndex)
        # 设置titleLabel与listNavi和listNavi_2的item同步
        self.listNavi.itemClicked.connect(
            lambda item: self.titleLabel.setText(item.text()))
        self.listNavi_2.itemClicked.connect(
            lambda item: self.titleLabel.setText(item.text()))
        # 点击listNavi_2,跳转到第2页
        self.listNavi_2.itemClicked.connect(
            lambda item: self.stackedWidget.setCurrentIndex(2))
        # 当listNavi和listNavi_2中有一个被点击时，另一个重置
        self.listNavi.itemClicked.connect(
            lambda item: self.listNavi_2.setCurrentRow(-1))
        self.listNavi_2.itemClicked.connect(
            lambda item: self.listNavi.setCurrentRow(-1))

    def setPage1(self):
        # 加载html
        self.worldCloudWeb.load(QtCore.QUrl.fromLocalFile(HTML_PATH + 'wordCloud.html'))
        self.historicalLineChart.load(QtCore.QUrl.fromLocalFile(HTML_PATH + 'historicalLineChart.html'))


    def setPage2(self):
        # 加载html
        self.newsTrendingWeb.load(QtCore.QUrl.fromLocalFile(HTML_PATH + 'newsTrendingLineChart.html'))
        bbcHeadLines = [
            'World Bank warns oil prices could reach $150 a barrel',
            'New licences granted for North Sea oil and gas projects',
            'Government borrows less than expected in September'
        ]
        cnnHeadLines = [
            'Realtors found liable for $1.8 billion in damages in conspiracy to keep commissions high',
            "Europe's economy risks a recession after output falls in the third quarter",
            "Canada bans China's Wechat from government devices citing security risks"
        ]
        alphaHeadLines = [
            "Natural gas surges to cap 22% October gain, most in more than a year",
            "S&P 500 notches three-month losing streak for first time since Q1 2020",
            "SpaceX Starship rocket closer to second launch after FAA completes safety review"
        ]

        def mediaButton_1_clicked():
            self.mediaButton_2.setChecked(False)
            self.mediaButton_3.setChecked(False)
            self.labelHeadLine_1.setText(bbcHeadLines[0])
            self.labelHeadLine_2.setText(bbcHeadLines[1])
            self.labelHeadLine_3.setText(bbcHeadLines[2])
        def mediaButton_2_clicked():
            self.mediaButton_1.setChecked(False)
            self.mediaButton_3.setChecked(False)
            self.labelHeadLine_1.setText(cnnHeadLines[0])
            self.labelHeadLine_2.setText(cnnHeadLines[1])
            self.labelHeadLine_3.setText(cnnHeadLines[2])
        def mediaButton_3_clicked():
            self.mediaButton_1.setChecked(False)
            self.mediaButton_2.setChecked(False)
            self.labelHeadLine_1.setText(alphaHeadLines[0])
            self.labelHeadLine_2.setText(alphaHeadLines[1])
            self.labelHeadLine_3.setText(alphaHeadLines[2])

        # 绑定不同媒体的点击事件
        mediaButton_1_clicked()
        self.mediaButton_1.clicked.connect(mediaButton_1_clicked)
        self.mediaButton_2.clicked.connect(mediaButton_2_clicked)
        self.mediaButton_3.clicked.connect(mediaButton_3_clicked)

        def event_clicked():
            events = {
                'title1': "Israel Palestine Conflict",
                'title2': "The Russia-Ukraine conflict continues to escalate",
                'title3': "China hosts the Belt and Road Forum",
                'summary1':'      Israels military has confirmed that its jets carried out an attack in the Jabalia area of northern Gaza on TuesdayThe IDF says the strike killed a senior Hamas commander and caused the collapse of Hamas s underground infrastructure.',
                'summary2':'      The Russo-Ukrainian War has escalated, resulting in intense clashes in Ukraines conflict zones. The international communitystrongly condemns Russias invasion. Ukraine seeks support, while Russia maintains the legitimacy of its actions.',
                'summary3':"      Xi Jinping met Putin at the Belt and Road Summit. Xi expressed a willingness to collaborate with Russia to uphold international fairness and justice. Putin noted shared external threats, strengthening their relationship.",
                'time1_1': "  2023-10-31 20:39",
                'time1_2': "  2023-10-28 07:13",
                'time1_3': "  2023-10-27 12:38",
                'timeline1_1':"    Escalation in Israel-Palestine Conflict: Gaza Rockets Target Israeli Cities, Israeli Forces Launch Airstrikes.",
                'timeline1_2':"    Israeli military spokesperson: IDF will expand ground operations.",
                'timeline1_3':"    The Israeli-Palestinian conflict has resulted in over 10,000 casualties on both sides.",
                'time2_1': "  2023-10-29 22:20",
                'time2_2': "  2023-10-26 14:35",
                'time2_3': "  2023-10-24 14:31",
                'timeline2_1':"    Ukraine to cease Russian gas transit by the end of 2024, potentially causing energy supply concerns for Europe.",
                'timeline2_2':"    Putin oversees strategic nuclear forces exercise, Russian military practices response to enemy nuclear strikes.",
                'timeline2_3':"    Biden: The United States is the strongest it has ever been, capable of supporting both Israel and Ukraine simultaneously.",
                'time3_1': "  2023-10-28 22:20",
                'time3_2': "  2023-10-26 14:35",
                'time3_3': "  2023-10-24 14:31",
                'timeline3_1':"    Common threats will only strengthen the Sino-Russian relationship.",
                'timeline3_2':"    China economy grew beyond expectations in the first three quarters of the year.",
                'timeline3_3':"    Leaders from multiple countries gather in Beijing; Xi Jinping holds bilateral talks with Putin."
            }
            # 获取当前点击的item的索引
            index = self.eventList.currentRow()
            if(index == 0):
                self.summary.setText(events['summary1'])
                self.timeLabel_1.setText(events['time1_1'])
                self.timeLabel_2.setText(events['time1_2'])
                self.timeLabel_3.setText(events['time1_3'])
                self.timeline1.setText(events['timeline1_1'])
                self.timeline2.setText(events['timeline1_2'])
                self.timeline3.setText(events['timeline1_3'])
            elif(index == 1):
                self.summary.setText(events['summary2'])
                self.timeLabel_1.setText(events['time2_1'])
                self.timeLabel_2.setText(events['time2_2'])
                self.timeLabel_3.setText(events['time2_3'])
                self.timeline1.setText(events['timeline2_1'])
                self.timeline2.setText(events['timeline2_2'])
                self.timeline3.setText(events['timeline2_3'])
            elif(index == 2):
                self.summary.setText(events['summary3'])
                self.timeLabel_1.setText(events['time3_1'])
                self.timeLabel_2.setText(events['time3_2'])
                self.timeLabel_3.setText(events['time3_3'])
                self.timeline1.setText(events['timeline3_1'])
                self.timeline2.setText(events['timeline3_2'])
                self.timeline3.setText(events['timeline3_3'])
            # 设置summary字体大小
            self.summary.setStyleSheet("font-size: 18px;")

        # 绑定eventList的item的点击事件
        self.eventList.itemClicked.connect(event_clicked)
        self.eventList.setCurrentRow(0)


    def setPage3(self):
        # 加载html
        self.historyPriceScoreLineChartWeb.load(QtCore.QUrl.fromLocalFile(HTML_PATH + 'historyPriceScoreLineChart.html'))

    def setPage2_1(self):
        model = qt_models.DataFeatureModel()
        self.tableDataFeature.setModel(model)
        # 设置列宽
        for i in range(model.columnCount()):
            self.tableDataFeature.setColumnWidth(i, 110)

        # 显示html组件
        self.missingDataPieWeb.load(
            QtCore.QUrl.fromLocalFile(HTML_PATH + 'pie.html'))

    def setPage2_2(self):
        self.tableOutputData.setModel(qt_models.OutputDataModel())

        # 显示html组件
        self.missingRateBarWeb.load(
            QtCore.QUrl.fromLocalFile(HTML_PATH + 'missingRateBar.html'))

    def setPage2_3(self):
        # listAlgo默认选择第一个item
        self.listAlgo.setCurrentRow(0)
        # 绑定listAlgo和stackedWidget_Algo
        self.listAlgo.currentRowChanged.connect(
            self.stackedWidget_Algo.setCurrentIndex)

    def setPage2_4(self):
        pass

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    signInWindow = SignInWindow()
    mainWindow = MainWindow()

    signInWindow.show()
    # mainWindow.show()

    # 登录/注册按钮打开主窗口
    signInWindow.signinButton.clicked.connect(mainWindow.show)
    signInWindow.signupButton.clicked.connect(mainWindow.show)

    sys.exit(app.exec_())