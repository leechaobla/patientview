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
            'user': 'terry',
            'password': '',
            'database': 'appointmentmanagement',
            'charset': 'utf8mb4'
        }

        try:
            connection = pymysql.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM appointments")
            requests = cursor.fetchall()

            if not requests:
                self.list_widget.addItem("There are no active requests.")
            else:
                for request in requests:
                    item_text = f"Appointment ID: {request[0]} - Clinic: {request[1]} - Date: {request[2]} - Doctor: {request[3]}"
                    self.list_widget.addItem(item_text)

        except pymysql.MySQLError as e:
            QtWidgets.QMessageBox.critical(None, "Database Error", str(e))
        finally:
            if connection:
                connection.close()
