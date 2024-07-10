from PyQt5 import QtWidgets, QtCore, QtGui

class HomePage(QtWidgets.QWidget):
    def __init__(self):
        super(HomePage, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.home_layout = QtWidgets.QVBoxLayout(self)

        self.background_label = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("assets/Marché.jpg")

        scaled_pixmap = self.pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        self.background_label.setPixmap(scaled_pixmap)
        self.background_label.setScaledContents(True)

        self.overlay_layout = QtWidgets.QVBoxLayout()
        self.overlay_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.home_title = QtWidgets.QLabel('Nou\'Gain')
        self.home_title.setAlignment(QtCore.Qt.AlignCenter)
        self.home_title.setFont(QtGui.QFont("Arial", 24, QtGui.QFont.Bold))
        self.home_title.setStyleSheet("color: black;")

        self.home_button = QtWidgets.QPushButton('Connectez vous')
        self.home_button.setFont(QtGui.QFont("Arial", 14))
        self.home_button.setFixedSize(200, 50)
        self.home_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")

        self.create_account_button = QtWidgets.QPushButton('Créer un compte')
        self.create_account_button.setFont(QtGui.QFont("Arial", 14))
        self.create_account_button.setFixedSize(200, 50)
        self.create_account_button.setStyleSheet("background-color: #2196F3; color: white; border-radius: 10px;")

        self.overlay_layout.addWidget(self.home_title)
        self.overlay_layout.addWidget(self.home_button)
        self.overlay_layout.addWidget(self.create_account_button)

        self.overlay_widget = QtWidgets.QWidget(self)
        self.overlay_widget.setLayout(self.overlay_layout)
        self.overlay_widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.home_layout.addWidget(self.background_label)
        self.home_layout.addWidget(self.overlay_widget)

        self.setLayout(self.home_layout)
        self.home_layout.setContentsMargins(0, 0, 0, 0)
        self.home_layout.setAlignment(self.overlay_widget, QtCore.Qt.AlignCenter)
