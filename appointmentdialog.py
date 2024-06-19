# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql


class AppointmentDialog(QtWidgets.QDialog):
    def __init__(self, clinic_name, parent=None):
        super(AppointmentDialog, self).__init__(parent)
        self.setWindowTitle(f"Request Doctor at {clinic_name}")
        self.setGeometry(100, 100, 400, 300)
        self.clinic_name = clinic_name

        # Layout and widgets
        layout = QtWidgets.QVBoxLayout()

        self.label_doctor = QtWidgets.QLabel("Select Doctor:")
        layout.addWidget(self.label_doctor)

        self.combo_doctors = QtWidgets.QComboBox()
        layout.addWidget(self.combo_doctors)

        self.label_details = QtWidgets.QLabel("Enter Appointment Details:")
        layout.addWidget(self.label_details)

        self.text_details = QtWidgets.QTextEdit()
        layout.addWidget(self.text_details)

        self.button_submit = QtWidgets.QPushButton("Submit Request")
        self.button_submit.clicked.connect(self.submit_request)
        layout.addWidget(self.button_submit)

        self.setLayout(layout)


        self.populate_doctors()

    def populate_doctors(self):

        db_config = {
            'host': '127.0.0.1',
            'user': 'root',
            'password': '10013lool',
            'database': 'doctorslist',
            'charset': 'utf8mb4'
        }

        try:

            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()


            cursor.execute("SELECT doctor_name FROM doctors")
            doctors = cursor.fetchall()


            for doctor in doctors:
                self.combo_doctors.addItem(doctor[0])

        except pymysql.MySQLError as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", str(e))

        finally:

            if connection:
                connection.close()

    def submit_request(self):
        doctor = self.combo_doctors.currentText()
        details = self.text_details.toPlainText()
        if doctor and details:
            QtWidgets.QMessageBox.information(self, "Request Submitted",
                                              f"Doctor {doctor} has been requested at {self.clinic_name}.\nDetails: {details}")
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Incomplete Data",
                                          "Please select a doctor and enter the appointment details.")
