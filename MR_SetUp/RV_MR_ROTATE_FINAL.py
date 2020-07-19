

###  THIS IS GRAPHIC USER FOR CREATING A GUI FOR MR MEASUREMENT SETUP IN PYTHON WITH PYQT5
###  THIS PROGRAM WILL SET CONSTANT MAGNETIC FIELD IN MAGNETS AND
###  ROTATES THE SAMPLE AT THE DEFINITE INTERVALS AND MEASURES MAGNETIC FIELD
###  FIELD LIMIT IS SET TO 1500G OR 150 MILLI TESLA
###  PLEASE CONTACT PROF. P S ANIL KUMAR IF YOU NEED HIGHER FIELD LEVELS TO BE GENERATED
###  PLEASE CONTACT R A RAVEENDRA VARMA, PHD STUDENT FOR ANY QUERIES REGARDING INTERFACE OPERATION AND FEEDBACK

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from numpy import *
# from random import *

import pyvisa
import time
import os
import io
import serial
import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

# To use the ethernet connection instead of the GPIB interface import Socket
# instead of Visa
# from slave.transport import Visa
# We don't need to import the nanovoltmeter driver, the K6221 does this for us.
# from slave.keithley import K6221
# from slave.keithley import K2182
# from slave.srs import SR830





class RV_INTERFACE(QDialog):

    def __init__(self, parent=None):

        super(RV_INTERFACE, self).__init__(parent)
        self.originalPalette = QApplication.palette()

        self.setWindowTitle("MR_ROTATE_AND_MEASURE")            # Window Title Changed
        self.setWindowIcon(QIcon("Magnet_Icon.png"))            # ADD Logo

        self.createTitle()                  ## Creates Title of the Gui
        self.createMagFieldGroupBox()
        self.set_6221_current()
        self.sample_direction_GroupBox()
        self.createProgressBar()
        self.createInputDetails()           ## Takes Details of FileName and User
        self.createdataPlot()
        self.createliveData()
        self.createTableWidget()

        # self.createTableWidget(text)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.Title_GroupBox, 0, 0, 1, 4)
        mainLayout.addWidget(self.SetMagFieldGroupBox, 1, 0, 1, 1)
        mainLayout.addWidget(self.Current6221GroupBox, 2, 0, 1, 1)
        mainLayout.addWidget(self.Sample_Direction_GroupBox, 3, 0, 1, 1)
        mainLayout.addWidget(self.Input_GroupBox,4,0,1,1)


        # mainLayout.addWidget(self.Live_GroupBox, 0, 2, 1, 2)

        mainLayout.addWidget(self.TableWidgetGroupBox, 1, 1, 4, 2)
        mainLayout.addWidget(self.plot_GroupBox, 1, 3, 4, 1)
        mainLayout.addWidget(self.progressBar, 5, 0, 1, 4)



        self.setLayout(mainLayout)

        self.changeStyle('Fusion')                      #  Visualisation Changed to Fusion


    def createTitle(self):

        self.Title_GroupBox = QGroupBox()
        styleLabel = QLabel("MR MEASUREMENT BY SAMPLE ROTATION")
        styleLabel.setFont(QFont("Times", 14, QFont.Bold))
        styleLabel.setStyleSheet('color:royalblue')
        styleLabel.setAlignment(Qt.AlignCenter)

        Title_layout = QVBoxLayout()
        Title_layout.addWidget(styleLabel)
        self.Title_GroupBox.setLayout(Title_layout)


    def createdataPlot(self):

        self.plot_GroupBox = QGroupBox("Data Measurement Update")
        self.plot_GroupBox.setFixedWidth(500)

        # a figure instance to plot on
        self.figure = plt.figure()


        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        # self.button = QPushButton('Plot')
        # self.button.clicked.connect(self.plot)

        # set the layout
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.toolbar)
        plot_layout.addWidget(self.canvas)
        # plot_layout.addWidget(self.button)
        self.plot_GroupBox.setLayout(plot_layout)



    def changeStyle(self, styleName):                       ## Window Visualisation   Use "QApplication.setStyle(QStyleFactory.create('Fusion'))" later
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):                                 ### Push Button Pallet set as Original
            QApplication.setPalette(self.originalPalette)



    def createMagFieldGroupBox(self):
        self.SetMagFieldGroupBox = QGroupBox("Set Magnetic Field control Voltage (0 to 2.5 Volts)")
        self.SetMagFieldGroupBox.setToolTip("1V Sets Magnetic Field of 60mT")

        MLabel1 = QLabel('Field Voltage Val :')
        self.MLineEdit1 = QLineEdit()

        # MPushButton = QPushButton("Set Field")
        # MPushButton.clicked.connect(self.CurrentPushButtonClicked)

        Mlayout = QGridLayout()
        Mlayout.addWidget(MLabel1, 0, 0)
        Mlayout.addWidget(self.MLineEdit1, 0, 1)
        # Clayout.addWidget(CPushButton, 0, 2)

        self.SetMagFieldGroupBox.setLayout(Mlayout)
    #
    #
    # def MPushButtonClicked(self):  ## check properly and confirm
    #     #
    #     text = [0]
    #
    #     if self.MGrpBox1.isChecked():
    #         MStart1 = float(self.MLineEdit11.text())
    #         MEnd1 = float(self.MLineEdit12.text())
    #         MDiv1 = int(self.MLineEdit13.text())
    #
    #         text1 = sort(linspace(MStart1, MEnd1, MDiv1))
    #         text = hstack((text, text1))
    #
    #     if self.MGrpBox2.isChecked():
    #         MStart2 = float(self.MLineEdit21.text())
    #         MEnd2 = float(self.MLineEdit22.text())
    #         MDiv2 = int(self.MLineEdit23.text())
    #
    #         text2 = sort(linspace(MStart2, MEnd2, MDiv2))
    #         text = hstack((text, text2))
    #
    #     if self.MGrpBox3.isChecked():
    #         MStart3 = float(self.MLineEdit31.text())
    #         MEnd3 = float(self.MLineEdit32.text())
    #         MDiv3 = int(self.MLineEdit33.text())
    #
    #         text3 = sort(linspace(MStart3, MEnd3, MDiv3))
    #         text = hstack((text, text3))
    #
    #     if self.MGrpBox4.isChecked():
    #         MStart4 = float(self.MLineEdit41.text())
    #         MEnd4 = float(self.MLineEdit42.text())
    #         MDiv4 = int(self.MLineEdit43.text())
    #
    #         text4 = sort(linspace(MStart4, MEnd4, MDiv4))
    #         text = hstack((text, text4))
    #
    #     if self.MGrpBox5.isChecked():
    #         MStart5 = float(self.MLineEdit51.text())
    #         MEnd5 = float(self.MLineEdit52.text())
    #         MDiv5 = int(self.MLineEdit53.text())
    #
    #         text5 = sort(linspace(MStart5, MEnd5, MDiv5))
    #         text = hstack((text, text5))
    #
    #         # text2 = sort(linspace(-MEnd, -MStart, MDiv))
    #         #
    #         # text3 = concatenate([text1,text2])
    #         # # text3 = hstack((text1,text2))
    #
    #     self.textu = unique(text)
    #
    #     maxtext = max(self.textu)
    #     mintext = min(self.textu)
    #
    #     if abs(maxtext) > 2.5 or mintext < 0:
    #         print('Field Voltage Value Exceeds Limit')
    #         self.MGrpBox1.setChecked(False)
    #         self.MGrpBox2.setChecked(False)
    #         self.MGrpBox3.setChecked(False)
    #         self.MGrpBox4.setChecked(False)
    #         self.MGrpBox5.setChecked(False)
    #         self.showFieldDialog()
    #
    #         self.textu = [0]
    #
    #     if self.Mcheck_Neg.isChecked():
    #         self.Mcheck_Neg_function()
    #
    #     if self.McheckBox.isChecked():
    #         self.Mcheckbox_hysterisis()
    #
    #     # print(maxtext)
    #
    #     table_size = size(self.textu)
    #     print(self.textu)
    #     self.tableWidget.setRowCount(table_size)
    #
    #     for i in range(table_size):
    #         self.tableWidget.setItem(i, 0, QTableWidgetItem(str(self.textu[i])))
    #
    #     self.tableWidget.resizeColumnsToContents()
    #
    #     # self.tableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
    #
    #     # with open('Mdata.txt', 'w') as f:
    #     #     text = text.T   #  Transposing the array
    #     #     f.write(str(text))
    #
    #     ## try to put plot in the plot box
    #     # random data
    #     # data_val = [random() for i in range(table_size)]
    #     #
    #     # data = [text, data_val]
    #
    #     # random data
    #     # data = [random.random() for i in range(table_size)]
    #     data = [text]
    #
    #     # instead of ax.hold(False)
    #     self.figure.clear()
    #
    #     # create an axis
    #     ax = self.figure.add_subplot(111)
    #
    #     # discards the old graph
    #     # ax.hold(False) # deprecated, see above
    #
    #     # plot data
    #     ax.plot(data, '*-')
    #
    #     # refresh canvas
    #     self.canvas.draw()

    def Mcheck_Neg_function(self):

        print("Generating Negative Values...")
        text_pos = self.textu
        text_neg = -1 * text_pos

        fieldvol_stack = hstack([text_pos, text_neg])
        self.textu = unique(fieldvol_stack)
        # print(str(self.textu))

    def Mcheckbox_hysterisis(self):
        print("Generating Hysteresis Loop...")

        text_init = self.textu
        text_ext = -1 * text_init
        size_ext = size(text_ext)
        # print("Text Neg: ", str(text_ext))
        self.textu = hstack([text_init, text_ext[1:size_ext]])



    def set_6221_current(self):

        self.Current6221GroupBox = QGroupBox("Set 6221 Current in Amps (1.0E-6 to 2.0E-3)")
        self.Current6221GroupBox.setToolTip("Example: 0.002 or 2e-3 for setting 2mA")

        CLabel1 = QLabel('Current Val :')
        self.CLineEdit1 = QLineEdit()

        # CPushButton = QPushButton("Set Current")
        # CPushButton.clicked.connect(self.CurrentPushButtonClicked)

        Clayout = QGridLayout()
        Clayout.addWidget(CLabel1, 0, 0)
        Clayout.addWidget(self.CLineEdit1, 0, 1)
        # Clayout.addWidget(CPushButton, 0, 2)

        self.Current6221GroupBox.setLayout(Clayout)

    def showFieldDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Field Voltage exceeds Limit")
        msgBox.setWindowTitle("Error Message")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()

    def showCurrentDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Current exceeds Limit of 2mA")
        msgBox.setWindowTitle("Error Message")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()

    #
    #
    # def CurrentPushButtonClicked(self):  ## check properly and confirm
    #
    #     self.curr_Val6221 = self.CLineEdit1.text()
    #     print(self.curr_Val6221)
    #
    #     if abs(float(self.curr_Val6221))>2e-3:
    #         print("6221 Current Value Exceeds Limit")
    #         self.showCurrentDialog()
    #         self.CLineEdit1.setText("0")
    #
    #     else:
    #         rm = pyvisa.ResourceManager()
    #         print(rm.list_resources())
    #
    #
    #         ## --------------------------------------------------------------------------
    #         ## control keithley instruments 6221 current source
    #         ## ------------------------------------------------------------------------
    #
    #         current = rm.open_resource('GPIB0::12::INSTR')
    #         # nano = rm.open_resource('GPIB0::09::INSTR')
    #
    #         print(current.query("*IDN?"))
    #
    #         ##  set current in 6221
    #         current.write('*RST')
    #         time.sleep(0.1)
    #         current.write('SOUR:CURR ' + self.curr_Val6221)
    #         time.sleep(0.1)
    #         # inst.write()
    #         current.write('SOUR:CURR:COMP 10')
    #         time.sleep(0.1)
    #         current.write('OUTP ON')
    #         time.sleep(0.1)
    #


    def createTableWidget(self):
        Table_Length = 16

        self.TableWidgetGroupBox = QGroupBox("Field and Voltage")

        # self.tableWidget = QTableView(self)  # SELECTING THE VIEW
        # self.tableWidget.setGeometry(0, 0, 575, 575)
        # self.model = QStandardItemModel(self)  # SELECTING THE MODEL - FRAMEWORK THAT HANDLES QUERIES AND EDITS
        # self.tableWidget.setModel(self.model)  # SETTING THE MODEL
        # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #
        # self.tableWidget.setHorizontalHeader(self, QHeaderView('Field', 'Voltage', 'MR'))

        self.tableWidget = QTableWidget(Table_Length, 3)
        self.tableWidget.setFixedWidth(230)
        self.tableWidget.setHorizontalHeaderLabels(('Angle', 'Voltage', 'MR'))


        table_vbox = QVBoxLayout()

        table_vbox.setContentsMargins(5, 5, 10, 5)
        table_vbox.addWidget(self.tableWidget)

        self.TableWidgetGroupBox.setLayout(table_vbox)



    def sample_direction_GroupBox(self):

        self.Sample_Direction_GroupBox = QGroupBox("Set Sample Direction")
        self.Sample_Direction_GroupBox.setCheckable(True)
        self.Sample_Direction_GroupBox.setChecked(True)


        self.Angle_GrpBox01 = QGroupBox("Align")
        self.Angle_GrpBox01.setCheckable(True)
        self.Angle_GrpBox01.setChecked(False)

        enter_Angle_Label1 = QLabel('Angle Adjust :')
        self.enter_angle = QLineEdit(self)

        Angle_PushButton01 = QPushButton("Align Sample")
        Angle_PushButton01.clicked.connect(self.Align_Sample)

        Angle_layout01 = QGridLayout()

        Angle_layout01.addWidget(enter_Angle_Label1, 0, 0)
        Angle_layout01.addWidget(self.enter_angle, 0, 1)
        Angle_layout01.addWidget(Angle_PushButton01,1, 1)
        self.Angle_GrpBox01.setLayout(Angle_layout01)


        #
        # Angle_checkBox = QCheckBox("Set Angle to Zero")  ## CONSIDER WHILE PROGRAMMING
        # Angle_checkBox.setChecked(False)


        self.Angle_GrpBox02 = QGroupBox("Set Angle Steps")
        self.Angle_GrpBox02.setCheckable(True)
        self.Angle_GrpBox02.setChecked(False)


        Angle_Label1 = QLabel('Start Angle :')
        Angle_Label2 = QLabel('End Angle :')
        Angle_Label3 = QLabel('Angle Step :')

        self.Angle_LineEdit1 = QLineEdit()
        self.Angle_LineEdit2 = QLineEdit(self)
        self.Angle_LineEdit3 = QLineEdit(self)


        Angle_PushButton02 = QPushButton("Set Angle Steps")   ## WRITE PROGRAM FOR READING VALUES AND FILE OPENING

        Angle_PushButton02.clicked.connect(self. Angle_PushButtonClicked)


        Angle_layout02 = QGridLayout()

        Angle_layout02.addWidget(Angle_Label1, 0, 0)
        Angle_layout02.addWidget(Angle_Label2, 1, 0)
        Angle_layout02.addWidget(Angle_Label3, 2, 0)

        Angle_layout02.addWidget(self.Angle_LineEdit1, 0, 1)
        Angle_layout02.addWidget(self.Angle_LineEdit2, 1, 1)
        Angle_layout02.addWidget(self.Angle_LineEdit3, 2, 1)
        Angle_layout02.addWidget(Angle_PushButton02, 3, 1)

        self.Angle_GrpBox02.setLayout(Angle_layout02)



        layout = QGridLayout()

        layout.addWidget(self.Angle_GrpBox01, 0, 0)
        layout.addWidget(self.Angle_GrpBox02, 1, 0)

        self.Sample_Direction_GroupBox.setLayout(layout)



    def Align_Sample(self):

        print("Aligning Sample...")

        Allign = int(self.enter_angle.text())

        ser = serial.Serial('COM18', 9600, timeout=1)
        # var = str(Allign * 57)
        var1 = input("Please confirm rotation by pressing enter here: ")
        # print(var1)
        # print(type(var1))

        var = str(int(Allign) * 57)
        print(var)
        print(type(var))

        ser.write(bytes(var.encode('ascii')))
        t_end = time.time() + 10
        while time.time() < t_end:
            try:
                print(ser.readline())
                time.sleep(1)
            except ser.SerialTimeoutException:
                print(('Data could not be read'))
        print('Check for Alignment Physically.')

        # self.serial_arduino()

    def Angle_PushButtonClicked(self):
        print('Created Angle Steps...')

        if self.Angle_GrpBox02.isChecked():
            AStart = float(self.Angle_LineEdit1.text())
            AEnd = float(self.Angle_LineEdit2.text())
            self.ADiv = int(self.Angle_LineEdit3.text())
            # self.Angle_Steps = sort(linspace(AStart, AEnd, ADiv))
            self.Angle_Steps = arange(AStart, AEnd, self.ADiv)

            print(self.Angle_Steps)


