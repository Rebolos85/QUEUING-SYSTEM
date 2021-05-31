import queue
import re
import sys
import time
from tkinter import Image, PhotoImage, Label, messagebox

import bcrypt
import mysql.connector
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer, QTime, QSortFilterProxyModel
from PyQt5.QtGui import QPixmap, QStandardItem
from PyQt5.QtWidgets import QDialog, QApplication, QLabel, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QHeaderView
import tkinter
import tkinter.messagebox

from mysql.connector import IntegrityError

from message.MessageToUSER import checkErrorRegister, validateUserCancelButton, successfullyRegisterUserMessage, \
    errorMessageForPasswordDoesntMatch, noAccountFoundInDatabase, duplicateEntryForUsername, inputAllTheFields, \
    errorFieldAppointment, feedbackUserDuplicatePriorityNumber, checkInputFields, guestCodeFeedback, \
    guestSuccessfullyFeedback, successfullyFacultyRequest
from mydatabse.MyDatabaseQuery import insertSuccessfullyRegisterStudent, mydb, insertStudentAppointment, \
    insertSuccessLogBookRegister
from validateInput.Validator import isValidSchoolId, isValidUsernameInput, isValidEmail, isValidCompleteName, \
    isValidFirstNameAndLastname, isValidSuffixes, isValidGmailAccount

from datetime import date

from datetime import datetime

fifo = queue.Queue()
finalFifo = queue.Queue()


class LoginStudentForm(QDialog):
    def __init__(self):
        super(LoginStudentForm, self).__init__()
        loadUi('GeneralLoginForm.ui', self)
        self.attachListenersToWidgets()

    def attachListenersToWidgets(self):

        self.usernameTextField_2.returnPressed.connect(self.validateLengthOfTextFields)
        self.usernameTextField_2.editingFinished.connect(self.validateLengthOfTextFields)
        self.usernameTextField_2.textChanged.connect(self.validateLengthOfTextFields)
        self.loginButton_2.clicked.connect(self.verifyUsernameAndPasswordOnceLoginClick)
        self.loginButton_2.setEnabled(False)
        self.passwordTextField_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registerButton_2.clicked.connect(self.goToRegistrationForm)
        self.outsiderStudent_2.clicked.connect(self.goToLoginGuestRegistration)


    def goToLoginGuestRegistration(self):
        guestRegitration = GuestLogbookRegistration()
        widget.addWidget(guestRegitration)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def validateLengthOfTextFields(self):
        usernameInput = self.usernameTextField_2.text()
        passwordInput = self.passwordTextField_2.text()

        if usernameInput == "" and passwordInput == "":
            self.loginButton_2.setEnabled(False)
        else:
            self.loginButton_2.setEnabled(True)

    def pop_message(self, text=""):
        msg = QtWidgets.QMessageBox()

        msg.setText("{}".format(text))
        msg.exec_()

    def goToRegistrationForm(self):
        registration = RegistrationForm()
        widget.addWidget(registration)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def verifyUsernameAndPasswordOnceLoginClick(self):
        print("fafafa")
        usernameInput = self.usernameTextField_2.text()
        passwordInput = self.passwordTextField_2.text()

        self.authenticationloginAccounts(usernameInput, passwordInput)

    def authenticationloginAccounts(self, usernameInput, passwordGeneralInput):
        loadpass = "SELECT student_password FROM studentaccount WHERE username = %s"

        mycursor = mydb.cursor()
        # mycursor.execute('SELECT * FROM studentaccount WHERE username = %s AND password = %s', (username, password,))
        # account = mycursor.fetchone()
        # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        passwordInput = passwordGeneralInput.encode("UTF-8")

        mycursor.execute(loadpass, (usernameInput,))
        loginpasswordCheck = mycursor.fetchone()

        retrieveDataFACULTY = "SELECT password FROM faculty_account WHERE email = %s"
        mycursor = mydb.cursor()
        mycursor.execute(retrieveDataFACULTY, (usernameInput,))
        passwordFaculty = passwordGeneralInput.encode("UTF-8")
        loginFacultyPassword = mycursor.fetchone()

        # Checking if the loginpasswordCheck will retrieve not none
        if loginpasswordCheck is not None:
            # Re-assigning the username in order to have encode function
            usernameCheck = loginpasswordCheck[0]

            # Checking passowrd and stored password in db
            if bcrypt.checkpw(passwordInput, usernameCheck.encode("UTF-8")):

                self.goToAppointment()
                # self.appointmentFrame = SetAppointment()
                #
                # self.appointmentFrame.show()

                # appointmentFrame()

            else:
                errorMessageForPasswordDoesntMatch()

                # Display error message if the password user input doesn't match in database
                # errorMessageForPasswordDoesntMatch()

        elif loginFacultyPassword is not None:
            passwordAccount = loginFacultyPassword[0]

            if bcrypt.checkpw(passwordFaculty, passwordAccount.encode("UTF-8")):
                successfullyFacultyRequest()

            else:
                errorMessageForPasswordDoesntMatch()


        else:
            # Display error message if password and username doesn't match
            noAccountFoundInDatabase()

    # class SetAppointment(QMainWindow):
    #     def __init__(self):
    #         QMainWindow.__init__(self)
    #         self.ui = MainAppointmentFinal()
    #         self.ui.setupUi(self)
    def goToAppointment(self):
        appointment = SetAppointment()
        widget.addWidget(appointment)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    # def guestLogbookFACULTY(self):
    #     guestFaculty = GuestFunction()
    #     widget.addWidget(guestFaculty)
    #     widget.setCurrentIndex(widget.currentIndex() + 1)

