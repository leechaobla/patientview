import sys
import MySQLdb
from PyQt5 import QtWidgets, QtCore
from assignment import Ui_mainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Connect to MySQL database
        self.conn = MySQLdb.connect(
            host='localhost',
            user='terry',
            passwd='10013lool',
            db='clinic_database'
        )
        self.cursor = self.conn.cursor()

        # Load clinics into the list widget
        self.load_clinics()

        # Connect buttons to functions
        self.pushButton.clicked.connect(self.request_doctor)

    def load_clinics(self):
        self.cursor.execute("SELECT name FROM clinics")
        clinics = self.cursor.fetchall()
        for clinic in clinics:
            self.listWidget.addItem(clinic[0])

    def request_doctor(self):
        selected_clinic = self.listWidget.currentItem()
        if selected_clinic:
            clinic_name = selected_clinic.text()
            QtWidgets.QMessageBox.information(self, "Request Sent", f"Doctor requested for {clinic_name}")
        else:
            QtWidgets.QMessageBox.warning(self, "No Clinic Selected", "Please select a clinic from the list.")

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
