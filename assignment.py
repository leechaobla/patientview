# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pymysql
from appointmentdialog import AppointmentDialog


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(537, 868)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 80, 216, 16))
        self.label_2.setObjectName("label_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 140, 509, 261))
        self.groupBox.setObjectName("groupBox")
        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setGeometry(QtCore.QRect(10, 30, 491, 211))
        self.listWidget.setObjectName("listWidget")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 430, 509, 255))
        self.groupBox_2.setObjectName("groupBox_2")
        self.webEngineView = QWebEngineView(self.groupBox_2)
        self.webEngineView.setGeometry(QtCore.QRect(20, 50, 481, 161))
        self.webEngineView.setObjectName("webEngineView")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(220, 20, 71, 20))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 740, 511, 81))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 40, 123, 23))
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 537, 21))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)


        self.pushButton.clicked.connect(self.request_doctor)


        self.populate_clinic_list()


        file_path = "file:///C:/Users/Terrence/AppData/Local/Programs/Python/Python312/Lib/site-packages/QtDesigner/Project/index.html"
        self.webEngineView.setUrl(QtCore.QUrl(file_path))

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Call a Doctor"))
        self.label_2.setText(_translate("mainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Where appointments are made easy !</span></p></body></html>"))
        self.groupBox.setTitle(_translate("mainWindow", "Clinic List"))
        self.groupBox_2.setTitle(_translate("mainWindow", "Clinic Map"))
        self.label_3.setText(_translate("mainWindow",
                                        "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">Map View</span></p></body></html>"))
        self.pushButton.setText(_translate("mainWindow", "Request a Doctor"))
        self.label.setText(_translate("mainWindow",
                                      "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600; text-decoration: underline;\">Call a Doctor</span></p></body></html>"))

    def populate_clinic_list(self):
        # Database connection parameters
        db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '10013lool',
            'database': 'appointmentmanagement',
            'charset': 'utf8mb4'
        }

        try:

            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()


            cursor.execute("SELECT clinic_name FROM clinics")
            clinics = cursor.fetchall()


            for clinic in clinics:
                self.listWidget.addItem(clinic[0])

        except pymysql.MySQLError as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", str(e))

        finally:

            if connection:
                connection.close()

    def request_doctor(self):
        selected_clinic = self.listWidget.currentItem()
        if selected_clinic:
            clinic_name = selected_clinic.text()
            dialog = AppointmentDialog(clinic_name, self.centralwidget)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:

                pass
        else:
            QtWidgets.QMessageBox.warning(None, "No Clinic Selected", "Please select a clinic from the list.")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
