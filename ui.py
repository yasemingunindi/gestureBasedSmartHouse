import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QFrame, QScrollArea, QSlider, QGroupBox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer, QDateTime

class SmartHouseGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.icons_folder = os.path.join(os.path.dirname(__file__), "icons")

        self.setWindowTitle("Smart House Home Page")
        self.setGeometry(100, 100, 800, 600)
        
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        self.create_main_menu()

    def create_main_menu(self):
        main_menu = QWidget()
        layout = QVBoxLayout()
        main_menu.setLayout(layout)

        header_frame = QFrame()
        header_layout = QHBoxLayout()
        header_frame.setLayout(header_layout)

        house_icon_path = os.path.join(self.icons_folder, "house_icon.jpg")
        if os.path.exists(house_icon_path):
            house_pixmap = QPixmap(house_icon_path).scaled(150, 150, Qt.KeepAspectRatio)
            house_icon_label = QLabel()
            house_icon_label.setPixmap(house_pixmap)
            header_layout.addWidget(house_icon_label)

        welcome_label = QLabel("Welcome Home")
        welcome_label.setFont(QFont("Helvetica", 30))
        header_layout.addWidget(welcome_label)

        layout.addWidget(header_frame)

        info_frame = QFrame()
        info_layout = QHBoxLayout()
        info_frame.setLayout(info_layout)

        clock_icon_path = os.path.join(self.icons_folder, "clock_icon.png")
        if os.path.exists(clock_icon_path):
            clock_pixmap = QPixmap(clock_icon_path).scaled(50, 50, Qt.KeepAspectRatio)
            clock_icon_label = QLabel()
            clock_icon_label.setPixmap(clock_pixmap)
            info_layout.addWidget(clock_icon_label)

        self.time_label = QLabel()
        self.time_label.setFont(QFont("Helvetica", 20))
        info_layout.addWidget(self.time_label)
        self.update_time()

        temp_icon_path = os.path.join(self.icons_folder, "temperature_icon.png")
        if os.path.exists(temp_icon_path):
            temp_pixmap = QPixmap(temp_icon_path).scaled(50, 50, Qt.KeepAspectRatio)
            temp_icon_label = QLabel()
            temp_icon_label.setPixmap(temp_pixmap)
            info_layout.addWidget(temp_icon_label)

        temp_label = QLabel("22.5°C")
        temp_label.setFont(QFont("Helvetica", 20))
        info_layout.addWidget(temp_label)

        layout.addWidget(info_frame)

        rooms_button = QPushButton("Rooms")
        rooms_button.setFont(QFont("Helvetica", 24))
        rooms_button.clicked.connect(self.open_room_list)
        layout.addWidget(rooms_button)

        self.stack.addWidget(main_menu)
        self.stack.setCurrentWidget(main_menu)

    def update_time(self):
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.time_label.setText(current_time)

        # Update the time every second
        QTimer.singleShot(1000, self.update_time)

    def open_room_list(self):
        room_list = QWidget()
        layout = QVBoxLayout()
        room_list.setLayout(layout)

        header_frame = QFrame()
        header_layout = QHBoxLayout()
        header_frame.setLayout(header_layout)

        back_button = QPushButton("⬅")
        back_button.setFont(QFont("Helvetica", 18))
        back_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        header_layout.addWidget(back_button)

        title_label = QLabel("Rooms")
        title_label.setFont(QFont("Helvetica", 30))
        header_layout.addWidget(title_label)

        layout.addWidget(header_frame)

        scroll_area = QScrollArea()
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_content.setLayout(scroll_layout)

        rooms = ["Bedroom", "Living Room", "Kitchen", "Bathroom", "Office"]

        for room in rooms:
            room_button = QPushButton(room)
            room_button.setFont(QFont("Helvetica", 16))
            room_button.clicked.connect(lambda checked, room=room: self.open_room_controls(room))
            scroll_layout.addWidget(room_button)

        scroll_area.setWidget(scroll_content)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        self.stack.addWidget(room_list)
        self.stack.setCurrentWidget(room_list)

    def open_room_controls(self, room_name):
        room_controls = QWidget()
        layout = QVBoxLayout()
        room_controls.setLayout(layout)

        header_frame = QFrame()
        header_layout = QHBoxLayout()
        header_frame.setLayout(header_layout)

        back_button = QPushButton("⬅")
        back_button.setFont(QFont("Helvetica", 18))
        back_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        header_layout.addWidget(back_button)

        title_label = QLabel(f"{room_name} Controls")
        title_label.setFont(QFont("Helvetica", 30))
        header_layout.addWidget(title_label)

        layout.addWidget(header_frame)

        controls_label = QLabel(f"Controls for {room_name} will be added here.")
        controls_label.setFont(QFont("Helvetica", 20))
        layout.addWidget(controls_label)

        self.stack.addWidget(room_controls)
        self.stack.setCurrentWidget(room_controls)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartHouseGUI()
    window.show()
    sys.exit(app.exec_())
