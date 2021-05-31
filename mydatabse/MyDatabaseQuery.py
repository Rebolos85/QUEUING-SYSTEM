import bcrypt
import mysql.connector
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

# from SetAppointmentStudent import MainAppointmentFinal
from message.MessageToUSER import successfullyCreateAccountMessage, errorMessageForPasswordDoesntMatch, \
    accountSuccessfullyLogin, noAccountFoundInDatabase, feedbackUserSetAppointmentMessage

mydb = mysql.connector.connect(host="localhost", user="root", password="Rebolos143#",
                               database="cc15finalproject")


def retrieveUserInputUsernameAndPassword(username, userEnteredPassword, buttonDisabled):
    # mydb = mysql.connector.connect(host="localhost", user="root", password="Rebolos143#",
    #                                database="cc15finalproject")
    loadpass = "SELECT student_password FROM studentaccount WHERE username = %s"

    mycursor = mydb.cursor()
    # mycursor.execute('SELECT * FROM studentaccount WHERE username = %s AND password = %s', (username, password,))
    # account = mycursor.fetchone()
    # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    passwordInput = userEnteredPassword.encode("UTF-8")

    mycursor.execute(loadpass, (username,))
    loginpasswordCheck = mycursor.fetchone()

    retrieveDataFACULTY = "SELECT password FROM faculty_account WHERE email = %s"
    mycursor = mydb.cursor()
    mycursor.execute(retrieveDataFACULTY, (username,))
    passwordFaculty = userEnteredPassword.encode("UTF-8")
    loginFacultyPassword = mycursor.fetchone()

    # Checking if the loginpasswordCheck will retrieve not none
    if loginpasswordCheck is not None:
        # Re-assigning the username in order to have encode function
        usernameCheck = loginpasswordCheck[0]

        # Checking passowrd and stored password in db
        if bcrypt.checkpw(passwordInput, usernameCheck.encode("UTF-8")):
            accountSuccessfullyLogin()
            # appointFrame()
            # appointmentFrame()

        else:
            errorMessageForPasswordDoesntMatch()

            # Display error message if the password user input doesn't match in database
            # errorMessageForPasswordDoesntMatch()

    elif loginFacultyPassword is not None:
        passwordAccount = loginFacultyPassword[0]

        if bcrypt.checkpw(passwordFaculty, passwordAccount.encode("UTF-8")):
            accountSuccessfullyLogin()
        else:
            errorMessageForPasswordDoesntMatch()


    else:
        # Display error message if password and username doesn't match
        noAccountFoundInDatabase()


# def insertDataIntoAppointment(choosenPurpose, departmentChoices, purposeNotes, concernNotes, generatePriority,
#                               priorityNumber):
#     # mydb = mysql.connector.connect(host="localhost", user="root", password="Rebolos143#",
#     #                                database="cc15finalproject")
#     # mydb = mysql.connector.connect(host="localhost", user="root", password="Rebolos143#",
#     #                                database="cc15finalproject")
#     # insertDataIntoAppointment(hasChoosePurposeOfAppointment, isDefaultValueSelected,
#     #                           getUserInputInTheNotes, getInputFromPurposeNotes, presentQueueNumber,
#     #                           self.presentNumberOfQueue.text())
#     mycursor = mydb.cursor()
#     mycursor.execute(
#         """INSERT INTO appointment (studentPriorityNumber,purpose, notes, Department, other_specifynotes)
#              VALUES(%s,%s,%s,%s,%s)""",
#         (generatePriority, choosenPurpose, purposeNotes, departmentChoices, concernNotes))
#
#     feedbackUserSetAppointmentMessage(priorityNumber)
#     mydb.commit(
#
#     )

def insertStudentAppointment(priorityNumber,complete_name,choosePurpose,choiceDepartment,otherSpecifyNotes,notes,date,time):
    mycursor = mydb.cursor()
    mycursor.execute(""" INSERT INTO appointment(priority_number,complete_name,choosePurpose,choiceDepartment,otherSpecifyNotes,notes,date,time)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """, (priorityNumber,complete_name,choosePurpose,choiceDepartment,otherSpecifyNotes,notes,date,time))
    mydb.commit()
    


def insertSuccessfullyRegisterStudent(username, schoolid, schoolEmail, password, course, yearLevel):
    mycursor = mydb.cursor()
    mycursor.execute(
        """INSERT INTO studentaccount (username, school_id, school_email,student_course, student_year, student_password) 
        VALUES(%s,%s,%s,%s,%s,%s) """,
        (username, schoolid, schoolEmail, course, yearLevel, password))

    mydb.commit()


def insertSuccessLogBookRegister(completeName, email, date, Time):
    mycursor = mydb.cursor()
    mycursor.execute(
        """INSERT INTO logbookaccounts (complete_name, gmail_acc, date,timeRegistered) 
        VALUES(%s,%s,%s,%s) """,
        (completeName, email, date, Time))
    mydb.commit()


def registerFacultyAccount(firstName, lastName, middleName, suffixeName, email, password):
    mycursor = mydb.cursor()
    mycursor.execute(
        """INSERT INTO faculty_account (firstname, lastname, middle_name,suffixe_name,email,password) 
        VALUES(%s,%s,%s,%s,%s,%s) """,
        (firstName, lastName, middleName, suffixeName, email, password))
    mydb.commit()

#
# def appointFrame():
#     appointment = QtWidgets.QMainWindow()
#
#     appointmentGui = MainAppointmentFinal()
#     appointmentGui.setupUi(appointment)
#     appointment.show()
