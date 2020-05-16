import sys
from PyQt5 import QtWidgets
from os import path
from qt_designer import *
from style import *
import re
import json


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        # load the icons
        folder = path.dirname(__file__)
        icon_folder = path.join(folder, "icons")

        # check if database exists, if it does open it, else create new empty one
        file_exists = path.isfile(path.join(path.dirname(__file__), "data.json"))
        if file_exists:
            with open("data.json", "r") as json_file:
                self.data = json.load(json_file)
        else:
            self.data = {}

        self.win = Ui_MainWindow()
        self.win.setupUi(self)
        self.setWindowTitle("Login Now!")
        self.setWindowIcon(QtGui.QIcon(path.join(icon_folder, "key.png")))

        # connect all the buttons on diferent pages to functions
        self.win.create_but.clicked.connect(self.create)
        self.win.forgot_but.clicked.connect(self.forgot)
        self.win.back_to_login_but.clicked.connect(self.back_to_login)
        self.win.back_to_login_but_2.clicked.connect(self.back_to_login)
        self.win.back_to_login_but_3.clicked.connect(self.back_to_login)
        self.win.login_but.clicked.connect(self.check_login)
        self.win.register_but.clicked.connect(self.register_user)
        self.win.lost_pass_but.clicked.connect(self.lost_password)

    def back_to_login(self):
        # reset all textboxes when going back to login page
        self.win.reg_email_box.setText("")
        self.win.reg_user_box.setText("")
        self.win.reg_pass_box.setText("")
        self.win.reg_confirm_pass_box.setText("")
        self.win.username_box.setText("")
        self.win.password_box.setText("")
        self.win.lost_email_box.setText("")

        # reset all error messages on all pages
        self.register_user()
        self.check_login()
        self.lost_password()
        self.win.invalid_email.setVisible(False)

        # set the index of the stacked widget back to the login page
        self.win.stackedWidget.setCurrentIndex(0)

    def register_user(self):
        # get all the data user typed in the boxes
        email = self.win.reg_email_box.text()
        user = self.win.reg_user_box.text()
        passw = self.win.reg_pass_box.text()
        passw_confirm = self.win.reg_confirm_pass_box.text()

        # reset error messages for every register attempt
        self.win.invalid_email.setVisible(False)
        self.win.reg_email_box.setStyleSheet("color: black")
        self.win.taken_username.setVisible(False)
        self.win.reg_user_box.setStyleSheet("color: black")
        self.win.invalid_reg_password.setVisible(False)

        # check if it is valid data for registration
        if not email or not user or not passw or not passw_confirm:
            self.win.invalid_email.setText("Fill out all the fields")
            self.win.invalid_email.setVisible(True)
            return None
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.win.invalid_email.setText("Incorrect format for email!")
            self.win.invalid_email.setVisible(True)
            self.win.reg_email_box.setStyleSheet("color: red")
            return None
        for username in self.data:
            if email == self.data[username][0]:
                self.win.invalid_email.setText("Email already taken!")
                self.win.invalid_email.setVisible(True)
                self.win.reg_email_box.setStyleSheet("color: red")
                return None
        if user in self.data:
            self.win.taken_username.setVisible(True)
            self.win.reg_user_box.setStyleSheet("color: red")
            return None
        if len(passw) < 8:
            self.win.invalid_reg_password.setText("Password too short!")
            self.win.invalid_reg_password.setVisible(True)
            return None
        any_digit = any(char.isdigit() for char in passw)
        if not any_digit:
            self.win.invalid_reg_password.setText("Password contains no digits!")
            self.win.invalid_reg_password.setVisible(True)
            return None
        if passw != passw_confirm:
            self.win.invalid_reg_password.setText("Passwords don't match!")
            self.win.invalid_reg_password.setVisible(True)
            return None
        self.data[user] = [email, passw]
        self.win.welcome_user.setText(user)
        self.win.stackedWidget.setCurrentIndex(3)

    def check_login(self):
        user = self.win.username_box.text()
        passw = self.win.password_box.text()

        # reset error messages for every login attempt
        self.win.invalid_user.setVisible(False)
        self.win.invalid_password.setVisible(False)

        if not user:
            return None
        if user not in self.data:
            self.win.invalid_user.setVisible(True)
            self.win.username_box.setStyleSheet("color: red")
            return None
        if passw != self.data[user][1]:
            self.win.invalid_password.setVisible(True)
            self.win.password_box.setStyleSheet("background-color: rgba(255, 0, 0, 0.2)")
            return None
        self.win.welcome_user.setText(user)
        self.win.stackedWidget.setCurrentIndex(3)

    def lost_password(self):
        email = self.win.lost_email_box.text()

        # reset error message
        self.win.invalid_recover_email.setVisible(False)
        self.win.lost_email_box.setStyleSheet("background-color: rgba(240, 240, 240, 0.7)")
        if not email:
            return None
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.win.invalid_recover_email.setText("Incorrect format for email!")
            self.win.invalid_recover_email.setVisible(True)
            self.win.lost_email_box.setStyleSheet("background-color: rgba(255, 0, 0, 0.2)")
            return None
        for user in self.data:
            if self.data[user][0] == email:
                self.win.passw_sent_user.setText(email)
                self.win.stackedWidget.setCurrentIndex(4)
                return None
        self.win.invalid_recover_email.setText("Email not in our database!")
        self.win.invalid_recover_email.setVisible(True)
        self.win.lost_email_box.setStyleSheet("background-color: rgba(255, 0, 0, 0.2)")

    def create(self):
        self.win.stackedWidget.setCurrentIndex(1)

    def forgot(self):
        self.win.stackedWidget.setCurrentIndex(2)

    def closeEvent(self, e):
        # automatically save database on closing the
        with open("data.json", "w") as json_file:
            json.dump(self.data, json_file)
        e.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