class RegistrationForm(QDialog):
    def __init__(self):
        super(RegistrationForm, self).__init__()
        loadUi('StudentRegistrationForm.ui', self)
        self.allEventListeners()

    def allEventListeners(self):
        self.submitButtonRegister.clicked.connect(self.feedbackOnceUserClickRegister)
        self.usernameTextField.returnPressed.connect(self.validateStudentPersonalInformation)
        self.usernameTextField.editingFinished.connect(self.validateStudentPersonalInformation)
        self.usernameTextField.textChanged.connect(self.validateStudentPersonalInformation)
        self.schoolIdTextField.returnPressed.connect(self.validateStudentPersonalInformation)
        self.schoolIdTextField.editingFinished.connect(self.validateStudentPersonalInformation)
        self.schoolIdTextField.textChanged.connect(self.validateStudentPersonalInformation)
        self.schoolEmailTextField.returnPressed.connect(self.validateStudentPersonalInformation)
        self.schoolEmailTextField.editingFinished.connect(self.validateStudentPersonalInformation)
        self.schoolEmailTextField.textChanged.connect(self.validateStudentPersonalInformation)
        self.firstPasswordField_2.returnPressed.connect(self.validateStudentPersonalInformation)
        self.firstPasswordField_2.editingFinished.connect(self.validateStudentPersonalInformation)
        self.firstPasswordField_2.textChanged.connect(self.validateStudentPersonalInformation)
        self.secondPasswordField.returnPressed.connect(self.validateStudentPersonalInformation)
        self.secondPasswordField.editingFinished.connect(self.validateStudentPersonalInformation)
        self.secondPasswordField.textChanged.connect(self.validateStudentPersonalInformation)
        # self.yearLevelChoices.currentIndex.connect(self.createAccount)
        self.yearLevelChoices.currentIndexChanged.connect(self.choicesComboBoxForYearLevel)
        self.comboBoxCourseChoices.currentIndexChanged.connect(self.userChoicesForCourse)
        self.cancelButton.clicked.connect(self.askUserToCancelButton)
        self.submitButtonRegister.setEnabled(False)
        self.goBackToLogin_2.clicked.connect(self.goBackToLogin)

    hasValidUsername = False
    hasValidSchoolId = False
    hasValidGmail = False
    hasChooseYearLevel = False
    hasChooseCourse = False


    def goBackToLogin(self):
        loginForm = LoginStudentForm()
        widget.addWidget(loginForm)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def validateStudentPersonalInformation(self):
        schoolEmail = self.schoolEmailTextField.text()
        schoolId = self.schoolIdTextField.text()
        mydb = mysql.connector.connect(host="localhost", user="root", password="Rebolos143#",
                                       database="cc15finalproject")
        # mycursor = mydb.cursor()
        loadSchoolId = "SELECT studentSchoolID FROM studentpreviousaccount WHERE studentSchoolID = %s"
        loadSchoolEmail = "SELECT studentSchoolID FROM studentpreviousaccount WHERE student_email = %s"

        # myCursorSchoolId = mydb.cursor()
        # myCursorSchoolId.execute(loadSchoolId, (schoolId,))
        # myCursorSchoolEmail = mydb.cursor()
        # myCursorSchoolEmail.execute(loadSchoolEmail, (email,))
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(loadSchoolId, (schoolId,))
        mycursor2 = mydb.cursor(buffered=True)
        mycursor2.execute(loadSchoolEmail, (schoolEmail,))
        # mycursor.execute(loadSchoolEmail, (schoolEmail,))

        verifySchoolId = mycursor.fetchone()
        verifySchoolEmail = mycursor2.fetchone()
        mycursor.execute(loadSchoolEmail, (loadSchoolEmail,))

        # myCursorSchoolEmail =mycursor.fetchone()

        global hasValidUsername
        global hasValidSchoolId
        global hasValidGmail

        settingBorderToWrongInput = "QLineEdit { border : 2px solid red;}"
        settingGoodCorrectInputPassword = "QLineEdit { border : 2px solid #39ccb1;}"
        settingToNormalField = "QLineEdit {}"
        username = self.usernameTextField.text()
        schoolEmail = self.schoolEmailTextField.text()
        # schoolId = self.schoolIdTextField.text()
        self.secondPasswordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.firstPasswordField_2.setEchoMode(QtWidgets.QLineEdit.Password)
        # schoolEmail = self.schoolEmailTextField.text()
        firstPassword = self.firstPasswordField_2.text()
        # schoolIdLength = len(schoolId)
        secondPassword = self.secondPasswordField.text()
        schoolIdLength = len(schoolId)
        schoolEmailLength = len(schoolEmail)
        processedUsername = username.strip()
        # verifyEmailAndEmailId(schoolId,schoolEmail)
        usernamelength = len(processedUsername)
        # courseAndYear = self.comboBoxCourseChoices.itemText(self.comboBoxCourseChoices.currentIndex())
        # yearLevel =
        firstPasswordLength = len(firstPassword)
        secondPasswordLength = len(secondPassword)
        courseAndYear = self.comboBoxCourseChoices.itemText(self.comboBoxCourseChoices.currentIndex())
        hasChoosenYear = self.yearLevelChoices.itemText(self.yearLevelChoices.currentIndex())
        # verifyEmailAndEmailId(schoolId, schoolEmail)

        if isValidUsernameInput(processedUsername):

            self.usernameTextField.setStyleSheet(settingGoodCorrectInputPassword)
            hasValidUsername = True
            self.studentUsernameFeedback.setText("")

        elif processedUsername == "":
            self.usernameTextField.setStyleSheet('QLineEdit { border : 1px black;')
        else:

            self.usernameTextField.setStyleSheet(settingBorderToWrongInput)
            hasValidUsername = False

        if verifySchoolId and isValidSchoolId(schoolId):

            self.schoolIdTextField.setStyleSheet(settingGoodCorrectInputPassword)
            hasValidSchoolId = True
            self.schoolIDFeedBack.setText("")

        elif schoolId == '':

            self.schoolIdTextField.setStyleSheet('QLineEdit { border : 1px black;')
        elif schoolIdLength >= 12 or schoolIdLength == 1:
            hasValidSchoolId = False
            # print('gana na')
            self.schoolIdTextField.setStyleSheet(settingBorderToWrongInput)

        else:
            hasValidSchoolId = False
            print("YAWA GANA NA312312")
            self.schoolIdTextField.setStyleSheet(settingBorderToWrongInput)

        if verifySchoolEmail and isValidEmail(schoolEmail):
            self.schoolEmailTextField.setStyleSheet(settingGoodCorrectInputPassword)
            hasValidGmail = True
            self.schoolEmailFeedback.setText("")
        elif schoolEmail == '':
            self.schoolEmailTextField.setStyleSheet('QLineEdit { border : 1px black;')
        else:
            self.schoolEmailTextField.setStyleSheet(settingBorderToWrongInput)
            hasValidGmail = False

        if usernamelength == 0 and schoolIdLength == 0 and schoolEmailLength == 0 and firstPasswordLength == 0 and secondPasswordLength == 0:
            self.submitButtonRegister.setEnabled(False)

        else:
            self.submitButtonRegister.setEnabled(True)

        if schoolEmail == " " or schoolId == " " or username == " " or firstPassword == "" or secondPassword == " ":
            self.submitButtonRegister.setEnabled(False)
        else:

            self.submitButtonRegister.setEnabled(True)
        self.validatePasswordUserInput()
        # self.printHelloWorld()
        # if firstPassword == secondPassword and
        lowerPasswordInput = self.validateLowerInputPassword()
        capitalLetterPassword = self.validateCapitalInputPassword()
        digitInputPassword = self.validateDigitInputInPassword()
        requiredSpecialCharacter = self.specialCharacterValidation(firstPassword)

    def choicesComboBoxForYearLevel(self):
        global hasChooseYearLevel
        hasChoosenYear = self.yearLevelChoices.itemText(self.yearLevelChoices.currentIndex())
        if hasChoosenYear == "First Year" or hasChoosenYear == 'Second Year' or hasChoosenYear == 'Third Year' or hasChoosenYear == 'Fourth Year' or hasChooseYearLevel:
            hasChooseYearLevel = True
            self.yearLevelChoices.setStyleSheet("font: 14px bold;\n"
                                                "border-style:outset;\n"
                                                "border-width:2px; \n"
                                                "border-radius:8px;\n"
                                                "border-color: #39ccb1;\n"
                                                )
        else:
            self.submitButtonRegister.setEnabled(False)
            hasChooseYearLevel = False

    # hasChooseCourse = False

    def userChoicesForCourse(self):
        global hasChooseCourse

        courseAndYear = self.comboBoxCourseChoices.itemText(self.comboBoxCourseChoices.currentIndex())
        if courseAndYear == "BSCS" or courseAndYear == "BSIS" or courseAndYear == "BSIT":

            hasChooseCourse = True
            self.comboBoxCourseChoices.setStyleSheet("font: 14px bold;\n"
                                                     "border-style:outset;\n"
                                                     "border-width:2px; \n"
                                                     "border-radius:8px;\n"
                                                     "border-color: #39ccb1;\n"
                                                     )

        else:
            hasChooseCourse = False
            self.comboBoxCourseChoices.setStyleSheet("font: 14px bold;\n"
                                                     "border-style:outset;\n"
                                                     "border-width:2px; \n"
                                                     "border-radius:8px;\n"
                                                     "border-color: red;\n"
                                                     )
            self.submitButtonRegister.setEnabled(False)

    hasDidnotChooseCourse = False
    hasChooseBSIT = False
    hasChooseBSCS = False
    hasChooseBSIS = False

    # def pop_message(self, text=""):
    #     msg = QtWidgets.QMessageBox()
    #     msg.setText("{}".format(text))
    #     msg.exec_()

    def validateLowerInputPassword(self):
        firstPassword = self.firstPasswordField_2.text()
        secondPassword = self.secondPasswordField.text()
        lowerPasswordInput = any(
            eachCharacterInputUser.islower() for eachCharacterInputUser in
            firstPassword or secondPassword)
        return lowerPasswordInput

    def validateCapitalInputPassword(self):
        firstPassword = self.firstPasswordField_2.text()
        secondPassword = self.secondPasswordField.text()
        capitalCasePasswordInput = any(
            eachCharacterInputUser.isupper() for eachCharacterInputUser in
            firstPassword or secondPassword)

        return capitalCasePasswordInput

    def validateDigitInputInPassword(self):
        firstPassword = self.firstPasswordField_2.text()
        secondPassword = self.secondPasswordField.text()
        digitPasswordInput = any(
            eachCharacterInputUser.isdigit() for eachCharacterInputUser in
            firstPassword)
        return digitPasswordInput

    def specialCharacterValidation(self, password):
        patternRegex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]$')
        # REGEX_FOR_SPECIAL_CHARACTERS = self.firstPasswordField.text()
        validatePasswordSpecialCharacters = re.search(patternRegex, password)

        if validatePasswordSpecialCharacters:
            return validatePasswordSpecialCharacters

    def validateLowerInputSecondPassword(self):

        secondPassword = self.secondPasswordField.text()
        lowerPasswordInput = any(
            eachCharacterInputUser.islower() for eachCharacterInputUser in
            secondPassword)
        return lowerPasswordInput

    def validateCapitalInputSecondPassword(self):
        firstPassword = self.firstPasswordField_2.text()
        secondPassword = self.secondPasswordField.text()
        capitalCasePasswordInput = any(
            eachCharacterInputUser.isupper() for eachCharacterInputUser in
            secondPassword)

        return capitalCasePasswordInput

    def validateDigitInputInSecondPassword(self):
        firstPassword = self.firstPasswordField_2.text()
        secondPassword = self.secondPasswordField.text()
        digitPasswordInput = any(
            eachCharacterInputUser.islower() for eachCharacterInputUser in
            secondPassword)
        return digitPasswordInput

    # def specialCharacterValidationSecondPassword(self, password):
    #     patternRegex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]$')
    #     # REGEX_FOR_SPECIAL_CHARACTERS = self.firstPasswordField.text()
    #     validatePasswordSpecialCharacters = re.search(patternRegex, password)
    #
    #     if validatePasswordSpecialCharacters:
    #         return validatePasswordSpecialCharacters
    def validateSpecialCharactersSecondPassword(self, hasSpecialCharacter):
        secondPassword = self.secondPasswordField.text()
        pattern = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')

        if pattern.search(secondPassword):
            hasSpecialCharacter = True

        else:
            hasSpecialCharacter = False
            self.requirementsPassword_4.setText("Too weak")
            self.requirementsPassword_4.setStyleSheet("color:red;\n"
                                                      "\n"
                                                      "font: 12px bold;")
            self.firstPasswordField_2.setStyleSheet('border:2px solid red;')

            # print('NO SPECIAL CAHRACTER')

        return hasSpecialCharacter

    def validateSpecialCharactersFirstPassword(self, ):
        firstPassword = self.firstPasswordField_2.text()
        pattern = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]')
        validateDigit = self.validateDigitInputInPassword()
        if pattern.search(firstPassword):
            hasSpecialCharacterInFirstPassword = True

            if validateDigit:
                self.specialCharactersLabel_3.setPixmap(QtGui.QPixmap("res/checkIcon.png"))

        else:
            hasSpecialCharacterInFirstPassword = False
            self.requirementsPassword_4.setText("Too weak")
            self.requirementsPassword_4.setStyleSheet("color:red;\n"
                                                      "\n"
                                                      "font: 12px bold;")
            self.firstPasswordField_2.setStyleSheet('border:2px solid red;')

            # print('NO SPECIAL CAHRACTER')

        return hasSpecialCharacterInFirstPassword

    def validatePasswordUserInput(self):
        hasSpecialCharacter = True
        firstPassword = self.firstPasswordField_2.text()
        firstPasswordLength = len(firstPassword)
        hasSpecialCharacterInFirstPassword = True
        lowerPasswordInput = self.validateLowerInputPassword()
        capitalLetterPassword = self.validateCapitalInputPassword()
        digitInputPassword = self.validateDigitInputInPassword()
        specialCharacterInFirstPassword = self.validateSpecialCharactersFirstPassword()
        specialCharacterInSecondPassword = self.validateSpecialCharactersSecondPassword(hasSpecialCharacter)
        secondPassword = self.secondPasswordField.text()
        secondPasswowrdLength = len(secondPassword)
        eightCharacterPassword = (lowerPasswordInput and capitalLetterPassword) and (
                digitInputPassword and specialCharacterInFirstPassword) and (
                                         firstPasswordLength == 8 or firstPasswordLength == 9 or firstPasswordLength == 10 or firstPasswordLength == 11)

        lessthanEightCharacters = (lowerPasswordInput and capitalLetterPassword) or (
                digitInputPassword and specialCharacterInFirstPassword) and (
                                          firstPasswordLength <= 7)

        moreSecurePassword = (lowerPasswordInput and capitalLetterPassword) and (
                digitInputPassword and specialCharacterInFirstPassword) and (
                                     firstPasswordLength >= 12)

        hasCapitalAndLower = lowerPasswordInput and capitalLetterPassword
        hasDigitAndSpecialCharacter = digitInputPassword and specialCharacterInFirstPassword
        lowerSecondPasswordInput = self.validateLowerInputSecondPassword()
        capitalSecondPasswordInput = self.validateCapitalInputSecondPassword()
        digitInSecondPasswordInput = self.validateDigitInputInPassword()

        lessthanEightCharactersSecondPassword = (lowerSecondPasswordInput and capitalSecondPasswordInput) and (
                digitInSecondPasswordInput and specialCharacterInSecondPassword) and secondPasswowrdLength <= 7
        eightCharactersInSecondPassword = (lowerSecondPasswordInput and capitalSecondPasswordInput) and (
                digitInSecondPasswordInput and specialCharacterInSecondPassword)
        moreSecureSecondPassword = (lowerSecondPasswordInput and capitalSecondPasswordInput) and (
                digitInSecondPasswordInput and specialCharacterInSecondPassword)
        hasNoDigit = False
        hasNoCapital = False
        hasNoSpecialCharacter = False
        hasNoLowerCase = False
        settingBorderToWrongInput = "QLineEdit {}"

        self.dontHaveCapitalLetter(hasNoCapital)

        self.donotHaveDigitCharacterInPassword(hasNoDigit)

        self.dontHaveDigitInDigitSecondPassword(hasNoDigit, secondPassword)
        self.dontHaveLowerCaseInSecondPassword(hasNoLowerCase, secondPassword)
        self.dontHaveSpecialCharacterInPassword(hasNoSpecialCharacter, secondPassword)
        self.dontHaveUpperCaseInSecondPassword(hasNoCapital, secondPassword)

        if firstPasswordLength == 8:
            self.eightCharactersLabel_3.setPixmap(QtGui.QPixmap("res/checkIcon.png"))

        if hasDigitAndSpecialCharacter:
            self.specialCharactersLabel_3.setPixmap(QtGui.QPixmap("res/checkIcon.png"))
        if hasCapitalAndLower:
            self.capitalCaseLbel_3.setPixmap(QtGui.QPixmap("res/checkIcon.png"))

        if lessthanEightCharacters:
            self.requirementsPassword_4.setText("Too weak")
            self.requirementsPassword_4.setStyleSheet("color:red;\n"
                                                      "\n"
                                                      "font: 12px bold;")
            self.firstPasswordField_2.setStyleSheet('border:2px solid red;')

        if eightCharacterPassword:
            # print('31232131')
            self.requirementsPassword_4.setText("Okay")
            self.requirementsPassword_4.setStyleSheet("color:#e59700;\n"
                                                      "\n"
                                                      "font: 12px bold;")
            self.firstPasswordField_2.setStyleSheet('border:2px solid #e59700;')
            self.eightCharactersLabel_3.setPixmap(QtGui.QPixmap("res/checkIcon.png"))
            self.capitalCaseLbel_3.setPixmap(QtGui.QPixmap("res/checkIcon.png"))
            self.specialCharactersLabel_3.setPixmap(QtGui.QPixmap("res/checkIcon.png"))
        if moreSecurePassword:
            self.requirementsPassword_4.setText("Great")
            self.requirementsPassword_4.setStyleSheet("color:#39ccb1;\n"
                                                      "\n"
                                                      "font: 12px bold;")
            self.firstPasswordField_2.setStyleSheet('border:2px solid #39ccb1;')
            self.eightCharactersLabel_3.setPixmap(QtGui.QPixmap('res/checkIcon.png'))
            self.capitalCaseLbel_3.setPixmap(QtGui.QPixmap("res/checkIcon.png"))
            self.specialCharactersLabel_3.setPixmap(QtGui.QPixmap('res/checkIcon.png'))

        if lessthanEightCharactersSecondPassword:
            self.secondPasswordField.setStyleSheet('border:2px solid red;')

        if eightCharactersInSecondPassword and (
                secondPasswowrdLength == 8 or secondPasswowrdLength == 9 or secondPasswowrdLength == 10 or secondPasswowrdLength == 11):
            # print('Gana na')
            # self.secondPasswordField.setStyleSheet('border:2px #e59700;')
            self.secondPasswordField.setStyleSheet('border:2px solid #e59700;')

        if moreSecureSecondPassword and secondPasswowrdLength >= 12:
            self.secondPasswordField.setStyleSheet('border:2px solid #39ccb1;')

        if firstPassword == "":
            self.requirementsPassword_4.setText("")
            self.firstPasswordField_2.setStyleSheet(settingBorderToWrongInput)
            self.eightCharactersLabel_3.setPixmap(QtGui.QPixmap('res/Close-icon.png'))
            self.capitalCaseLbel_3.setPixmap(QtGui.QPixmap("res/Close-icon.png"))
            self.specialCharactersLabel_3.setPixmap(QtGui.QPixmap('res/Close-icon.png'))
        if secondPassword == "":
            self.secondPasswordField.setStyleSheet(settingBorderToWrongInput)

    def donotHaveDigitCharacterInPassword(self, hasNoDigit):
        firstPassword = self.firstPasswordField_2.text()

        if not any(eachCharacter.isdigit() for eachCharacter in firstPassword):
            hasNoDigit = False
        self.requirementsPassword_4.setText("Too weak")
        self.requirementsPassword_4.setStyleSheet("color:red;\n"
                                                  "\n"
                                                  "font: 12px bold;")
        self.firstPasswordField_2.setStyleSheet('border:2px solid red;')

        return hasNoDigit

    def dontHaveCapitalLetter(self, hasNoCapital):
        firstPassword = self.firstPasswordField_2.text()
        if not any(eachCharacter.isupper() for eachCharacter in firstPassword):
            hasNoCapital = False
            self.requirementsPassword_4.setText("Too weak")
            self.requirementsPassword_4.setStyleSheet("color:red;\n"
                                                      "\n"
                                                      "font: 12px bold;")
            self.firstPasswordField_2.setStyleSheet('border:2px solid red;')
        return hasNoCapital

    def validateSpecialCharacters(self, has_no_special_character, firstPassword):

        pattern = re.compile(r'^[^<>{}\"/|;:.,~!?@#$%^=&123*\\]\\\\()\\[¿§«»ω⊙¤°℃℉€¥£¢¡®©0-9_+]*$')

        if pattern.search(firstPassword):
            has_no_special_character = True

        else:
            has_no_special_character = False
            self.requirementsPassword_4.setText("Too weak")
            self.requirementsPassword_4.setStyleSheet("color:red;\n"
                                                      "\n"
                                                      "font: 12px bold;")
            self.firstPasswordField_2.setStyleSheet('border:2px solid red;')

            # print('NO SPECIAL CAHRACTER')

        return has_no_special_character

    def dontHaveLowerCase(self, hasNoLowerCase):
        firstPassword = self.firstPasswordField_2.text()
        if not any(eachCharacter.islower() for eachCharacter in firstPassword):
            self.requirementsPassword_4.setText("Too weak")
            self.requirementsPassword_4.setStyleSheet("color:red;\n"
                                                      "\n"
                                                      "font: 12px bold;")
            self.firstPasswordField_2.setStyleSheet('border:2px solid red;')

            hasNoLowerCase = False
        return hasNoLowerCase

    def dontHaveLowerCaseInSecondPassword(self, hasNoLowerCase, secondPassword):
        if not any(eachCharacter.islower() for eachCharacter in secondPassword):
            self.secondPasswordField.setStyleSheet("color:red;\n"
                                                   "\n"
                                                   "font: 12px bold;")
            self.secondPasswordField.setStyleSheet('border:2px solid red;')

            hasNoLowerCase = False
        return hasNoLowerCase

    def dontHaveUpperCaseInSecondPassword(self, hasNoUpperCase, secondPassword):

        if not any(eachCharacter.isupper() for eachCharacter in secondPassword):
            hasNoUpperCase = False

            self.secondPasswordField.setStyleSheet("color:red;\n"
                                                   "\n"
                                                   "font: 12px bold;")
            self.secondPasswordField.setStyleSheet('border:2px solid red;')
        return hasNoUpperCase

    def dontHaveSpecialCharacterInPassword(self, hasNoSpecialCharacter, secondPassword):
        pattern = re.compile(r'^[^<>{}\"/|;:.,~!?@#$%^=&123*\\]\\\\()\\[¿§«»ω⊙¤°℃℉€¥£¢¡®©0-9_+]*$')

        if pattern.search(secondPassword):
            hasNoSpecialCharacter = True

        else:
            print('hello')
            hasNoSpecialCharacter = False

            self.secondPasswordField.setStyleSheet("color:red;\n"
                                                   "\n"
                                                   "font: 12px bold;")
            self.secondPasswordField.setStyleSheet('border:2px solid red;')

        return hasNoSpecialCharacter

    def dontHaveDigitInDigitSecondPassword(self, hasNoDigitInSecondPassword, secondPassword):
        if not any(eachCharacter.isdigit() for eachCharacter in secondPassword):
            hasNoDigitInSecondPassword = False

            self.secondPasswordField.setStyleSheet("color:red;\n"
                                                   "\n"
                                                   "font: 12px bold;")
            self.secondPasswordField.setStyleSheet('border:2px solid red;')

        return hasNoDigitInSecondPassword

    def askUserToCancelButton(self):
        validateUserCancelButton()

    def feedbackOnceUserClickRegister(self):
        # global hasDidnotChooseCourse

        global hasValidUsername
        global hasValidSchoolId
        global hasValidGmail

        hasDidnotChooseCourse = False
        hasDidnotChooseYearLevel = False
        hasChooseBSIT = False
        hasChooseBSCS = False
        hasChooseBSIS = False
        hasDidnotChooseYear = False
        hasChooseFirstYear = False
        hasChooseSecondYear = False
        hasChooseThirdYear = False
        hasChooseFourthYear = False

        try:
            firstPassword = self.firstPasswordField_2.text()
            secondPassword = self.secondPasswordField.text()
            hashFirstPassword = bcrypt.hashpw(firstPassword.encode('utf-8'), bcrypt.gensalt())

            lowerPasswordInput = self.validateLowerInputPassword()
            capitalLetterPassword = self.validateCapitalInputPassword()
            digitInputPassword = self.validateDigitInputInPassword()
            requiredSpecialCharacter = self.specialCharacterValidation(firstPassword)

            courseAndYear = self.comboBoxCourseChoices.itemText(self.comboBoxCourseChoices.currentIndex())
            hasYearLevelChoices = self.yearLevelChoices.itemText(self.yearLevelChoices.currentIndex())

            username = self.usernameTextField.text()
            schoolId = self.schoolIdTextField.text()
            schoolEmail = self.schoolEmailTextField.text()
            firstPassword = self.firstPasswordField_2.text()
            hasValidEqualPassword = False
            secondPassword = self.secondPasswordField.text()

            settingBorderToWrongInput = "QLineEdit { border : 2px solid red;}"
            if firstPassword != secondPassword:
                self.firstPasswordField_2.setStyleSheet(settingBorderToWrongInput)
                self.secondPasswordField.setStyleSheet(settingBorderToWrongInput)

            if username == "" and schoolId == "" and schoolEmail == "" and firstPassword == "" and secondPassword == "":
                self.usernameTextField.setStyleSheet(settingBorderToWrongInput)
                self.schoolIdTextField.setStyleSheet(settingBorderToWrongInput)
                self.schoolEmailTextField.setStyleSheet(settingBorderToWrongInput)
                self.firstPasswordField_2.setStyleSheet(settingBorderToWrongInput)
                self.secondPasswordField.setStyleSheet(settingBorderToWrongInput)

            if courseAndYear == "Choose your course?":
                hasDidnotChooseCourse = True
                self.comboBoxCourseChoices.setStyleSheet("font: 14px bold;\n"
                                                         "border-style:outset;\n"
                                                         "border-width:2px; \n"
                                                         "border-radius:8px;\n"
                                                         "border-color: red;\n"

                                                         )

            if hasYearLevelChoices == "Year Level":
                hasDidnotChooseYearLevel = True
                self.yearLevelChoices.setStyleSheet("font: 14px bold;\n"
                                                    "border-style:outset;\n"
                                                    "border-width:2px; \n"
                                                    "border-radius:8px;\n"
                                                    "border-color: red;\n"

                                                    )
            if hasValidUsername is not True:
                self.studentUsernameFeedback.setText("Your username should be atleast 6 characters or more")
            else:
                self.studentUsernameFeedback.setText("")

            if hasValidSchoolId is not True:
                self.schoolIDFeedBack.setText("Your schoolID Doesn't Exist")
            else:
                self.schoolIDFeedBack.setText("")

            if hasValidGmail is not True:
                self.schoolEmailFeedback.setText("Your email doesn't exist")
            else:
                self.schoolEmailFeedback.setText("")

            if firstPassword == secondPassword and (lowerPasswordInput and capitalLetterPassword) and (
                    digitInputPassword or requiredSpecialCharacter) and (
                    hasValidUsername and hasValidSchoolId and hasValidGmail) and hasDidnotChooseCourse is not True and hasDidnotChooseYearLevel is not True:
                insertSuccessfullyRegisterStudent(username.strip(), schoolId.strip(), schoolEmail.strip(),
                                                  hashFirstPassword.strip(), courseAndYear, hasYearLevelChoices)
                successfullyRegisterUserMessage()


            else:

                checkErrorRegister()
                self.submitButtonRegister.setEnabled(False)

        except mysql.connector.Error as err:

            self.usernameTextField.setStyleSheet('border:2px solid red;')
            # self.usernameTextField.setText("")
            self.studentUsernameFeedback.setText("Your username is already exist")
            checkErrorRegister()