### CHECK IF SERIAL ARDUINO IS REQUIRED

    def serial_arduino(self):

        ser = serial.Serial('COM18', 9600, timeout=1)
        steps = str(int(self.var) * 57)
        print(type(steps))
        print('No of Steps:', steps)
        ser.write(bytes(steps.encode('ascii')))
        t_end = time.time() + 10
        while time.time() < t_end:
            try:
                print(ser.readline())
                time.sleep(1)
            except ser.SerialTimeoutException:
                print(('Data could not be read'))
        print('Check for Alignment Physically.')

        # ser = serial.Serial()
        # ser.baudrate = 9600
        # ser.port = 'COM18'
        # time.sleep(0.1)
        # ser.open()
        # time.sleep(0.1)
        # ser.write(b'1000')
        # time.sleep(2)
        # ser.close()

        # angle = self.spinBox.value()
        #
        # steps = 1000
        #
        # arduino = serial.Serial('COM18', 9600, timeout=.1)
        # arduino.write(steps)
        # time.sleep(1)


        # rm = pyvisa.ResourceManager()
        # arduino1 = rm.open_resource("COM18")
        # arduino1.write(b"1000")
        # time.sleep(1)
        # print(arduino1.read())


    def createProgressBar(self):

        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)   ### PUT THE VARIABLE VALUE HERE FOR UPDATE


    def createInputDetails(self):
        self.Input_GroupBox = QGroupBox("Inputs of File")

        Input_Label_User = QLabel('Create Folder Name :')
        self.Input_LineEdit_User = QLineEdit()

        Input_Label_File = QLabel('Create File Name :')
        self.Input_LineEdit_File = QLineEdit()

        # dateTimeEdit = QDateTimeEdit(self.Input_GroupBox)
        # dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        Input_PushButton = QPushButton("Start Measurement")
        Input_PushButton.clicked.connect(self.createStartMeasurement)

        Input_layout = QGridLayout()
        Input_layout.addWidget(Input_Label_User, 0, 0)
        Input_layout.addWidget(self.Input_LineEdit_User, 0, 1)
        # Input_layout.addWidget(dateTimeEdit,0,2)
        Input_layout.addWidget(Input_Label_File, 1, 0)
        Input_layout.addWidget(self.Input_LineEdit_File, 1, 1)
        Input_layout.addWidget(Input_PushButton,2,1)

        self.Input_GroupBox.setLayout(Input_layout)


    def createStartMeasurement(self):

        # self.Live_LineEdit_SetCurrent.setText(self.CLineEdit1.text())
        # table_size_val = self.tableWidget.rowCount()


        folder_name = self.Input_LineEdit_User.text()
        file_name = self.Input_LineEdit_File.text() + '.txt'

        foldername = "/RV/MR_GUI/DATA_FILES/" + folder_name + "/"

        # filename = "/RV/MR_GUI/DATA_FILES/" + folder_name + "/" + file_name + ".txt"
        os.makedirs(os.path.dirname(foldername), exist_ok=True)


        directory = 'D:/RV/MR_GUI/DATA_FILES/ANGLE/'

        print("------------------------------------------------------------------")
        print("STARTING PROCESS....")
        print("Current working directory is: ", directory)
        print("Creating Folder Name:", folder_name)
        print("Creating File Name:", file_name)
        print(" ")


        self.curr_Val6221 = self.CLineEdit1.text()
        print('6221 Current Value is', self.curr_Val6221)

        if abs(float(self.curr_Val6221))>2e-3:
            print("6221 Current Value Exceeds Limit")
            self.showCurrentDialog()
            self.CLineEdit1.setText("0")

        else:


            rm = pyvisa.ResourceManager()
            print(rm.list_resources())
            srs = rm.open_resource("GPIB::7")  ## SET GPIB ADDRESS OF SRS 830 TO 7
            current = rm.open_resource('GPIB0::12::INSTR')   ## SET GPIB ADDRESS OF 6221  TO 12
            keithley = rm.open_resource("GPIB::9")   ## SET GPIB ADDRESS OF 2182A TO 9
            arduino = rm.open_resource("COM18", baud_rate = 9600)   ## COM 18 is port address of Arduino board for stepper control

            var1 = input("Confirm Rotation by pressing Enter: ")

            # ser = serial.Serial('COM18', 9600, timeout=1)


            print('Setting MAGNETIC FIELD...')

            # ## -------------------------------------------------------------
            # ## control magnetic field current source by controlling srs 830
            # ## --------------------------------------------------------------
            #
            # rm = pyvisa.ResourceManager()
            # srs = rm.open_resource("GPIB::7")  ## SET GPIB ADDRESS OF SRS 830 TO 7
            # # srs.write("*RST")
            srs.write("AUXV 4, " + self.MLineEdit1.text())
            time.sleep(1)

            print('Setting 6221 CURRENT to Sample...')

            ## --------------------------------------------------------------------------
            ## control keithley instruments 6221 current source
            ## ------------------------------------------------------------------------

            # current = rm.open_resource('GPIB0::12::INSTR')
            # # nano = rm.open_resource('GPIB0::09::INSTR')
            #
            # print(current.query("*IDN?"))
            #
            # ##  set current in 6221
            current.write('*RST')
            time.sleep(0.1)
            current.write('SOUR:CURR ' + self.curr_Val6221)
            time.sleep(0.1)
            # inst.write()
            current.write('SOUR:CURR:COMP 10')
            time.sleep(0.1)
            current.write('OUTP ON')
            time.sleep(0.1)

        if self.Angle_GrpBox02.isChecked():
            AStart = float(self.Angle_LineEdit1.text())
            AEnd = float(self.Angle_LineEdit2.text())
            self.ADiv = int(self.Angle_LineEdit3.text())
            self.Angle_Steps = arange(AStart, AEnd, self.ADiv)

            print(self.Angle_Steps)

        else:
            self.Angle_Steps = linspace(0, 350, 36)
            self.Angle_Steps = arange(0, 360, 10)


        data_table = zeros((size(self.Angle_Steps),3))
        index = 0

        # values = zeros(size(self.Angle_Steps))


        # for i in range(table_size_val):


        Init_Angle = 0

        for values in self.Angle_Steps:

            if values == 0:
                print('Angle Value is: ', values)

            else:

                print('Angle Value is: ', values)

                arduino.write(str(int(self.ADiv)*57))
                # arduino.write('1000')
                time.sleep(1)
                t_end = time.time() + 5
                arduino.read_termination = '\n'
                while time.time() < t_end:
                    try:
                        print(arduino.read())
                        time.sleep(1)
                    except Exception:
                        pass
                        # print(('Data could not be read'))


            print('Measuring MR Voltage')
            #

            keithley.write("*rst; status:preset; *cls")
            interval_in_ms = 10
            number_of_readings = 3
            keithley.write("status:measurement:enable 512; *sre 1")
            keithley.write("sample:count %d" % number_of_readings)
            keithley.write("trigger:source bus")
            keithley.write("trigger:delay %f" % (interval_in_ms / 10000.0))
            keithley.write("trace:points %d" % number_of_readings)
            keithley.write("trace:feed sense1; feed:control next")

            keithley.write("initiate")
            keithley.assert_trigger()
            keithley.wait_for_srq()

            voltages = keithley.query_ascii_values("trace:data?")
            # print(voltages)
            average_Voltage = sum(voltages) / len(voltages)

            MR = average_Voltage/float(self.curr_Val6221) # 6221 current value



            # values[i]=average_Voltage
            # print(average_Voltage)
            #
            # #### DELETE FOLLOWING LINES IN ACTUAL PROGRAMME
            #
            # average_Voltage = random.random()
            # MR = average_Voltage / float(self.curr_Val6221)  # 6221 current value

            data_table[index] = [values, average_Voltage, MR]
            #
            #
            # keithley.query("status:measurement?")
            # keithley.write("trace:clear; feed:control next")

            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(values)))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(str(average_Voltage)))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(str(MR)))

            index = index + 1

            self.tableWidget.resizeColumnsToContents()

            QApplication.processEvents()

            time.sleep(0.1)


            os.makedirs(os.path.dirname(directory), exist_ok=True)
        #
        # ## -------------------------------------------------------------
        # ## control magnetic field current source by controlling srs 830
        # ## --------------------------------------------------------------
        # rm = pyvisa.ResourceManager()
        # srs = rm.open_resource("GPIB::7")  ## SET GPIB ADDRESS OF SRS 830 TO 7

        for i in range(5):
            values = values/5
            srs.write("*RST")
            srs.write("AUXV 4, " + str(values))
            time.sleep(1)

        srs.write("*RST")
        srs.write("AUXV 4, " + str(0))
        time.sleep(1)

        ### Rotate back to Original Position


        arduino.write(str(  (int(AEnd)-int(self.ADiv))*(-57)))
        time.sleep(1)
        t_end = time.time() + 5
        arduino.read_termination = '\n'
        while time.time() < t_end:
            try:
                print(arduino.read())
                time.sleep(1)
            except Exception:
                pass
                # print(('Data could not be read'))


        directory = os.getcwd()
        os.chdir(foldername)
        print('Creating data file in directory:',directory)


        # with open(file_name, "w") as f:
        #     f.write(str(data_table)+'\n')

        savetxt(file_name, data_table, delimiter=',', fmt='%1.4e')  # data_table is an array
        print('Text file created')

            # self.tableWidget.setItem(5, 1, QTableWidgetItem(str(25)))

        ##  -----------------------------------------------
        ## stop current source 6221 after measurement
        ##----------------------------------------------

        # rm = pyvisa.ResourceManager()
        # current = rm.open_resource('GPIB0::12::INSTR')
        # current.write('OUTP OFF')


        ## ---------------
        ## creating plot
        ## -------------

        # data[:,1] = data_table[:,1]
        # data[:, 2] = data_table[:, 3]
        data = data_table[:, 0:2]

        print(data_table)

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.plot(data[:,0], data[:,1],  '*-')
        ax.set_title(self.Input_LineEdit_File.text())

        # self.figure.text(0.5, 0.04, 'Magnetic Field (mT)', ha='center', va='center')
        # self.figure.text(0, 0.5, 'Magneto Resistance (Ohm)', ha='center', va='center', rotation='vertical' )

        # refresh canvas
        self.canvas.draw()


        #

        self.figure.savefig(self.Input_LineEdit_File.text()+'.svg', format='svg')
        self.figure.savefig(self.Input_LineEdit_File.text()+'.png', format='png')

    #
    # def createTableValue(self, i):
    #     ## measure volatage
    #     rm = pyvisa.ResourceManager()
    #     keithley = rm.open_resource("GPIB::9")
    #
    #     keithley.write("*rst; status:preset; *cls")
    #     interval_in_ms = 10
    #     number_of_readings = 5
    #     keithley.write("status:measurement:enable 512; *sre 1")
    #     keithley.write("sample:count %d" % number_of_readings)
    #     keithley.write("trigger:source bus")
    #     keithley.write("trigger:delay %f" % (interval_in_ms / 1000.0))
    #     keithley.write("trace:points %d" % number_of_readings)
    #     keithley.write("trace:feed sense1; feed:control next")
    #
    #     keithley.write("initiate")
    #     keithley.assert_trigger()
    #     keithley.wait_for_srq()
    #
    #     voltages = keithley.query_ascii_values("trace:data?")
    #     print(voltages)
    #     average_Voltage = sum(voltages) / len(voltages)
    #     self.Live_LineEdit_CurField.setText(str(average_Voltage))
    #
    #
    #
    #     # print(average_Voltage)
    #
    #     keithley.query("status:measurement?")
    #     keithley.write("trace:clear; feed:control next")
    #
    #     self.tableWidget.setItem(i, 1, QTableWidgetItem(str(average_Voltage)))
    #     self.tableWidget.resizeColumnsToContents()





    def createliveData(self):

        self.Live_GroupBox = QGroupBox("Live Data")

        Live_Label_TotLoop = QLabel('Total Loops :')
        self.Live_LineEdit_TotLoop = QLineEdit()

        Live_Label_CurLoop = QLabel('CurrentLoop No :')
        self.Live_LineEdit_CurLoop = QLineEdit()

        Live_Label_CurField= QLabel('Magnetic Field :')
        self.Live_LineEdit_CurField = QLineEdit()

        Live_Label_SetCurrent = QLabel('Set Current :')
        self.Live_LineEdit_SetCurrent = QLineEdit()


        Live_layout = QGridLayout()
        Live_layout.addWidget(Live_Label_TotLoop, 0, 0)
        Live_layout.addWidget(self.Live_LineEdit_TotLoop, 0, 1)

        Live_layout.addWidget(Live_Label_CurLoop,0,2)
        Live_layout.addWidget(self.Live_LineEdit_CurLoop,0,3)

        Live_layout.addWidget(Live_Label_CurField, 1, 0)
        Live_layout.addWidget(self.Live_LineEdit_CurField, 1, 1)


        Live_layout.addWidget(Live_Label_SetCurrent, 1, 2)
        Live_layout.addWidget(self.Live_LineEdit_SetCurrent, 1, 3)


        self.Live_GroupBox.setLayout(Live_layout)


    def advanceProgressBar(self):

        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)






if __name__ == '__main__':

    import sys


    app = QApplication(sys.argv)

    gallery = RV_INTERFACE()

    gallery.show()

    sys.exit(app.exec_())
