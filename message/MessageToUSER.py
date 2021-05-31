
#
import sys


from PyQt5.QtWidgets import QMessageBox


def successfullyCreateAccountMessage():
    sucessfullyCreateAccount = QMessageBox()
    sucessfullyCreateAccount.setWindowTitle("Sucessfully")
    sucessfullyCreateAccount.setText("Your account was successfully registered")

    sucessfullyCreateAccount.setIcon(QMessageBox.Information)

    getUserResponse = sucessfullyCreateAccount.exec_()


def errorMessageForPasswordDoesntMatch():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Sucessfully")
    errorMessageResponse.setText("Sorry your password doesn't match")

    errorMessageResponse.setIcon(QMessageBox.Critical)

    getUserResponse = errorMessageResponse.exec_()


def noAccountFoundInDatabase():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Error Input Credentials")
    errorMessageResponse.setText("Sorry but your input credentials is not valid")

    errorMessageResponse.setIcon(QMessageBox.Critical)

    getUserResponse = errorMessageResponse.exec_()


def duplicateEntryForUsername():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Duplicate Entry For Username")
    errorMessageResponse.setText("Sorry, username is already exist")

    errorMessageResponse.setIcon(QMessageBox.Critical)

    getUserResponse = errorMessageResponse.exec_()


def accountSuccessfullyLogin():
    sucessfullyLoginMessage = QMessageBox()
    sucessfullyLoginMessage.setWindowTitle("Sucessfully")
    sucessfullyLoginMessage.setText("You're now successfully log in")

    sucessfullyLoginMessage.setIcon(QMessageBox.Information)

    getUserResponse = sucessfullyLoginMessage.exec_()


def successfullyRegisterUserMessage():
    sucessfullyLoginMessage = QMessageBox()
    sucessfullyLoginMessage.setWindowTitle("Successfully")
    sucessfullyLoginMessage.setText("Your account was successfully register")

    sucessfullyLoginMessage.setIcon(QMessageBox.Information)

    getUserResponse = sucessfullyLoginMessage.exec_()


def checkErrorRegister():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Error")
    errorMessageResponse.setText("Kindly, Please check all invalid input that has border")

    errorMessageResponse.setIcon(QMessageBox.Critical)

    getUserResponse = errorMessageResponse.exec_()


def feedbackOnceUserIDDoenNotExist():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Error")
    errorMessageResponse.setText("Sorry, but your schoolID Doesn't Exist")

    errorMessageResponse.setIcon(QMessageBox.Critical)

    getUserResponse = errorMessageResponse.exec_()


def validateUserCancelButton():
    closeApplication = QMessageBox()
    closeApplication.setWindowTitle("QUESTION")
    closeApplication.setText("Are you sure that you want to cancel this application?")

    closeApplication.setIcon(QMessageBox.Question)

    closeApplication.setMaximumHeight(250)
    closeApplication.setMaximumWidth(300)
    closeApplication.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    closeApplication.buttonClicked.connect(validateMessage)

    getUserResponse = closeApplication.exec_()

    if getUserResponse == QMessageBox.Yes:
        sys.exit()


def validateMessage(i):
    if i == QMessageBox.Yes:
        print("Button clicked is ", i.text())



def feedbackUserDuplicatePriorityNumber(duplicatePriorityNumber):
    msgbox = QMessageBox(QMessageBox.Information, "Title", "Sorry but this priority number is already occupied: %s" % duplicatePriorityNumber, QMessageBox.Ok)




    msgbox.exec_()


def feedbackUserSetAppointmentMessage(userPriorityNumber):
    msgbox = QMessageBox(QMessageBox.Information, "Title",
                         "Your priority number is: %s" % userPriorityNumber,
                         QMessageBox.Ok)

    msgbox.exec_()

def checkInputFields():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Error")
    errorMessageResponse.setText("Kindly, Please check your input fields that has red border")

    errorMessageResponse.setIcon(QMessageBox.Critical)

    getUserResponse = errorMessageResponse.exec_()

def noDataProperlySelected():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("No selected data")
    errorMessageResponse.setText("Please select row that has a data")

    errorMessageResponse.setIcon(QMessageBox.Critical)

    getUserResponse = errorMessageResponse.exec_()

def successfullyLoginAsFaculty():
    sucessfullyLoginMessage = QMessageBox()
    sucessfullyLoginMessage.setWindowTitle("Sucessfully")
    sucessfullyLoginMessage.setText("You're now successfully login as faculty")

    sucessfullyLoginMessage.setIcon(QMessageBox.Information)

    getUserResponse = sucessfullyLoginMessage.exec_()


def inputAllTheFields():
    sucessfullyLoginMessage = QMessageBox()
    sucessfullyLoginMessage.setWindowTitle("Sucessfully")
    sucessfullyLoginMessage.setText("Your set appointment is successfully registered in our system")

    sucessfullyLoginMessage.setIcon(QMessageBox.Information)

    getUserResponse = sucessfullyLoginMessage.exec_()


def errorFieldAppointment():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Error")
    errorMessageResponse.setText("PLEASE CHECK ALL YOUR INPUT FIELDS")

    errorMessageResponse.setIcon(QMessageBox.Critical)

    getUserResponse = errorMessageResponse.exec_()



def passwordDoesnotMatchFeedback():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Error")
    errorMessageResponse.setText("Your first password and second password doesn't match")

    errorMessageResponse.setIcon(QMessageBox.Critical)

    getUserResponse = errorMessageResponse.exec_()


def guestCodeFeedback():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Error")
    errorMessageResponse.setText("Incorrect input for guestCode password")

    errorMessageResponse.setIcon(QMessageBox.Critical)

    getUserResponse = errorMessageResponse.exec_()



def guestSuccessfullyFeedback():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Sucessfully")
    errorMessageResponse.setText("Your credentials successfully registered")

    errorMessageResponse.setIcon(QMessageBox.Information)

    getUserResponse = errorMessageResponse.exec_()

def successfullyFacultyRequest():
    errorMessageResponse = QMessageBox()
    errorMessageResponse.setWindowTitle("Sucessfully")
    errorMessageResponse.setText("Your credentials successfully registered")

    errorMessageResponse.setIcon(QMessageBox.Information)

    getUserResponse = errorMessageResponse.exec_()