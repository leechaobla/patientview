import pytest
from PyQt5 import QtWidgets, QtCore
from unittest.mock import MagicMock
from appointmentdialog import AppointmentDialog

@pytest.fixture
def app(qtbot):
    test_app = QtWidgets.QApplication.instance()
    if test_app is None:
        test_app = QtWidgets.QApplication([])
    yield test_app
    test_app.quit()

@pytest.fixture
def dialog(qtbot):
    dialog = AppointmentDialog("Test Clinic")
    qtbot.addWidget(dialog)
    yield dialog
    dialog.close()

def test_empty_illness(qtbot, dialog, monkeypatch):
    dialog.text_illness.clear()
    dialog.combo_doctors.addItem("Dr. Test", 1)
    dialog.combo_doctors.setCurrentIndex(0)
    dialog.date_edit.setDate(QtCore.QDate.currentDate().addDays(1))
    dialog.time_edit.setTime(QtCore.QTime.currentTime().addSecs(3600))

    # Mock QMessageBox to avoid actual dialogs popping up
    mock_warning = MagicMock()
    monkeypatch.setattr(QtWidgets.QMessageBox, 'warning', mock_warning)

    with qtbot.waitSignal(dialog.button_submit.clicked, raising=False):
        qtbot.mouseClick(dialog.button_submit, QtCore.Qt.LeftButton)

    # Assertions
    assert mock_warning.called
    assert mock_warning.call_count == 1
    assert "Incomplete Data" in str(mock_warning.call_args)



def test_invalid_datetime(qtbot, dialog, monkeypatch):
    dialog.text_illness.setText("Test Illness")
    dialog.combo_doctors.addItem("Dr. Test", 1)
    dialog.combo_doctors.setCurrentIndex(0)
    dialog.date_edit.setDate(QtCore.QDate.currentDate().addDays(-1))
    dialog.time_edit.setTime(QtCore.QTime.currentTime().addSecs(-3600))

    # Mock QMessageBox to avoid actual dialogs popping up
    mock_warning = MagicMock()
    monkeypatch.setattr(QtWidgets.QMessageBox, 'warning', mock_warning)

    with qtbot.waitSignal(dialog.button_submit.clicked, raising=False):
        qtbot.mouseClick(dialog.button_submit, QtCore.Qt.LeftButton)

    # Assertions on the mocked QMessageBox
    assert mock_warning.called
    assert mock_warning.call_count == 1
    args, kwargs = mock_warning.call_args
    assert "Invalid Date/Time" in args[1]

def test_valid_submission(qtbot, dialog, monkeypatch):
    dialog.text_illness.setText("Test Illness")
    dialog.combo_doctors.addItem("Dr. Test", 1)
    dialog.combo_doctors.setCurrentIndex(0)
    dialog.date_edit.setDate(QtCore.QDate.currentDate().addDays(1))
    dialog.time_edit.setTime(QtCore.QTime.currentTime().addSecs(3600))

    # Mock database connection and cursor
    def mock_connect(*args, **kwargs):
        return mock_cursor()

    def mock_cursor():
        cursor = MagicMock()
        cursor.fetchone.return_value = (1,)
        cursor.execute.return_value = None
        cursor.close.return_value = None
        return cursor

    monkeypatch.setattr("pymysql.connect", mock_connect)

    # Mock QMessageBox to avoid actual dialogs popping up
    mock_information = MagicMock()
    monkeypatch.setattr(QtWidgets.QMessageBox, 'information', mock_information)

    with qtbot.waitSignal(dialog.button_submit.clicked, raising=False):
        qtbot.mouseClick(dialog.button_submit, QtCore.Qt.LeftButton)

    # Assertions on the mocked QMessageBox
    assert mock_information.called
    assert mock_information.call_count == 1
    args, kwargs = mock_information.call_args
    assert "Request Submitted" in args[1]

class mock_connect:
    def __init__(self, *args, **kwargs):
        pass

    def cursor(self):
        return self

    def execute(self, query, params=None):
        return self

    def fetchone(self):
        return [1]

    def commit(self):
        pass

    def close(self):
        pass
