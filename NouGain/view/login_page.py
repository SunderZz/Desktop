from PyQt5 import QtWidgets, QtGui, QtCore

class LoginPage(QtWidgets.QWidget):
    def __init__(self):
        super(LoginPage, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.login_layout = QtWidgets.QVBoxLayout()
        self.login_layout.setSpacing(10)

        self.login_label = QtWidgets.QLabel('Mail:')
        self.login_input = QtWidgets.QLineEdit()
        self.password_label = QtWidgets.QLabel('Password:')
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.login_button = QtWidgets.QPushButton('Login')
        self.login_button.clicked.connect(self.handle_login)

        self.error_label = QtWidgets.QLabel('')
        self.error_label.setStyleSheet("color: red")
        self.error_label.setAlignment(QtCore.Qt.AlignCenter)

        self.login_layout.addWidget(self.login_label)
        self.login_layout.addWidget(self.login_input)
        self.login_layout.addWidget(self.password_label)
        self.login_layout.addWidget(self.password_input)
        self.login_layout.addWidget(self.error_label)
        self.login_layout.addWidget(self.login_button)

        self.setLayout(self.login_layout)

    def handle_login(self):
        email = self.login_input.text()
        password = self.password_input.text()
        
        if self.authenticate(email, password):
            self.error_label.setText('')
            self.login_input.setStyleSheet('')
            self.password_input.setStyleSheet('')
        else:
            self.error_label.setText('Incorrect password.')
            self.login_input.setStyleSheet('border: 1px solid red')
            self.password_input.setStyleSheet('border: 1px solid red')

    def authenticate(self, email, password):
        return email == "user@example.com" and password == "password"

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_page = LoginPage()
    login_page.show()
    sys.exit(app.exec_())