class SetAppointment(QDialog):
    def __init__(self):
        super(SetAppointment, self).__init__()
        loadUi('SetAppointment.ui', self)

        self.allEventListeners()

    def allEventListeners(self):
        self.purposeComboBox_3.currentIndexChanged.connect(self.userChoicesForPurposes)
        self.instructorComboBox_3.currentIndexChanged.connect(self.userChoicesDepartment)
        # document().toPlainText()
        self.purposeEdit.textChanged.connect(self.getUserInputFromNotes)
        self.plainTextEdit_3.textChanged.connect(self.getUserInputFromNotes)
        self.plainTextEdit_3.setVisible(False)

        self.mainHeaderXavier_7.setText("")
        self.getPrioButton.clicked.connect(self.onceButtonClickGeneratePriorityNumber)
        self.purposeEdit.setVisible(False)
        self.firstNameTextField_2.textChanged.connect(self.validateFirstName)
        self.backButton_2.clicked.connect(self.backToLoginFrame)
        todays_date = date.today()

        self.timeLabel_2.setText(f"{todays_date}")
        self.prionumdisplay.setEnabled(False)
        self.date.setEnabled(False)
        self.lineEdit.setEnabled(False)
        timer = QTimer(self)
        timer.timeout.connect(self.displayTime)
        timer.start(1000)
        timerForQueue = QTimer(self)
        timerForQueue.timeout.connect(self.setNumberOfQueue)
        timerForQueue.start(1000)

    hasChooseOtherPleaseSpecify = False
    userEnteredInOtherSpecify = ""
    hasChoosePurposeInComboBox = False
    hasValidCompleteName = False

    def setNumberOfQueue(self):
        # # loadpass = "SELECT Count(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'appointment'"
        #
        # fetchQueue = " SELECT COUNT(priority_number) FROM appointment"
        # mycursor = mydb.cursor(fetchQueue)
        # queueNumber = mycursor.fetchall()
        # rows = len(queueNumber)
        # if rows >= 1:
        #     print("fafafafa")
        # else:
        #     print('zczczxcz')
        loadpass = "SELECT COUNT(priority_number) FROM appointment"
        mydb = mysql.connector.connect(host="localhost", user="root", password="Rebolos143#",
                                       database="cc15finalproject")
        mycursor = mydb.cursor()
        mycursor.execute(loadpass)
        fetchAllQueue = mycursor.fetchall()
        firstList = []
        finalList = ()
        firstItem = 0
        # lengthOfItems = len(fetchAllQueue)
        # self.presentNumberQueue.setText(f"{lengthOfItems}")
        # for eachNumberOfQueue,item in enumerate(fetchAllQueue):
        #
        #     self.presentNumberQueue.setText(f"{item}")
        # for eachNumberQueue, itemQueue in enumerate(fetchAllQueue):
        #
        #     if eachNumberQueue > firstItem:
        #         firstItem += 1

        for eachItem in fetchAllQueue:
            self.presentNumberQueue.setText(f"{eachItem}")

        # lengthOfNumbers = len(firstList)
        # for eachItem in range(lengthOfNumbers):
        #     print(eachItem)
        #     self.presentNumberQueue.setText(f"{eachItem}")
        # for eachItem in range(1,eachNumberOfQueue,1):
        #     self.presentNumberQueue.setText(f"{eachItem}")

        # firstList = []
        # for eachNumber in queueNumber:
        #     firstList.append(eachNumber)
        #
        # for inEachQueue in firstList:
        #     fifo.put(inEachQueue)
        # while not fifo.empty():
        #     self.presentNumberQueue.setText(f"{fifo.get()}")

    def displayTime(self):
        currentTIme = QTime.currentTime()
        displayText = currentTIme.toString('hh:mm:ss ')
        print(displayText)
        self.timeLabel.setText(f"{displayText}")

    def backToLoginFrame(self):
        login = LoginStudentForm()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def validateFirstName(self):
        global hasValidCompleteName
        completeName = self.firstNameTextField_2.text()
        if isValidCompleteName(completeName):

            self.firstNameTextField_2.setStyleSheet("font: 18px bold;\n"
                                                    "border-style:outset;\n"
                                                    "border-width:2px; \n"
                                                    "border-radius:20px;\n"
                                                    "border-color: #39ccb1;\n")
            hasValidCompleteName = True

        elif completeName == "":
            hasValidCompleteName = False
            self.firstNameTextField_2.setStyleSheet("#firstNameTextField {\n"
                                                    "font:18px bold;\n"
                                                    "\n"
                                                    "border-color:gray;\n"
                                                    "border-style:outset;\n"
                                                    "border-width:2px;\n"
                                                    "border-radius:20px;\n"
                                                    "border:none;\n"
                                                    "padding:8px;\n"
                                                    "background-color:#fff;\n"
                                                    "color:rgb(1, 26, 42)\n"
                                                    "}\n"
                                                    "\n"
                                                    "")

        else:
            hasValidCompleteName = False
            self.firstNameTextField_2.setStyleSheet("font: 18px bold;\n"
                                                    "border-style:outset;\n"
                                                    "border-width:2px; \n"
                                                    "border-radius:20px;\n"
                                                    "border-color: red;\n")

    def userChoicesForPurposes(self):
        global hasChooseOtherPleaseSpecify
        global userEnteredInOtherSpecify
        global hasChoosePurposeInComboBox

        hasChoosePurposeOfAppointment = self.purposeComboBox_3.itemText(self.purposeComboBox_3.currentIndex())

        if hasChoosePurposeOfAppointment == "Tuition Fee" or hasChoosePurposeOfAppointment == "Enrollment" or hasChoosePurposeOfAppointment == "Course Inquiry" or hasChoosePurposeOfAppointment == "Grade Consultation":
            hasChoosePurposeInComboBox = True
            self.purposeComboBox_3.setStyleSheet("font: bold 14px;\n"
                                                 "border-style:outset;\n"
                                                 "border-width:2px; \n"
                                                 "border-radius:8px;\n"
                                                 "border-color: #39ccb1;\n")
            self.popMessageToGenerateUser()

        if hasChoosePurposeOfAppointment == "Others Please Specify Below":
            hasChooseOtherPleaseSpecify = True
            self.purposeComboBox.setStyleSheet("font: bold 14px;\n"
                                               "border-style:outset;\n"
                                               "border-width:2px; \n"
                                               "border-radius:8px;\n"
                                               "border-color: #39ccb1;\n"
                                               )
            self.popUpForOtherSpecify()

    hasChooseAnyInTheDepartment = False

    def userChoicesDepartment(self):
        global hasChooseAnyInTheDepartment
        hasUserChooseDepartment = self.instructorComboBox_3.itemText(self.instructorComboBox_3.currentIndex())

        if hasUserChooseDepartment == "Computer Science" or hasUserChooseDepartment == " Information Technology" or hasUserChooseDepartment == " Information Systems":
            hasChooseAnyInTheDepartment = True
            self.instructorComboBox_3.setStyleSheet("font: bold 14px;\n"
                                                    "border-style:outset;\n"
                                                    "border-width:2px; \n"
                                                    "border-radius:8px;\n"
                                                    "border-color: #39ccb1;\n"
                                                    )

        else:

            self.instructorComboBox_3.setStyleSheet("font: bold 14px;\n"
                                                    "border-style:outset;\n"
                                                    "border-width:2px; \n"
                                                    "border-radius:8px;\n"
                                                    "border-color: red;\n"
                                                    )

    hasChooseYesToShowNotes = False

    def popMessageToGenerateUser(self):
        global hasChooseYesToShowNotes
        askUserToShowTheNotes = QMessageBox()
        askUserToShowTheNotes.setWindowTitle("QUESTION")
        askUserToShowTheNotes.setText("Do you want to add a notes for your appointment?")
        askUserToShowTheNotes.setIcon(QMessageBox.Question)

        askUserToShowTheNotes.setMaximumHeight(250)
        askUserToShowTheNotes.setMaximumWidth(300)
        askUserToShowTheNotes.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        askUserToShowTheNotes.buttonClicked.connect(self.validateMessage)

        getUserResponse = askUserToShowTheNotes.exec_()

        if getUserResponse == QMessageBox.Yes:
            hasChooseYesToShowNotes = True
            self.purposeEdit.setStyleSheet("border-color: #39ccb1")
            self.purposeEdit.setVisible(True)
            self.mainHeaderXavier_7.setText("TYPE YOUR NOTES BELOW")
            self.mainHeaderXavier_7.setStyleSheet("font:bold 12px;")
        elif getUserResponse == QMessageBox.No:
            print("FAFAFAFA")
            hasChooseYesToShowNotes = False

    validateUserResponseOnOtherSpecifiy = False

    def popUpForOtherSpecify(self):
        global validateUserResponseOnOtherSpecifiy
        askUserShowSpecifyNotes = QMessageBox()
        askUserShowSpecifyNotes.setWindowTitle("QUESTION")
        askUserShowSpecifyNotes.setText("Are you sure that you want to choice other specify?")

        askUserShowSpecifyNotes.setIcon(QMessageBox.Question)

        askUserShowSpecifyNotes.setMaximumHeight(250)
        askUserShowSpecifyNotes.setMaximumWidth(300)
        askUserShowSpecifyNotes.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        askUserShowSpecifyNotes.buttonClicked.connect(self.validateMessage)

        getUserResponse = askUserShowSpecifyNotes.exec_()

        if getUserResponse == QMessageBox.Yes:
            validateUserResponseOnOtherSpecifiy = True
            self.plainTextEdit_3.setStyleSheet("border-color: #39ccb1")
            self.plainTextEdit_3.setVisible(True)
            self.mainHeaderXavier_7.setText("YOUR CONCERN")
            self.mainHeaderXavier_7.setStyleSheet("font:bold 12px;")
        elif getUserResponse == QMessageBox.No:
            validateUserResponseOnOtherSpecifiy = False
        else:
            print("YAWA KA")

    hasValidNotesOtherSpecify = False

    def getUserInputFromNotes(self):
        global hasValidNotesInput
        global hasValidNotesOtherSpecify
        getUserInputInTheNotes = self.plainTextEdit_3.document().toPlainText()
        getTheLengthInputInNotes = len(getUserInputInTheNotes)
        getInputFromPurposeNotes = self.purposeEdit.document().toPlainText()
        getLengthFromPurposeNotes = len(getInputFromPurposeNotes)
        if getTheLengthInputInNotes >= 1 and hasChooseOtherPleaseSpecify:
            hasValidNotesInput = True
            self.getPrioButton.setEnabled(True)
            self.plainTextEdit_3.setStyleSheet("font: bold 14px;\n"
                                               "border-style:outset;\n"
                                               "border-width:2px; \n"
                                               "border-radius:8px;\n"
                                               "border-color: #39ccb1;\n"

                                               )
        else:
            self.plainTextEdit_3.setStyleSheet("font: bold 14px;\n"
                                               "border-color: red;\n"
                                               )

        if getLengthFromPurposeNotes >= 1 and hasChooseYesToShowNotes:
            print("Notes button")
            hasValidNotesOtherSpecify = True
            self.purposeEdit.setStyleSheet("font: bold 14px;\n"
                                           "border-style:outset;\n"
                                           "border-width:2px; \n"
                                           "border-radius:8px;\n"
                                           "border-color: #39ccb1;\n"

                                           )


        else:

            self.purposeEdit.setStyleSheet("font: bold 14px;\n"
                                           "border-color: red;\n"
                                           )

    def validateMessage(self, i):
        if i == QMessageBox.Yes:
            print("Button clicked is ", i.text())

    def generatePrio(self):
        list = []
        count = 1

        try:
            for eachButtonIsClicked in range(count, 100, 1):
                # fifo.put(eachButtonIsClicked)

                fifo.put(eachButtonIsClicked)

            finalList = set()

            for eachItemInQueue in fifo.queue:
                if eachItemInQueue not in finalList:
                    finalList.add(eachItemInQueue)

            for eachNotDuplicate in finalList:
                finalFifo.put(eachNotDuplicate)

            while not finalFifo.empty():
                self.prionumdisplay.setText(f"{finalFifo.get()}")

                break
        except IntegrityError as err:
            duplicateEntryForUsername()

    hasChooseNotToSetAnAppointment = False

    def validateUserToProceedInPrio(self):
        global hasChooseNotToSetAnAppointment
        closeApplication = QMessageBox()
        closeApplication.setWindowTitle("QUESTION")
        closeApplication.setText("Are you sure that you don't want to set a day and time on your appointment?")

        closeApplication.setIcon(QMessageBox.Question)

        closeApplication.setMaximumHeight(250)
        closeApplication.setMaximumWidth(300)
        closeApplication.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        closeApplication.buttonClicked.connect(self.validateMessage)

        getUserResponse = closeApplication.exec_()

        if getUserResponse == QMessageBox.Yes:
            self.generatePrio()
            hasChooseNotToSetAnAppointment = True
            self.getPrioButton.setEnabled(False)

        elif getUserResponse == QMessageBox.No:
            self.generatePrio()
            hasChooseNotToSetAnAppointment = False
            todays_date = date.today()
            import time
            t = time.localtime()

            current_time = time.strftime("%H:%M:%S AM", t)

            self.date.setText(f"{todays_date}")
            self.lineEdit.setText(f"{current_time}")

            self.getPrioButton.setEnabled(False)
            # self.dayTextField.setEnabled(True)
            # self.monthTextField.setEnabled(True)
            # self.yearTextField.setEnabled(True)

    def validateMessage(self, i):
        if self == QMessageBox.Yes:
            print("Button clicked is ", i.text())

    def onceButtonClickGeneratePriorityNumber(self):
        # presentQueueNumber = self.presentNumberOfQueue.text()
        try:

            count = 0
            hasChoosePurposeOfAppointment = self.purposeComboBox_3.itemText(self.purposeComboBox_3.currentIndex())
            isDefaultValueSelected = self.instructorComboBox_3.itemText(self.instructorComboBox_3.currentIndex())
            hasChoiceAnyDepartment = False
            getUserInputInTheNotes = self.plainTextEdit_3.document().toPlainText()
            getTheLengthInputInNotes = len(getUserInputInTheNotes)
            getInputFromPurposeNotes = self.purposeEdit.document().toPlainText()
            getLengthFromPurposeNotes = len(getInputFromPurposeNotes)

            # userEntererdMonth = self.monthTextField.text()
            # userEnteredDay = self.dayTextField.text()
            hasValidNotesInput = False
            hasValidNotesForOTherConcern = False
            hasChooseOtherSpecifyBox = False
            complete_Name = self.firstNameTextField_2.text()
            dateInputed = self.date.text()
            timeTextField = self.lineEdit.text()
            priorityNumber = self.prionumdisplay.text()
            hasChoosePurposeForAppointment = False

            if complete_Name == "":
                self.firstNameTextField_2.setStyleSheet("font: bold 18px;\n"
                                                        "border-style:outset;\n"
                                                        "border-width:2px; \n"
                                                        "border-radius:20px;\n"
                                                        "border-color: red;\n"
                                                        )
            if hasChoosePurposeOfAppointment == "Other Please Specify Below":
                self.purposeComboBox_3.setStyleSheet("font: bold 14px;\n"
                                                     "border-style:outset;\n"
                                                     "border-width:2px; \n"
                                                     "border-radius:8px;\n"
                                                     "border-color: red;\n"
                                                     )
            if isDefaultValueSelected == "Choices Department":

                self.instructorComboBox_3.setStyleSheet("font: bold 14px;\n"
                                                        "border-style:outset;\n"
                                                        "border-width:2px; \n"
                                                        "border-radius:8px;\n"
                                                        "border-color: red;\n"
                                                        )

            else:
                hasChoiceAnyDepartment = True
            if hasChoosePurposeOfAppointment == "Choose your Purpose?":
                self.purposeComboBox_3.setStyleSheet("font: bold 14px;\n"
                                                     "border-style:outset;\n"
                                                     "border-width:2px; \n"
                                                     "border-radius:8px;\n"
                                                     "border-color: red;\n"
                                                     )
            else:
                hasChoosePurposeForAppointment = True

            if getTheLengthInputInNotes >= 1 and hasChooseOtherPleaseSpecify:
                hasValidNotesForOTherConcern = True
                self.plainTextEdit_3.setStyleSheet("font: bold 14px;\n"
                                                   "border-style:outset;\n"
                                                   "border-width:2px; \n"
                                                   "border-radius:8px;\n"
                                                   "border-color: #39ccb1;\n"

                                                   )
            elif getLengthFromPurposeNotes >= 1 and hasChooseYesToShowNotes:
                hasValidNotesInput = True
                self.purposeEdit.setStyleSheet("font: bold 14px;\n"
                                               "border-style:outset;\n"
                                               "border-width:2px; \n"

                                               "border-radius:8px;\n"
                                               "border-color: #39ccb1;\n"

                                               )
            if hasChooseAnyInTheDepartment and hasChoosePurposeForAppointment or hasChooseYesToShowNotes and hasValidCompleteName and hasChooseNotToSetAnAppointment:
                self.validateUserToProceedInPrio()

                insertStudentAppointment(self.prionumdisplay.text(), complete_Name, hasChoosePurposeOfAppointment,
                                         isDefaultValueSelected, getUserInputInTheNotes, getInputFromPurposeNotes,
                                         dateInputed, timeTextField)
                inputAllTheFields()

            else:
                errorFieldAppointment()


        except IntegrityError as err:

            # self.presentNumberOfQueue.setText("")
            feedbackUserDuplicatePriorityNumber(self.presentNumberOfQueue.text())


        except NameError as err:
            print(err)
            errorFieldAppointment()
        except mysql.connector.errors.DatabaseError:
            print("312312312")


