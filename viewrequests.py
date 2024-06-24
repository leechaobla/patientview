from PyQt5 import QtWidgets, QtCore
import pymysql


class ViewRequestsWidget(QtWidgets.QWidget):
    back_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ViewRequestsWidget, self).__init__(parent)

        self.setWindowTitle("View Requests")
        self.resize(537, 868)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.list_widget = QtWidgets.QListWidget(self)
        self.layout.addWidget(self.list_widget)

        self.button_back = QtWidgets.QPushButton("Back", self)
        self.button_back.setFixedSize(120, 40)
        self.layout.addWidget(self.button_back, alignment=QtCore.Qt.AlignCenter)
        self.button_back.clicked.connect(self.request_back)

        self.populate_requests()

    def request_back(self):
        self.back_requested.emit()

    def populate_requests(self):
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
            cursor.execute("""
                SELECT a.appointment_id, d.doctor_name, c.clinic_name, a.illness, a.appointment_date, a.appointment_time
                FROM appointments a
                INNER JOIN doctors d ON a.doctor_id = d.doctor_id
                INNER JOIN clinics c ON a.clinic_id = c.clinic_id
            """)
            requests = cursor.fetchall()

            if not requests:
                self.list_widget.addItem("There are no active requests.")
            else:
                for request in requests:
                    appointment_id = request[0]
                    doctor_name = request[1]
                    clinic_name = request[2]
                    illness = request[3]
                    appointment_date = request[4]
                    appointment_time = request[5]

                    item_text = (
                        f"Appointment ID: {appointment_id}\n"
                        f"Doctor: {doctor_name}\n"
                        f"Clinic: {clinic_name}\n"
                        f"Illness: {illness}\n"
                        f"Date: {appointment_date}\n"
                        f"Time: {appointment_time}"
                    )
                    self.list_widget.addItem(item_text)
                    self.list_widget.addItem("")

        except pymysql.MySQLError as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", str(e))
        finally:
            if connection:
                connection.close()







