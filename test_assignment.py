import sys
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QListWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.uic.properties import QtCore


from assignment import Ui_mainWindow
from viewrequests import ViewRequestsWidget
from appointmentdialog import AppointmentDialog


@pytest.fixture
def setup_ui(qtbot):
    app = QApplication(sys.argv)
    ui = Ui_mainWindow()
    mainWindow = QMainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    qtbot.addWidget(mainWindow)
    yield app, ui, mainWindow
    sys.exit(app.exec_())

# Test function for populating clinic list
def test_populate_clinic_list(setup_ui, qtbot):
    app, ui, mainWindow = setup_ui

    # Mock database handler to return specific clinic names
    ui.db_handler.execute_query = lambda query: [("Clinic A",), ("Clinic B",), ("Clinic C",)]

    # Call the populate_clinic_list method
    ui.populate_clinic_list()

    # Check the number of items in the list widget
    assert ui.listWidget.count() == 3

    # Check the text of each item in the list widget
    assert ui.listWidget.item(0).text() == "Clinic A"
    assert ui.listWidget.item(1).text() == "Clinic B"
    assert ui.listWidget.item(2).text() == "Clinic C"

    # Simulate clicking on the second item in the list widget
    item = ui.listWidget.item(1)
    qtbot.mouseClick(ui.listWidget.viewport(), Qt.LeftButton, pos=ui.listWidget.visualItemRect(item).center())

    # Check if the clicked item is selected
    assert ui.listWidget.currentItem() == item

def test_google_maps_integration(setup_ui, qtbot):
    app, ui, mainWindow = setup_ui

    # Ensure the web engine view is instantiated
    assert isinstance(ui.webEngineView, QWebEngineView)

    # Wait for the web engine view to load the HTML content
    qtbot.waitUntil(lambda: ui.webEngineView.page().url().isValid(), timeout=10000)

    # Check if the URL loaded in the web engine view is valid
    assert ui.webEngineView.page().url().isValid()

def test_view_requests_button(setup_ui, qtbot):
    app, ui, mainWindow = setup_ui

    # Simulate clicking the "View Submitted Requests" button
    qtbot.mouseClick(ui.pushButton_view_requests, Qt.LeftButton)

    # Ensure the ViewRequestsWidget is created and shown
    view_requests_widget = ui.stacked_widget.currentWidget()
    assert isinstance(view_requests_widget, ViewRequestsWidget)


# Mock QApplication exit to prevent actual app exit
@pytest.fixture(autouse=True)
def no_app_exit(monkeypatch):
    monkeypatch.setattr(QApplication, 'exit', lambda *args: None)