class GuestLogbookRegistration(QDialog):
    def __init__(self):
        super(GuestLogbookRegistration, self).__init__()
        loadUi('GuestLogbookRegistrationForm.ui', self)

        self.allEventListeners()

    def allEventListeners(self):
        self.firstNameTextField.textChanged.connect(self.validPersonalInfomartionOfUsers)
        self.lastNameTextField.textChanged.connect(self.validPersonalInfomartionOfUsers)
        self.middleNameTextField.textChanged.connect(self.validPersonalInfomartionOfUsers)
        self.firstNameTextField.returnPressed.connect(self.validPersonalInfomartionOfUsers)
        self.firstNameTextField.editingFinished.connect(self.validPersonalInfomartionOfUsers)
        self.middleNameTextField_2.textChanged.connect(self.validPersonalInfomartionOfUsers)
        self.middleNameTextField_3.textChanged.connect(self.validPersonalInfomartionOfUsers)
        self.dayTextField.textChanged.connect(self.validateDateAndTime)
        self.monthTextField.textChanged.connect(self.validateDateAndTime)
        self.yearTextField.textChanged.connect(self.validateYear)
        self.submitButtonRegister_2.setEnabled(False)
        self.submitButtonRegister_2.clicked.connect(self.feedbackUserOnceTheButtonClicked)
        # self.goBackToLogin_2.clicked.connect(self.goToLoginScreen)
        self.cancelButton_2.clicked.connect(self.askUserCancel)

    hasValidFirstname = False
    hasValidLastName = False
    hasValidMiddleName = False
    hasValidSuffixesName = False
    hasValidGmail = False

    def validPersonalInfomartionOfUsers(self):
        outsiderFirstName = self.firstNameTextField.text()
        outsiderLastName = self.lastNameTextField.text()
        outsiderMiddleName = self.middleNameTextField.text()
        suffixeName = self.middleNameTextField_2.text()
        gmailAccount = self.middleNameTextField_3.text()
        global hasValidFirstname
        global hasValidLastName
        global hasValidMiddleName
        global hasValidSuffixesName
        global hasValidGmail
        settingGoodCorrectInputPassword = " border : 2px solid #39ccb1;\n color:black;\n  font: 15px normal;"
        settingBorderToWrongInput = "border : 2px solid red;\n color:black;\n  font: 15px normal;"
        settingBacktoNormal = "border : 1px solid black;\n color:black;\n  font: 15px normal;"
        if isValidFirstNameAndLastname(outsiderFirstName):
            hasValidFirstname = True
            self.firstNameTextField.setStyleSheet(settingGoodCorrectInputPassword)
            # self.firstNameTextField.setStyleSheet(fontUserInput)
        elif outsiderFirstName == "":

            self.firstNameTextField.setStyleSheet(settingBacktoNormal)
        else:
            hasValidFirstname = False
            self.firstNameTextField.setStyleSheet(settingBorderToWrongInput)
            # self.firstNameTextField.setStyleSheet(settingBorderToWrongInput)
            # self.firstNameTextField.setStyleSheet(fontUserInput)
        if isValidFirstNameAndLastname(outsiderLastName):
            hasValidLastName = True
            self.lastNameTextField.setStyleSheet(settingGoodCorrectInputPassword)
        elif outsiderLastName == "":
            self.lastNameTextField.setStyleSheet(settingBacktoNormal)
        else:
            hasValidLastName = False
            self.lastNameTextField.setStyleSheet(settingBorderToWrongInput)

        if isValidFirstNameAndLastname(outsiderMiddleName):
            hasValidMiddleName = True
            self.middleNameTextField.setStyleSheet(settingGoodCorrectInputPassword)
        elif outsiderMiddleName == "":
            self.middleNameTextField.setStyleSheet(settingBacktoNormal)
        else:
            hasValidMiddleName = False
            self.middleNameTextField.setStyleSheet(settingBorderToWrongInput)

        if isValidSuffixes(suffixeName):
            hasValidSuffixesName = True
            self.middleNameTextField_2.setStyleSheet(settingGoodCorrectInputPassword)
        elif suffixeName == "":
            self.middleNameTextField_2.setStyleSheet(settingBacktoNormal)
        else:
            hasValidSuffixesName = False
            self.middleNameTextField_2.setStyleSheet(settingBorderToWrongInput)

        if isValidGmailAccount(gmailAccount):
            hasValidGmail = True
            self.middleNameTextField_3.setStyleSheet(settingGoodCorrectInputPassword)
        elif gmailAccount == "":
            self.middleNameTextField_3.setStyleSheet(settingBacktoNormal)
        else:
            self.middleNameTextField_3.setStyleSheet(settingBorderToWrongInput)

        if outsiderFirstName == "" or outsiderLastName == "" or outsiderMiddleName == "" or gmailAccount == "":
            self.submitButtonRegister_2.setEnabled(False)
        else:
            self.submitButtonRegister_2.setEnabled(True)

    hasChooseMonthHas30Days = False
    hasChooseMonthHas31Days = False
    hasChooseMonthWith28Days = False
    hasUserEnteredDay31 = False
    hasUserChooseDay28 = False
    hasUserEnteredDAY30 = False
    hasValidYear = False
    hasDontHaveValidDate = False

    def validateDateAndTime(self):
        settingGoodCorrectInputPassword = " border : 2px solid #39ccb1;\n color:black;\n  font: 15px normal;"
        settingBorderToWrongInput = "border : 2px solid red;\n color:black;\n  font: 15px normal;"
        settingBacktoNormal = "border : 1px solid black;\n color:black;\n  font: 15px normal;"
        try:
            global hasChooseMonthHas30Days
            global hasChooseMonthHas31Days
            global hasChooseMonthWith28Days

            userEntererdMonth = self.monthTextField.text()
            global hasUserEnteredDay31
            global hasUserChooseDay28
            global hasUserEnteredDAY30
            global hasGreaterTwoLength
            global hasDontHaveValidDate

            userEnteredDay = self.dayTextField.text()
            convertedDayToInteger = int(userEnteredDay)

            if convertedDayToInteger <= 31:
                hasUserEnteredDay31 = True
                self.dayTextField.setStyleSheet(settingGoodCorrectInputPassword)

            if convertedDayToInteger <= 30:
                hasUserEnteredDAY30 = True
                self.dayTextField.setStyleSheet(settingGoodCorrectInputPassword)



            elif len(userEnteredDay) == 0 or len(userEnteredDay) > 2:
                hasUserEnteredDAY30 = False
                self.dayTextField.setStyleSheet(settingBorderToWrongInput)

            if convertedDayToInteger <= 28:
                hasUserChooseDay28 = True
                self.dayTextField.setStyleSheet(settingGoodCorrectInputPassword)

            elif len(userEnteredDay) == 0 or len(userEnteredDay) > 2:
                hasUserChooseDay28 = False
                self.dayTextField.setStyleSheet(settingBorderToWrongInput)
            else:
                hasUserChooseDay28 = False

            if (
                    userEntererdMonth == "June" or userEntererdMonth == "September" or userEntererdMonth == "November" or userEntererdMonth == "April" and hasUserEnteredDAY30 is True):
                print("30 days")
                hasChooseMonthHas30Days = True
                self.monthTextField.setStyleSheet(settingGoodCorrectInputPassword)

            if userEntererdMonth == "":
                print("YAWA SULOD SI 30DAYS")
                hasChooseMonthHas30Days = False
                self.monthTextField.setStyleSheet(settingBacktoNormal)

            if userEntererdMonth == "March" or userEntererdMonth == "July" or userEntererdMonth == "August" or userEntererdMonth == "December" or userEntererdMonth == "October" or userEntererdMonth == "May" or userEntererdMonth == "January" and hasUserEnteredDay31 and hasChooseMonthHas30Days is not True:
                print("You should work")
                self.monthTextField.setStyleSheet(settingGoodCorrectInputPassword)

                hasChooseMonthHas31Days = True

            if userEntererdMonth == "February" and hasUserChooseDay28:
                hasChooseMonthWith28Days = True
                print("YAWA")
                self.monthTextField.setStyleSheet(settingGoodCorrectInputPassword)
            if userEntererdMonth == "February" and hasUserChooseDay28 is not True:
                hasChooseMonthWith28Days = False
                hasChooseMonthHas30Days = False
                hasChooseMonthHas31Days = False
                hasDontHaveValidDate = True
                print("YAWA GANA NA ")
                self.dayTextField.setStyleSheet(settingBorderToWrongInput)

                self.monthTextField.setStyleSheet(settingGoodCorrectInputPassword)


        except NameError:
            self.monthTextField.setStyleSheet(settingBacktoNormal)
        except ValueError:
            self.dayTextField.setStyleSheet(settingBacktoNormal)

    def validateYear(self):
        settingGoodCorrectInputPassword = " border : 2px solid #39ccb1;\n color:black;\n  font: 15px normal;"
        settingBorderToWrongInput = "border : 2px solid red;\n color:black;\n  font: 15px normal;"
        settingBacktoNormal = "border : 1px solid black;\n color:black;\n  font: 15px normal;"
        global hasValidYear
        try:
            userEnteredYear = self.yearTextField.text()
            convertStringToInt = int(userEnteredYear)
            if convertStringToInt == 2021:
                hasValidYear = True
                self.yearTextField.setStyleSheet(settingGoodCorrectInputPassword)


            elif convertStringToInt > 2021:
                hasValidYear = False
                self.yearTextField.setStyleSheet(settingBorderToWrongInput)



            else:

                hasValidYear = False
                self.yearTextField.setStyleSheet(settingBorderToWrongInput)



        except ValueError:
            self.yearTextField.setStyleSheet(settingBacktoNormal)

    validateSuffixeNameEmptyResponse = False

    def validateUserCancelButton(self):
        global validateSuffixeNameEmptyResponse
        validateUserResponseSuffixeName = QMessageBox()
        validateUserResponseSuffixeName.setWindowTitle("QUESTION")
        validateUserResponseSuffixeName.setText("Are you sure that you don't have a suffixe name?")

        validateUserResponseSuffixeName.setIcon(QMessageBox.Question)

        validateUserResponseSuffixeName.setMaximumHeight(250)
        validateUserResponseSuffixeName.setMaximumWidth(300)
        validateUserResponseSuffixeName.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        validateUserResponseSuffixeName.buttonClicked.connect(self.validateMessage)

        getUserResponse = validateUserResponseSuffixeName.exec_()

        if getUserResponse == QMessageBox.Yes:
            validateSuffixeNameEmptyResponse = True
        elif getUserResponse == QMessageBox.No:
            validateSuffixeNameEmptyResponse = False

    def feedbackUserOnceTheButtonClicked(self):
        outsiderFirstName = self.firstNameTextField.text()
        outsiderLastName = self.lastNameTextField.text()
        outsiderMiddleName = self.middleNameTextField.text()
        suffixeName = self.middleNameTextField_2.text()
        gmailAccount = self.middleNameTextField_3.text()
        userEntererdMonth = self.monthTextField.text()
        userEnteredDay = self.dayTextField.text()
        convertedDayToInteger = int(userEnteredDay)
        dayConvertToString = str(convertedDayToInteger)
        userEnteredYear = self.yearTextField.text()
        userEnteredYear = self.yearTextField.text()
        convertStringToInt = int(userEnteredYear)
        yearToString = str(convertStringToInt)

        completeName = outsiderFirstName + " " + outsiderLastName + " " + outsiderMiddleName + " " + suffixeName
        dateAccount = dayConvertToString + "," + userEntererdMonth + "," + yearToString

        timeAccountRegister = self.yearTextField_2.text()

        t = time.localtime()
        current_time = time.strftime("%H:%M:%S AM", t)
        settingGoodCorrectInputPassword = " border : 2px solid #39ccb1;\n color:black;\n  font: 15px normal;"

        if suffixeName == "":

            self.validateUserCancelButton()

            if hasValidFirstname and validateSuffixeNameEmptyResponse and hasValidMiddleName and hasValidGmail and (
                        hasChooseMonthHas30Days or hasChooseMonthHas31Days or hasChooseMonthWith28Days):
                self.yearTextField_2.setText(f"{current_time}")
                self.yearTextField_2.setStyleSheet(settingGoodCorrectInputPassword)

                self.submitButtonRegister_2.setEnabled(False)
                insertSuccessLogBookRegister(completeName, gmailAccount, dateAccount, self.yearTextField_2.text())
                print("tang inaaaaaa")
                guestSuccessfullyFeedback
                self.guestAppointmentForm()


        elif hasValidFirstname and hasValidSuffixesName and hasValidMiddleName and hasValidGmail and (
                hasChooseMonthHas30Days or hasChooseMonthHas31Days or hasChooseMonthWith28Days):

            self.yearTextField_2.setText(f"{current_time}")
            self.yearTextField_2.setStyleSheet(settingGoodCorrectInputPassword)
            self.submitButtonRegister_2.setEnabled(False)
            insertSuccessLogBookRegister(completeName, gmailAccount, dateAccount, self.yearTextField_2.text())
            guestSuccessfullyFeedback()
            self.guestAppointmentForm()

        elif hasDontHaveValidDate is True:
            checkInputFields()

    def validateMessage(i):
        if i == QMessageBox.Yes:
            print("Button clicked is ", i.text())

    # def goToLoginScreen(self):
    #     self.login = QtWidgets.QMainWindow()
    #     self.ui = Login()
    #     self.ui.setupUi(self.login)
    #     MainWindow.destroy()
    #     self.login.show()

    def askUserCancel(self):
        validateUserCancelButton()
    def guestAppointmentForm(self):
        guestAppointment = SetAppointment()
        widget.addWidget(guestAppointment)
        widget.setCurrentIndex(widget.currentIndex() + 1)
