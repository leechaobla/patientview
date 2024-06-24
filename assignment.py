from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from appointmentdialog import AppointmentDialog
import os
from viewrequests import ViewRequestsWidget
from databasehandler import DatabaseHandler


class Ui_mainWindow(object):
    def __init__(self):
     self.db_handler = DatabaseHandler({
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': 'appointmentmanagement',
        'charset': 'utf8mb4'
     })
     self.db_handler.connect()
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(537, 868)

        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.stacked_widget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stacked_widget.setGeometry(QtCore.QRect(0, 0, 537, 868))

        self.main_page = QtWidgets.QWidget()
        self.stacked_widget.addWidget(self.main_page)

        self.label_2 = QtWidgets.QLabel(self.main_page)
        self.label_2.setGeometry(QtCore.QRect(160, 80, 216, 16))
        self.label_2.setObjectName("label_2")

        self.groupBox = QtWidgets.QGroupBox(self.main_page)
        self.groupBox.setGeometry(QtCore.QRect(10, 140, 509, 261))
        self.groupBox.setObjectName("groupBox")

        self.listWidget = QtWidgets.QListWidget(self.groupBox)
        self.listWidget.setGeometry(QtCore.QRect(10, 30, 491, 211))
        self.listWidget.setObjectName("listWidget")

        self.groupBox_2 = QtWidgets.QGroupBox(self.main_page)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 430, 509, 255))
        self.groupBox_2.setObjectName("groupBox_2")

        self.webEngineView = QWebEngineView(self.groupBox_2)
        self.webEngineView.setGeometry(QtCore.QRect(20, 50, 481, 161))
        self.webEngineView.setObjectName("webEngineView")

        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(220, 20, 71, 20))
        self.label_3.setObjectName("label_3")

        self.pushButton = QtWidgets.QPushButton(self.main_page)
        self.pushButton.setGeometry(QtCore.QRect(10, 740, 511, 81))
        self.pushButton.setObjectName("pushButton")

        self.label = QtWidgets.QLabel(self.main_page)
        self.label.setGeometry(QtCore.QRect(200, 40, 123, 23))
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")

        self.pushButton_view_requests = QtWidgets.QPushButton(self.main_page)
        self.pushButton_view_requests.setGeometry(QtCore.QRect(10, 650, 511, 31))
        self.pushButton_view_requests.setObjectName("pushButton_view_requests")
        self.pushButton_view_requests.setText("View Submitted Requests")

        self.stacked_widget.addWidget(self.main_page)

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

        self.pushButton_view_requests.clicked.connect(self.open_view_requests_page)
        self.pushButton.clicked.connect(self.request_doctor)

        self.populate_clinic_list()

        html_file_path = os.path.abspath('index.html')
        self.webEngineView.setUrl(QtCore.QUrl.fromLocalFile(html_file_path))

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

    def open_view_requests_page(self):
        self.view_requests_widget = ViewRequestsWidget()
        self.view_requests_widget.back_requested.connect(self.show_main_page)
        self.stacked_widget.addWidget(self.view_requests_widget)
        self.stacked_widget.setCurrentWidget(self.view_requests_widget)

    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def populate_clinic_list(self):
        clinics = self.db_handler.execute_query("SELECT clinic_name FROM clinics")
        self.listWidget.clear()
        if clinics:
            for clinic in clinics:
                self.listWidget.addItem(clinic[0])
            self.listWidget.clearSelection()
        else:
            QtWidgets.QMessageBox.critical(None, "Database Error", "Failed to retrieve clinic list.")

        self.listWidget.clearSelection()

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
