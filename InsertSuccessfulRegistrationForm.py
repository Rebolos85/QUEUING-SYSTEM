import mysql.connector


def insertSuccessfullyRegisterStudent(username, schoolid, schoolEmail, password, course, yearLevel):
    mydb = mysql.connector.connect(host="localhost", user="root", password="Rebolos143#",
                                   database="cc15finalproject")
    mycursor = mydb.cursor()
    mycursor.execute(
        """INSERT INTO studentaccount (username, school_id, school_email,student_course, student_year, student_password) 
        VALUES(%s,%s,%s,%s,%s,%s) """,
        (username, schoolid, schoolEmail, course, yearLevel, password))

    mydb.commit()
