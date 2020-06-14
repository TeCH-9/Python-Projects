import sys
import time
import sqlite3
from PySide2.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtTest import *

connection = sqlite3.connect("data.db")
pen = connection.cursor()

# Fonts
title_font = QFont("Century Gothic", 45)
button_font = QFont("Century Gothic", 35)
about_font = QFont("Times", 40)
text_font = QFont("Times", 25)


def up_side(available_window):

    # undo :)
    esc_button = QPushButton("<", available_window)
    esc_button.setFont(title_font)
    esc_button.setGeometry(20, 20, 50, 50)
    esc_button.clicked.connect(available_window.undo)

    # Quit button
    quit_button = QPushButton("X", available_window)
    quit_button.setFont(title_font)
    quit_button.setGeometry(1300, 20, 50, 50)
    quit_button.clicked.connect(Window.exit)


# Side Window
class intro(QWidget):
    def __init__(self):
        super().__init__()

        horizontal = QHBoxLayout()

        self.text = QLabel("Library v1")

        horizontal.addStretch()
        horizontal.addWidget(self.text)
        horizontal.addStretch()

        self.text.setFont(about_font)

        self.setLayout(horizontal)


class new_book(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add new book")

        self.icon()

        # Vertical layout
        self.vertical = QVBoxLayout()

        title = QLabel("Add New Book")
        title.setFont(button_font)

        # Entry for the book to be added
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Enter New Book Name")

        # Save Button
        save = QPushButton("Save")
        save.clicked.connect(self.save)

        # Set Layout (Vertical)
        self.vertical.addWidget(title)
        self.vertical.addWidget(self.entry)
        self.vertical.addWidget(save)

        self.setLayout(self.vertical)

    def save(self):
        alert1 = QLabel("this may take a while. . . Please wait")

        self.vertical.addWidget(alert1)

        # To wait
        QTest.qWait(500)

        name = self.entry.text()

        # Sending to dataBase
        pen.execute("INSERT INTO books (book_name) VALUES (?)", (name,))
        connection.commit()

        alert1.setText("successful !")
        QTest.qWait(500)
        self.close()

    def icon(self):
        image = QIcon("book.png")
        self.setWindowIcon(image)


class add_new_student(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add new Student")

        self.icon()

        # Vertical layout
        self.vertical = QVBoxLayout()

        title = QLabel("Add New Student")
        title.setFont(button_font)

        # Entry for the book to be added
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Enter New Student Name")

        # Save Button
        save = QPushButton("Save")
        save.clicked.connect(self.save)

        # Set Layout (Vertical)
        self.vertical.addWidget(title)
        self.vertical.addWidget(self.student_name)
        self.vertical.addWidget(save)

        self.setLayout(self.vertical)

    def save(self):
        alert1 = QLabel("this may take a while. . . Please wait")

        self.vertical.addWidget(alert1)

        # To wait
        QTest.qWait(500)

        name = self.student_name.text()

        # Sending to dataBase
        pen.execute("INSERT INTO students (student_name) VALUES (?)", (name,))
        connection.commit()

        alert1.setText("successful !")
        QTest.qWait(500)
        self.close()

    def icon(self):
        image = QIcon("book.png")
        self.setWindowIcon(image)


class new_borrowing(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Borrowing")

        self.name = ""

        self.icon()

        # Vertical layout
        self.vertical = QVBoxLayout()

        title = QLabel("Add New Borrowing !")
        title.setFont(text_font)

        # Date information
        month = time.strftime("%m")
        day = time.strftime("%d")
        year = time.strftime("%Y")

        month = str(month)
        day = str(day)
        year = str(year)

        total = month + "/" + day + "/" + year

        date = QLabel("Today's date is: " + total)

        # Entry for the student name to be added
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Enter Student Name")

        # Entry for the book name to be added
        self.book_name = QLineEdit()
        self.book_name.setPlaceholderText("Enter Book Name")

        # Entry for the Refund Date
        self.refund_date = QLineEdit()
        self.refund_date.setPlaceholderText("Enter Refund Date example:  06/13/2020 month/day/year")

        # Save Button
        save = QPushButton("Save")
        save.clicked.connect(self.save)

        # Control Button
        control = QPushButton("Name Control")
        control.clicked.connect(self.control)
        self.control_text = QLabel("Close Searches are: ")

        # Set Layout (Vertical)
        self.vertical.addWidget(title)
        self.vertical.addWidget(self.student_name)
        self.vertical.addWidget(self.control_text)
        self.vertical.addWidget(self.book_name)
        self.vertical.addWidget(self.refund_date)
        self.vertical.addWidget(control)
        self.vertical.addWidget(save)
        self.vertical.addWidget(date)

        self.setLayout(self.vertical)

    def save(self):
        alert1 = QLabel("this may take a while. . . Please wait")

        self.vertical.addWidget(alert1)

        # To wait
        QTest.qWait(500)

        # Line edit Texts 'Entry'
        student_name = self.student_name.text()
        book_name = self.book_name.text()
        refund_date = self.refund_date.text()

        # Sending to dataBase
        pen.execute("INSERT INTO borrow (student_name,book_name,refund_date) VALUES (?, ?, ?)", (student_name, book_name, refund_date))
        # to Update book_status in dataBase
        pen.execute("UPDATE books SET book_status='1' WHERE book_name = ?", (book_name,))
        connection.commit()

        alert1.setText("successful !")
        QTest.qWait(500)
        self.close()

    def icon(self):
        image = QIcon("book.png")
        self.setWindowIcon(image)

    def control(self):
        data = pen.execute("SELECT * FROM students")
        student_name = self.student_name.text()

        for i in data.fetchall():
            if student_name == i[1]:
                self.control_text.setText("Only one")

            elif student_name in i[1]:
                self.name = i[1]

                self.control_text.setText("Closest Searches are: " + self.name)


class new_refund(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Refund")

        self.icon()

        # Vertical layout
        self.vertical = QVBoxLayout()

        title = QLabel("Add New Refund")
        title.setFont(button_font)

        # Entry for the student name to be added
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Enter Student Name")

        # Entry for the book name to be added
        self.book_name = QLineEdit()
        self.book_name.setPlaceholderText("Enter Book Name")

        # Save Button
        save = QPushButton("Save")
        save.clicked.connect(self.save)

        # Set Layout (Vertical)
        self.vertical.addWidget(title)
        self.vertical.addWidget(self.student_name)
        self.vertical.addWidget(self.book_name)
        self.vertical.addWidget(save)

        self.setLayout(self.vertical)

    def save(self):
        alert1 = QLabel("this may take a while. . . Please wait")

        self.vertical.addWidget(alert1)

        # To wait
        QTest.qWait(500)

        # Line edit Texts 'Entry'
        student_name = self.student_name.text()
        book_name = self.book_name.text()

        # Sending to dataBase
        pen.execute("DELETE FROM borrow WHERE student_name = ? AND book_name = ?", (student_name, book_name))
        pen.execute("UPDATE books SET book_status='0' WHERE book_name = ?", (book_name,))
        connection.commit()

        alert1.setText("successful !")
        QTest.qWait(500)
        self.close()

    def icon(self):
        image = QIcon("book.png")
        self.setWindowIcon(image)


# Side Window
class book_list(QWidget):

    def __init__(self):
        super().__init__()

        up_side(self)

        horizontal = QHBoxLayout()
        vertical = QVBoxLayout()

        title = QLabel("Book List")
        title.setFont(title_font)

        # Book information
        warning = QLabel("Click for more information")

        # Add list to book list
        liste = QListWidget()

        # New book button
        adding_book = QPushButton("Add New Book ")
        adding_book.setFont(title_font)
        adding_book.clicked.connect(self.add_new)

        # Get data to list
        books = pen.execute("SELECT * FROM books")

        for i in books.fetchall():
            # Add items to the list 'in book list'
            liste.addItem(i[1])

        liste.itemClicked.connect(self.book_info)

        vertical.addWidget(title)
        vertical.addWidget(warning)
        vertical.addWidget(liste)
        vertical.addWidget(adding_book)

        horizontal.addStretch()
        horizontal.addLayout(vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def book_info(self, item):

        book_name = item.text()
        control = pen.execute("SELECT * FROM books WHERE book_name = ?", (book_name,))
        status = control.fetchall()[0][2]

        # Is this book available for use? 'Control'
        if status == 0:
            self.icon()
            QMessageBox.information(self, "Book information", "The book named {} is ready for use".format(book_name))

        else:
            who = pen.execute("SELECT * FROM borrow WHERE book_name = ?", (book_name,))
            student = who.fetchall()[0][1]
            self.icon()
            QMessageBox.information(self, "Book Information", student + " has the book named " + book_name)

    def add_new(self):
        self.new = new_book()
        self.new.show()

    def icon(self):
        image = QIcon("book.png")
        self.setWindowIcon(image)

    def undo(self):
        self.close()


# Side Window
class student_list(QWidget):

    def __init__(self):
        super().__init__()

        up_side(self)

        horizontal = QHBoxLayout()
        vertical = QVBoxLayout()

        title = QLabel("Student List")
        title.setFont(title_font)

        # Student information
        warning = QLabel("Click for more information")

        # Add list to 'student name' list
        liste = QListWidget()

        # New student button
        adding_student = QPushButton("Add New Student ")
        adding_student.setFont(title_font)
        adding_student.clicked.connect(self.add_new)

        # Get data to list
        students = pen.execute("SELECT * FROM students")

        for i in students.fetchall():
            # Add items to the list 'in student list'
            liste.addItem(i[1])

        liste.itemClicked.connect(self.student_info)

        vertical.addWidget(title)
        vertical.addWidget(warning)
        vertical.addWidget(liste)
        vertical.addWidget(adding_student)

        horizontal.addStretch()
        horizontal.addLayout(vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def student_info(self, item):

        student_name = item.text()
        control = pen.execute("SELECT * FROM borrow WHERE student_name = ?", (student_name,))
        count = len(control.fetchall())

        # Is he/she reading anything ? 'control'
        if count == 0:
            self.icon()
            QMessageBox.information(self, "Student information", "Student Named {} Has No Book ".format(student_name))

        else:
            which = pen.execute("SELECT * FROM borrow WHERE student_name = ?", (student_name,))
            book = which.fetchall()[0][2]
            # First paramater has to be 'self' Second paramater is 'Window Title' and the Third one is 'Content the window'
            self.icon()
            QMessageBox.information(self, "Student information", student_name + " has the book named " + book)

    def undo(self):
        self.close()

    def icon(self):
        image = QIcon("book.png")
        self.setWindowIcon(image)

    def add_new(self):
        self.new = add_new_student()
        self.new.show()


# Side Window
class to_do_list(QWidget):

    def __init__(self):
        super().__init__()

        up_side(self)

        horizontal = QHBoxLayout()
        vertical = QVBoxLayout()

        # Time
        month = time.strftime("%m")
        day = time.strftime("%d")
        year = time.strftime("%Y")

        month = str(month)
        day = str(day)
        year = str(year)

        total = month + "/" + day + "/" + year

        title = QLabel("To-Do List")
        title.setFont(title_font)

        # Student information
        text = QLabel("These students should refund the book Today !")

        # Add list to 'student name' list
        liste = QListWidget()

        # Get data to list
        date = pen.execute("SELECT * FROM borrow")

        for i in date.fetchall():
            if i[3] == total:
                gonna_add = i[1] + " - " + i[2]
                liste.addItem(gonna_add)

        vertical.addWidget(title)
        vertical.addWidget(text)
        vertical.addWidget(liste)

        horizontal.addStretch()
        horizontal.addLayout(vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def undo(self):
        self.close()


# Side Window
class borrow_list(QWidget):

    def __init__(self):
        super().__init__()

        up_side(self)

        horizontal = QHBoxLayout()
        vertical = QVBoxLayout()

        # Main TİTLE
        title = QLabel("Borrowing")
        title.setFont(title_font)

        # Add list to 'student name' list
        liste = QListWidget()

        # to get borrow button and setFont
        get_borrow = QPushButton("Borrow")
        get_borrow.setFont(title_font)
        get_borrow.clicked.connect(self.add_new)

        # to refund the book button and setFont
        book_refund = QPushButton("Refund")
        book_refund.setFont(title_font)
        book_refund.clicked.connect(self.refund)

        # Get data to list
        gone = pen.execute("SELECT * FROM borrow")

        for i in gone.fetchall():
            # Add items to the list 'in borrowing "window" '
            gonna_add = i[1] + " - " + i[2]
            liste.addItem(gonna_add)

        vertical.addWidget(title)
        vertical.addWidget(liste)
        vertical.addWidget(get_borrow)
        vertical.addWidget(book_refund)

        horizontal.addStretch()
        horizontal.addLayout(vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def undo(self):
        self.close()

    def refund(self):
        self.new = new_refund()
        self.new.show()

    def add_new(self):
        self.new = new_borrowing()
        self.new.show()


# Side Window
class help_about(QWidget):
    def __init__(self):
        super().__init__()

        up_side(self)

        horizontal = QHBoxLayout()
        vertical = QVBoxLayout()

        title = QLabel("Help - About Me ")
        title.setFont(about_font)
        text = QLabel(".by Can Vural")
        text.setFont(about_font)

        vertical.addWidget(title)
        vertical.addStretch()
        vertical.addWidget(text)
        vertical.addStretch()

        horizontal.addStretch()
        horizontal.addLayout(vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

    def undo(self):
        self.close()


# Main Class - Main Window
class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Intro part
        self.begin = intro()
        self.begin.showFullScreen()
        QTest.qWait(2000)

        # To Close The Application
        quit_button = QPushButton("X", self)
        # it has to be a big font like 'title font'
        quit_button.setFont(title_font)
        quit_button.setGeometry(1300, 20, 50, 50)
        quit_button.clicked.connect(self.exit)

        horizontal = QHBoxLayout()
        vertical = QVBoxLayout()

        # Text
        title = QLabel("Library V1")
        title.setFont(title_font)

        # Main Buttons 'in main menu'
        book_button = QPushButton("Book List")
        student_button = QPushButton("Student List")
        trans_action_button = QPushButton("Borrowing")
        do_list_button = QPushButton("To-Do List")
        help_button = QPushButton("Help - About Me")

        # to Add font
        book_button.setFont(button_font)
        student_button.setFont(button_font)
        trans_action_button.setFont(button_font)
        do_list_button.setFont(button_font)
        help_button.setFont(button_font)

        # Connections of buttons
        book_button.clicked.connect(self.open_book)
        student_button.clicked.connect(self.open_st)
        trans_action_button.clicked.connect(self.open_borrow)
        do_list_button.clicked.connect(self.open_list)
        help_button.clicked.connect(self.open_help)

        # Horizontal Layout (adding)
        vertical.addWidget(title)
        vertical.addStretch()
        vertical.addWidget(book_button)
        vertical.addStretch()
        vertical.addWidget(student_button)
        vertical.addStretch()
        vertical.addWidget(trans_action_button)
        vertical.addStretch()
        vertical.addWidget(do_list_button)
        vertical.addStretch()
        vertical.addWidget(help_button)

        horizontal.addStretch()
        horizontal.addLayout(vertical)
        horizontal.addStretch()

        self.setLayout(horizontal)

        # to show window
        self.showFullScreen()

    def open_book(self):
        self.book = book_list()
        self.book.showFullScreen()

    def open_st(self):
        self.student = student_list()
        self.student.showFullScreen()

    def exit(self):
        qApp.quit()

    def open_borrow(self):
        self. trans_action = borrow_list()
        self.trans_action.showFullScreen()

    def open_list(self):
        self.doList = to_do_list()
        self.doList.showFullScreen()

    def open_help(self):
        self.help = help_about()
        self.help.showFullScreen()


application = QApplication(sys.argv)
window = Window()
sys.exit(application.exec_())
