# This Python file uses the following encoding: utf-8

from datetime import datetime
import os
from pathlib import Path
from pickle import TRUE
import sys

import urllib.request
from entity.task import Task
from controller import Controller
import numpy as np
from PySide6.QtCharts import (QChart, QChartView, QPieSeries,QLineSeries,
                            QBarCategoryAxis, QBarSeries, QBarSet, QValueAxis)
from PySide6.QtGui import (QPainter,QImage,QPixmap)
from PySide6.QtCore import (QFile,QDate,QPointF,Qt,QCalendar)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                              QTextEdit, QVBoxLayout, QWidget , QFrame,QListWidget
                               ,QSizePolicy,QTabWidget,QDateEdit,QProgressBar,
                               QToolBox,QScrollArea,QScrollBar)


class Widget(QWidget):

    num_grid_rows = 3
    num_buttons = 4

    def __init__(self):
        super(Widget, self).__init__()
        #self.controller = Controller("N")
        allIds = [70,24,10]#self.controller.getAllIds()
        print(allIds)

        self.controller = Controller()
        self.pId = 70
        self.selectedProject = self.controller.selectProject(self.pId)
        #print(self.selectedProject)
        x = list(self.controller.getUsers().values())
        self.user = None
        self.controller.showTask()
        for u in x:
            if len(u.tasks.values()) != 0 :
                self.user  = u
        self.controller.showTask()
        self.tasks = self.user.tasks
        self.selectedTask = Task(0)
        self.selectedProject = None

        self.load_ui()
        self.create_menu()
        self.createBasicMenu()
        self.createDataShow()
        self.setFixedSize(1000,600)

        
        big_editor = QTextEdit()
        big_editor.setPlainText("This widget takes up all the remaining space "
                "in the top-level layout.")

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QHBoxLayout()
        main_layout.setMenuBar(self._menu_bar)
        main_layout.addWidget(self._basicMenu)
        main_layout.addWidget(self._dataShow)
        #main_layout.addWidget(self._form_group_box)
        self.setLayout(main_layout)

        self.setWindowTitle("Basic Layouts")

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()

    def create_menu(self):
        self._menu_bar = QMenuBar()

        self._file_menu = QMenu("&File", self)
        self._exit_action = self._file_menu.addAction("E&xit")
        self._menu_bar.addMenu(self._file_menu)

        self._exit_action.triggered.connect(self.accept)

    def createBasicMenu(self):
        self._basicMenu = QFrame()
        self._basicMenu.setFixedSize(200,600)
        mainLayout = QVBoxLayout()
        self._profile = QWidget()
        self._profile.setFixedHeight(150)
        self._profile.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        profieLayout = QGridLayout()
        self._firstName = QLabel(self.user.firstName)
        self._lastName = QLabel(self.user.lastName)
        self._email = QLabel(self.user.email)

        url = self.user.image
        image = QImage()
        self._profileImage = QLabel()
        self._profileImage.setFixedSize(100,100)
        w = self._profileImage.width()
        h = self._profileImage.height()
        if url != None : 
            data = urllib.request.urlopen(url).read()

        
            image.loadFromData(data)
            self._profileImage.setPixmap(QPixmap(image).scaled(w,h,Qt.KeepAspectRatio))
        else :
            self._profileImage.setPixmap(QPixmap("./Stat/res/profile.jpg").scaled(w,h,Qt.KeepAspectRatio))
        
        
       
        profieLayout.addWidget(self._profileImage,0,0,1,2)
        profieLayout.addWidget(self._firstName,1,0)
        profieLayout.addWidget(self._lastName,1,1)
        profieLayout.addWidget(self._email,2,0,1,2)
        self._profile.setLayout(profieLayout)

        self._project = QWidget()
        self._profile.setFixedHeight(200)
        projectLayout = QVBoxLayout()
        projectLayout.setSpacing(0)
        projectList = QListWidget()
        projectList.setMaximumHeight(200)
        projectList.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed)
        for p in self.controller.projects.keys():
            projectList.addItem(str(p))

        #projectLayout.addWidget(QLabel("All Projects"))
        projectLayout.addWidget(projectList)
        self._project.setLayout(projectLayout)
        self._project.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        mainLayout.addWidget(self._profile)
        mainLayout.addWidget(self._project)
        self._basicMenu.setLayout(mainLayout)


    def selectTask(self):
        self.selectedTask = self.tasks[int(self.sender().text())]
        self.selectedTask.print()
        self.updateTaskData()

    def updateTaskData(self):
        self._status.setText("Status : "+self.selectedTask.status)
        self._workload.setText("Workload : "+str(self.selectedTask.workload))
        self._description.setText("Content : "+self.selectedTask.content)
        self._name.setText(self.selectedTask.name)
        url = self.selectedTask.image 
        data = urllib.request.urlopen(url).read()

        image = QImage()
        image.loadFromData(data)
        self._taskImg.setPixmap(QPixmap(image))
 

        date = self.selectedTask.startDate.split("-")
        start = QDate(int(date[0]),int(date[1]),int(date[2]))
        self._startDate.setDate(start)
        date = self.selectedTask.dueDate.split("-")
        end = QDate(int(date[0]),int(date[1]),int(date[2]))
        self._dueDate.setDate(end)
        now = QDate.currentDate()

        percent = min(100,int(now.daysTo(start)/end.daysTo(start))*100)
      
        self._countdown.setValue(percent)


    def createTabTask(self):
        self._taskWidget = QWidget()
        taskLayout = QGridLayout()

        #Q2
        _view = QWidget()
        _viewLayout = QVBoxLayout()
        _search = QLineEdit()
        _search.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed)
        _viewLayout.addWidget(_search)

        _scroll = QScrollArea()
        _data = QWidget()
        _dataLayout = QVBoxLayout()
        _scroll.addScrollBarWidget(QWidget(),Qt.AlignRight)
        #dataL = self.selectedProject.users[""].task.values()
        _scroll.setVerticalScrollBar(QScrollBar())
        
        for t in list(self.tasks.values()):
            _dataView = QPushButton(str(t.id))
            _dataView.setFlat(True)
            _dataView.clicked.connect(self.selectTask)
            _dataLayout.addWidget(_dataView)

        _data.setLayout(_dataLayout)
        _scroll.setWidget(_data)
        #_data.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Maximum)
        _viewLayout.addWidget(_scroll)
        _view.setLayout(_viewLayout)


        #Q1
        

        _content = QWidget()
        _contentLayout = QGridLayout()
        _content.setLayout(_contentLayout)
        self._name = QLabel("Name")

        


        self._taskImg = QLabel()
        w = self._taskImg.width()
        h = self._taskImg.height()
        self._taskImg.setPixmap(QPixmap("./Stat/res/empty.png").scaled(w,h,Qt.KeepAspectRatio))
        self._taskImg.setAlignment(Qt.AlignCenter)

        _contentLayout.addWidget(self._taskImg,0,0,1,2)
        _content.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        _content.setFixedHeight(250)
        _content.setFixedWidth(600)
        self._startDate = QDateEdit()
        self._startDate.setReadOnly(True)
        self._dueDate = QDateEdit()
        self._dueDate.setReadOnly(True)
        self._countdown = QProgressBar()
        #find percent
        percent = 50
        self._countdown.setValue(percent)
        self._status = QLabel(self.selectedTask.status if self.selectedTask!=None else "-")
        self._workload = QLabel(self.selectedTask.workload if self.selectedTask!=None else "-")
        self._description = QLabel(self.selectedTask.content if self.selectedTask!=None else "-")
        
        _contentLayout.addWidget(self._startDate,1,0,1,1)
        _contentLayout.addWidget(self._dueDate,1,1,1,1)
        _contentLayout.addWidget(self._countdown,2,0,1,2)
        _contentLayout.addWidget(self._status,3,0,1,1)
        _contentLayout.addWidget(self._workload,3,1,1,1)
        _contentLayout.addWidget(self._description,4,0,2,2)

        #Q3

        self._stat = QToolBox()
        self._stat.setContentsMargins(0,0,0,0)

        self.pSeries1 = QPieSeries()
        stat = self.user.statusStat
        i = 0
        for s in stat.keys():
            self.pSeries1.append(s,stat[s])
            chart_slice1 = self.pSeries1.slices()[i]
            i+=1
            #chart_slice1.setExploded()
            chart_slice1.setLabelVisible()
        self.pChart1 = QChart()
        self.pChart1.addSeries(self.pSeries1)
        self.pChart1.legend().hide()
        self._chartPView1 = QChartView(self.pChart1)
        self._chartPView1.setContentsMargins(0,0,0,0)



        self.pSeries2 = QPieSeries()
        stat = self.user.contentStat
        i = 0
        for c in stat.keys():
            print(c)
            self.pSeries2.append(c,stat[c])
            chart_slice2 = self.pSeries2.slices()[i]
            i+=1
            #chart_slice2.setExploded()
            chart_slice2.setLabelVisible()
        self.pChart2 = QChart()
        self.pChart2.addSeries(self.pSeries2)
        self.pChart2.legend().hide()
        self._chartPView2 = QChartView(self.pChart2)
        self._chartPView2.setContentsMargins(0,0,0,0)
        #self._contentChart.(self._chart_view)
        

        self._stat.addItem(self._chartPView1,"Content")
        self._stat.addItem(self._chartPView2,"Status")


        #Q4
        self.lSeries = QLineSeries()
        timeline = self.user.dateStat["timeline"]
        startEnd = self.user.dateStat["startEnd"]
        start = QDate(startEnd[0].year,startEnd[0].month,startEnd[0].day)
        end = QDate(startEnd[1].year,startEnd[1].month,startEnd[1].day)
        duration = start.daysTo(end)
        cat = []
        tmp = ""
        for i in range(duration):
            tmp = start.addDays(i).toString().split()
            tmp = tmp[2]+"/"+str(start.addDays(i).month())
            if i%30==0 :
                print(i,start.addDays(i),tmp)
                cat.append(tmp)
            else :
                cat.append(" ")
            self.lSeries.append(i,timeline[i])
        cat.append(tmp)

        self.lChart = QChart()
        self.lChart.legend().hide()
        self.lChart.addSeries(self.lSeries)
        self.lChart.createDefaultAxes()
        self.lChart.setTitle("Workload Timeline")
        x = QBarCategoryAxis()
        x.append(cat)
        y = QValueAxis()
        y.setRange(0,np.max(timeline))
        self.lChart.setAxisX(x)
        self.lChart.setAxisY(y)
        self._chartLView = QChartView(self.lChart)
        self._chartLView.setRenderHint(QPainter.Antialiasing)

     


       



        _view.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        _view.setFixedSize(350,200)
        _content.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred)
        _content.setFixedSize(350,200)
        taskLayout.addWidget(_view,0,0)
        taskLayout.addWidget(_content,0,1)
        taskLayout.addWidget(self._stat,1,0)
        taskLayout.addWidget(self._chartLView,1,1)

        self._taskWidget.setLayout(taskLayout)

    def createDataShow(self):
        self._dataShow = QTabWidget()
        self.createTabTask()
       
        noteWidget = QWidget()
        self._dataShow.addTab(self._taskWidget,"Task")
        
        self._dataShow.addTab(noteWidget,"Note")
        
        noteLayout = QGridLayout()

        
        noteWidget.setLayout(noteLayout)


    def create_form_group_box(self):
        self._form_group_box = QGroupBox("Form layout")
        layout = QFormLayout()
        layout.addRow(QLabel("Line 1:"), QLineEdit())
        layout.addRow(QLabel("Line 2, long text:"), QComboBox())
        layout.addRow(QLabel("Line 3:"), QSpinBox())
        self._form_group_box.setLayout(layout)

    def accept(self):
        pass

    def reject(self):
        pass
if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