# class GuestFunction(QDialog):
#     def __init__(self):
#         super(GuestFunction, self).__init__()
#         loadUi('FacultyGuestFunction.ui', self)
#         self.addDataColumnToTableView()
#         self.logoutButton.clicked.connect(self.removeRow)
#         self.model = QStandardItemModel()
#     #
#     # class TableModel(QtCore.QAbstractTableModel):
#     #     def __init__(self, data):
#     #         super(TableModel, self).__init__()
#     #         self._data = data
#     #
#     #     def data(self, index, role):
#     #         if role == Qt.DisplayRole:
#     #             # See below for the nested-list data structure.
#     #             # .row() indexes into the outer list,
#     #             # .column() indexes into the sub-list
#     #             return self._data[index.row()][index.column()]
#     #
#     #     def rowCount(self, index):
#     #         # The length of the outer list.
#     #         return len(self._data)
#     #
#     #     def columnCount(self, index):
#     #         # The following takes the first sub-list, and returns
#     #         # the length (only works if all rows are an equal length)
#     #         return len(self._data[0])
#
#
#     def addDataColumnToTableView(self):
#
#
#         mydb = mysql.connector.connect(host="localhost", user="root", password="Rebolos143#",
#                                        database="cc15finalproject")
#
#         loadSchoolId = "SELECT * FROM logbookaccounts"
#         mycursor = mydb.cursor(buffered=True)
#         mycursor.execute(loadSchoolId)
#
#         outsiderDatas = mycursor.fetchall()
#
#         headersName = ('Logbook Id', 'Complete Name', 'gmail_account', 'date', 'Time')
#         # model = QStandardItemModel()
#
#         self.model.setHorizontalHeaderLabels(headersName)
#
#         for eachRow, eachColumnItem, in enumerate(outsiderDatas):
#             # print(eachColumnItem)
#             row = []
#             # model.setItem(eachRow,eachColumnItem)
#             for eachItem, data in enumerate(eachColumnItem):
#                 print(eachColumnItem)
#                 # print(data)
#                 modelData = QStandardItem(data)
#
#                 self.model.setItem(eachRow, eachItem, modelData)
#
#                 # modelTable = TableModel(model)
#                 # self.tableView.setModel(modelTable)
#
#         self.tableView.setModel(self.model)
#         filter_proxy_model = QSortFilterProxyModel()
#
#         filter_proxy_model.setSourceModel(self.model)
#         filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
#         self.tableView.setModel(filter_proxy_model)
#         filter_proxy_model.setFilterKeyColumn(1)
#
#         self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
#         self.SearchBar.textChanged.connect(filter_proxy_model.setFilterRegExp)
#         # self.functionMappingSignal()
#
#     def removeRow(self):
#
#         mydb = mysql.connector.connect(host="localhost", user="root", password="Rebolos143#",
#                                        database="cc15finalproject")
#
#         mycursor = mydb.cursor()
#         index_list = []
#         indices = self.tableView.selectionModel().selectedRows()
#
#         for index in sorted(indices):
#
#             index_list.append(index)
#
#         for index in index_list:
#             dataSelected = self.model.removeRow(index.row())
#
#             mycursor.execute("DELETE  FROM logbookaccounts WHERE logbook_id = %s", (dataSelected,))
#             mydb.commit()


app = QApplication(sys.argv)
mainWindow = LoginStudentForm()
# Para ni sa maka transition kas mga different screen by
# incrementing the index in order you can change the screen
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(1250)
widget.setFixedHeight(1000)
widget.show()
app.exec_()
