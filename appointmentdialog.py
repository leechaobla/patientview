from PyQt5 import QtWidgets, QtCore
import pymysql

class AppointmentDialog(QtWidgets.QDialog):
    def __init__(self, clinic_name, parent=None):
        super(AppointmentDialog, self).__init__(parent)
        self.setWindowTitle(f"Request Doctor at {clinic_name}")
        self.setGeometry(100, 100, 400, 400)
        self.clinic_name = clinic_name

        layout = QtWidgets.QVBoxLayout()

        self.label_doctor = QtWidgets.QLabel("Select Doctor:")
        layout.addWidget(self.label_doctor)

        self.combo_doctors = QtWidgets.QComboBox()
        layout.addWidget(self.combo_doctors)

        self.label_illness = QtWidgets.QLabel("Enter Illness:")
        layout.addWidget(self.label_illness)

        self.text_illness = QtWidgets.QLineEdit()
        layout.addWidget(self.text_illness)

        self.label_date = QtWidgets.QLabel("Select Appointment Date:")
        layout.addWidget(self.label_date)

        self.date_edit = QtWidgets.QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QtCore.QDate.currentDate())
        layout.addWidget(self.date_edit)

        self.label_time = QtWidgets.QLabel("Select Appointment Time:")
        layout.addWidget(self.label_time)

        self.time_edit = QtWidgets.QTimeEdit()
        self.time_edit.setTime(QtCore.QTime.currentTime())
        layout.addWidget(self.time_edit)

        self.button_submit = QtWidgets.QPushButton("Submit Request")
        self.button_submit.clicked.connect(self.submit_request)
        layout.addWidget(self.button_submit)

        self.setLayout(layout)

        self.populate_doctors()

    def populate_doctors(self):
        db_config = {
            'host': '127.0.0.1',
            'user': 'terry',
            'password': '',
            'database': 'appointmentmanagement',
            'charset': 'utf8mb4'
        }

        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()

            query = """
            SELECT doctor_name, doctor_ID FROM doctors 
            WHERE doctor_status = 'Free' AND clinic_ID = (
                SELECT clinic_ID FROM clinics WHERE clinic_name = %s
            )
            """
            cursor.execute(query, (self.clinic_name,))
            doctors = cursor.fetchall()

            for doctor in doctors:
                self.combo_doctors.addItem(doctor[0], doctor[1])

        except pymysql.MySQLError as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", str(e))

        finally:
            if connection:
                connection.close()

    def submit_request(self):
        doctor = self.combo_doctors.currentText()
        doctor_id = self.combo_doctors.currentData()
        illness = self.text_illness.text()
        appointment_date = self.date_edit.date()
        appointment_time = self.time_edit.time()

        current_date = QtCore.QDate.currentDate()
        current_time = QtCore.QTime.currentTime()

        if appointment_date < current_date or (appointment_date == current_date and appointment_time < current_time):
            QtWidgets.QMessageBox.warning(self, "Invalid Date/Time",
                                          "The appointment date and time cannot be in the past. Please select a valid date and time.")
            return

        if doctor and illness and appointment_date and appointment_time:
            db_config = {
                'host': '127.0.0.1',
                'user': 'root',
                'password': '',
                'database': 'appointmentmanagement',
                'charset': 'utf8mb4'
            }

            try:
                connection = pymysql.connect(**db_config)
                cursor = connection.cursor()

                cursor.execute("SELECT clinic_ID FROM clinics WHERE clinic_name = %s", (self.clinic_name,))
                clinic_id = cursor.fetchone()[0]

                query = """
                INSERT INTO appointments (doctor_ID, clinic_ID, illness, appointment_date, appointment_time) 
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (doctor_id, clinic_id, illness, appointment_date.toString(QtCore.Qt.ISODate), appointment_time.toString(QtCore.Qt.ISODate)))
                connection.commit()

                QtWidgets.QMessageBox.information(self, "Request Submitted",
                                                  f"Doctor {doctor} has been requested at {self.clinic_name}.\n"
                                                  f"Illness: {illness}\n"
                                                  f"Date: {appointment_date.toString(QtCore.Qt.ISODate)}\n"
                                                  f"Time: {appointment_time.toString(QtCore.Qt.ISODate)}")
                self.accept()

            except pymysql.MySQLError as e:
                QtWidgets.QMessageBox.critical(None, "Database Error", str(e))

            finally:
                if connection:
                    connection.close()

        else:
            QtWidgets.QMessageBox.warning(self, "Incomplete Data",
                                          "Please fill in all the details.")
