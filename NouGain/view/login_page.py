from PyQt5 import QtWidgets, QtGui, QtCore

class LoginPage(QtWidgets.QWidget):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 800, 600)

        self.login_layout = QtWidgets.QVBoxLayout(self)

        self.background_label = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("assets/Marché.jpg")
        scaled_pixmap = self.pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        self.background_label.setPixmap(scaled_pixmap)
        self.background_label.setScaledContents(True)

        self.overlay_layout = QtWidgets.QVBoxLayout()
        self.overlay_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.login_label = QtWidgets.QLabel('E-Mail:')
        self.login_label.setStyleSheet("color: black;")

        self.login_input = QtWidgets.QLineEdit()
        self.login_input.setFixedSize(200, 30)

        self.password_label = QtWidgets.QLabel('Mot de passe:')
        self.password_label.setStyleSheet("color: black;")

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setFixedSize(200, 30)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.login_button = QtWidgets.QPushButton('Login')
        self.login_button.setFixedSize(200, 50)
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 10px;")
        self.login_button.clicked.connect(self.handle_login)

        self.error_label = QtWidgets.QLabel('')
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)

        self.overlay_layout.addWidget(self.login_label)
        self.overlay_layout.addWidget(self.login_input)
        self.overlay_layout.addWidget(self.password_label)
        self.overlay_layout.addWidget(self.password_input)
        self.overlay_layout.addWidget(self.error_label)
        self.overlay_layout.addWidget(self.login_button)

        self.overlay_widget = QtWidgets.QWidget(self)
        self.overlay_widget.setLayout(self.overlay_layout)
        self.overlay_widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.login_layout.addWidget(self.background_label)
        self.login_layout.addWidget(self.overlay_widget)

        self.setLayout(self.login_layout)
        self.login_layout.setContentsMargins(0, 0, 0, 0)
        self.login_layout.setAlignment(self.overlay_widget, QtCore.Qt.AlignCenter)

        self.show()

    def handle_login(self):
        email = self.login_input.text()
        password = self.password_input.text()

        if self.authenticate(email, password):
            self.error_label.setText('')
            self.login_input.setStyleSheet('')
            self.password_input.setStyleSheet('')
        else:
            self.error_label.setText('Adresse mail ou Mot de passe incorrect')
            self.login_input.setStyleSheet('border: 1px solid red')
            self.password_input.setStyleSheet('border: 1px solid red')

    def authenticate(self, email, password):
        return email == "user@example.com" and password == "password"

    def reset_login_fields(self):
        self.error_label.setText('')
        self.login_input.setStyleSheet('')
        self.password_input.setStyleSheet('')
        self.login_input.clear()
        self.password_input.clear()
