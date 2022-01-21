import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea,QVBoxLayout, QHBoxLayout,
QTableWidget,QTableWidgetItem,
QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
import sys
class Window(QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("schedule")
        self.vbox = QVBoxLayout(self)
        self._connect_to_db()
        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)
        self._create_summar_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="ras",
                                     user="postgres",
                                     password="1",
                                     host="localhost",
                                     port="5432")
        self.cursor = self.conn.cursor()

    def _create_summar_tab(self):
        self.schedule_tab = QWidget()
        self.schedule_tab.refbutt = QPushButton("Refresh")
        self.schedule_tab.tabs = QTabWidget(self)
        self.schedule_tab.vbox = QVBoxLayout(self)
        self.schedule_tab.hbox = QHBoxLayout(self)
        self.schedule_tab.setLayout(self.schedule_tab.vbox)
        self.schedule_tab.vbox.addWidget(self.schedule_tab.tabs)
        self.schedule_tab.hbox.addWidget(self.schedule_tab.refbutt)
        self.schedule_tab.vbox.addLayout(self.schedule_tab.hbox)
        self.tabs.addTab(self.schedule_tab, "Schedule")
        self._create_day_tabs()
        self.schedule_tab.refbutt.clicked.connect(self.update_day_tables)
        self.subs_tab = QWidget()
        self.subs_tab.refbutt = QPushButton("Refresh")
        self.subs_tab.table = QTableWidget(self)
        self.subs_tab.vbox = QVBoxLayout(self)
        self.subs_tab.hbox = QHBoxLayout(self)
        self.subs_tab.setLayout(self.subs_tab.vbox)
        self.subs_tab.vbox.addWidget(self.subs_tab.table)
        self.subs_tab.hbox.addWidget(self.subs_tab.refbutt)
        self.subs_tab.vbox.addLayout(self.subs_tab.hbox)
        self.tabs.addTab(self.subs_tab, "Subjects")
        self._create_subs_table(self.subs_tab)
        self.subs_tab.refbutt.clicked.connect(self.update_sub_table)
        self.teachers_tab = QWidget()
        self.teachers_tab.refbutt = QPushButton("Refresh")
        self.teachers_tab.table = QTableWidget(self)
        self.teachers_tab.vbox = QVBoxLayout(self)
        self.teachers_tab.hbox = QHBoxLayout(self)
        self.teachers_tab.setLayout(self.teachers_tab.vbox)
        self.teachers_tab.vbox.addWidget(self.teachers_tab.table)
        self.teachers_tab.hbox.addWidget(self.teachers_tab.refbutt)
        self.teachers_tab.vbox.addLayout(self.teachers_tab.hbox)
        self.tabs.addTab(self.teachers_tab, "Teachers")
        self._create_teacher_table(self.teachers_tab)
        self.teachers_tab.refbutt.clicked.connect(self.update_teacher_table)

    def _create_subs_table(self, name):
        name.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        name.table.setColumnCount(3)
        name.table.setHorizontalHeaderLabels(["Subject", " ", " "])
        self.cursor.execute("SELECT * FROM subject")
        records = list(self.cursor.fetchall())
        name.table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            print(r)
            name.table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            name.table.joinButton = QPushButton("Join")
            name.table.deleteButton = QPushButton("Delete")
            name.table.setCellWidget(i, 1, name.table.joinButton)
            name.table.setCellWidget(i, 2, name.table.deleteButton)
            name.table.joinButton.clicked.connect(lambda: self.update_sub_row(i, name.table))
            name.table.deleteButton.clicked.connect(lambda: self.delete_sub_row(i, name.table))
        name.table.addButton = QPushButton("Add")
        name.table.setCellWidget(len(records), 1, name.table.addButton)
        name.table.addButton.clicked.connect(lambda: self.add_sub_row(len(records), name.table))


    def _create_teacher_table(self, name):
        name.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        name.table.setColumnCount(5)
        name.table.setHorizontalHeaderLabels(["ID", "Name", "Subject", " ", " "])
        self.cursor.execute("SELECT * FROM teacher")
        records = list(self.cursor.fetchall())
        name.table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            print(r)
            name.table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            name.table.item(i, 0).setFlags(name.table.item(i, 0).flags() ^ Qt.ItemIsEditable)
            name.table.setItem(i, 1,
                               QTableWidgetItem(str(r[1])))
            name.table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            name.table.joinButton = QPushButton("Join")
            name.table.deleteButton = QPushButton("Delete")
            name.table.setCellWidget(i, 3, name.table.joinButton)
            name.table.setCellWidget(i, 4, name.table.deleteButton)
            name.table.joinButton.clicked.connect(lambda: self.update_teacher_row(i, name.table))
            name.table.deleteButton.clicked.connect(lambda: self.delete_teacher_row(i, name.table))

        name.table.addButton = QPushButton("Add")
        name.table.setCellWidget(len(records), 3, name.table.addButton)
        name.table.addButton.clicked.connect(lambda: self.add_teacher_row(len(records), name.table))

    def _create_day_tabs(self):
        mon = self.schedule_tab.mon = QWidget()
        tue = self.schedule_tab.tue = QWidget()
        wed = self.schedule_tab.wed = QWidget()
        thu = self.schedule_tab.thu = QWidget()
        fri = self.schedule_tab.fri = QWidget()
        sat = self.schedule_tab.sat = QWidget()
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
        tabs = [mon, tue, wed, thu, fri, sat]
        for i in range(len(days)):
            self.schedule_tab.tabs.addTab(tabs[i], days[i])
            self._create_day_table(tabs[i], days[i])

    def _create_day_table(self, name, day):
        name.vbox = QVBoxLayout(self)
        name.table = QTableWidget()
        name.vbox.addWidget(name.table)
        name.setLayout(name.vbox)
        name.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        name.table.setColumnCount(7)
        name.table.setHorizontalHeaderLabels(["ID", "Day", "Subject", "Location", "Time", " ", " "])
        self.cursor.execute("SELECT id,day, subject,room_numb, start_time FROM timetable WHERE day=%s", (str(day),))
        records = list(self.cursor.fetchall())
        name.table.setRowCount(len(records) + 1)
        for i, r in enumerate(records):
            r = list(r)
            print(r)
            name.table.setItem(i, 0, QTableWidgetItem(str(r[0])))
            name.table.item(i, 0).setFlags(name.table.item(i, 0).flags() ^ Qt.ItemIsEditable);
            name.table.setItem(i, 1, QTableWidgetItem(str(r[1])))
            name.table.setItem(i, 2, QTableWidgetItem(str(r[2])))
            name.table.setItem(i, 3, QTableWidgetItem(str(r[3])))
            name.table.setItem(i, 4, QTableWidgetItem(str(r[4])))
            name.table.joinButton = QPushButton("Join")
            name.table.deleteButton = QPushButton("Delete")
            name.table.setCellWidget(i, 5, name.table.joinButton)
            name.table.setCellWidget(i, 6, name.table.deleteButton)
            name.table.joinButton.clicked.connect(lambda: self.update_day_row(i, name.table))
            name.table.deleteButton.clicked.connect(lambda: self.delete_day_row(i, name.table))

        name.table.addButton = QPushButton("Add")
        name.table.setCellWidget(len(records), 5, name.table.addButton)
        name.table.addButton.clicked.connect(lambda: self.add_day_row(len(records), name.table))

    def update_day_row(self, rowNumb, tname):
        row = list()
        for i in range(tname.columnCount()):
            try:
                row.append(tname.item(rowNumb, i).text())
            except:
                row.append(None)
        print(row)
        try:
            self.cursor.execute("UPDATE timetable SET day=%s, subject=%s ,room_num=%s ,start_time=%s::time without time zone WHERE id=%s",(str(row[1]), str(row[2]), str(row[3]), str(row[4]), int(row[0])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Smth went wrong. Check table and try again")

    def add_day_row(self, rowNumb, tname):
        row = list()
        for i in range(tname.columnCount() - 1):
            try:
                row.append(tname.item(rowNumb, i + 1).text())
            except:
                row.append(None)
            print(row)
        try:
            self.cursor.execute("INSERT INTO timetable (day,subject,room_num,start_time) VALUES (%s,%s,%s,%s)",(str(row[0]), str(row[1]), str(row[2]), str(row[3])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Smth went wrong. Check table and try again")
        self.update_day_tables()

    def update_day_tables(self):
        self.schedule_tab.tabs.clear()
        self._create_day_tabs()

    def update_sub_table(self):
        self.subs_tab.table.clear()
        self._create_subs_table(self.subs_tab)

    def add_sub_row(self, rowNumb, tname):
        sub = tname.item(rowNumb, 0).text()
        self.cursor.execute("INSERT INTO subject (name) VALUES (%s)", (str(sub),))
        self.conn.commit()
        self.update_sub_table()

    def update_sub_row(self, rowNumb, tname):
        row = list()
        try:
            row.append(tname.item(rowNumb, 0).text())
        except:
            row.append(None)
        self.cursor.execute("SELECT * FROM subject")
        records = self.cursor.fetchall()
        print(records)
        try:
            x = str(records[rowNumb])
            x = x.replace("(", " ")
            x = x.replace(")", " ")
            x = x.replace(",", " ")
            x = x.replace("'", " ")
            x = x.strip()
            row.append(x)

        except:
            row.append(None)
        print(row)
        try:
            self.cursor.execute("UPDATE subject SET name=%s WHERE name=%s", (str(row[0]), str(row[1])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Smth went wrong. Check table and try again")

    def add_teacher_row(self, rowNumb, tname):
        row = list()
        for i in range(tname.columnCount() - 1):
            try:
                row.append(tname.item(rowNumb, i + 1).text())
            except:
                row.append(None)
        print(row)
        try:
            self.cursor.execute("INSERT INTO teacher (full_name, subject) VALUES (%s, %s)", (str(row[0]), str(row[1])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Smth went wrong. Check table and try again")
        self.update_teacher_table()

    def update_teacher_row(self, rowNumb, tname):
        row = list()
        for i in range(tname.columnCount()):
            try:
                row.append(tname.item(rowNumb, i).text())
            except:
                row.append(None)
        print(row)
        try:
            self.cursor.execute("UPDATE teacher SET full_name=%s, subject=%s WHERE id=%s",
                                (str(row[1]), str(row[2]), int(row[0])))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Smth went wrong. Check table and try again")

    def update_teacher_table(self):
        self.teachers_tab.table.clear()
        self._create_teacher_table(self.teachers_tab)

    def delete_day_row(self, rowNumb, tname):
        row = list()
        for i in range(tname.columnCount()):
            try:
                row.append(tname.item(rowNumb, i).text())
            except:
                row.append(None)
        print(row)
        try:
            self.cursor.execute(
                "DELETE FROM timetable WHERE day=%s AND subject=%s AND room_num=%s AND start_time=%s AND id=%s",
                (str(row[1]), str(row[2]), str(row[3]), str(row[4]), int(row[0])))
            self.conn.commit()
            self.update_day_tables()
        except:
            QMessageBox.about(self, "Error", "Smth went wrong. Check table and try again")
        self.update_day_tables()

    def delete_sub_row(self, rowNumb, tname):
        row = list()
        try:
            row.append(tname.item(rowNumb, 0).text())
        except:
            row.append(None)
        print(row)
        try:
            self.cursor.execute("DELETE FROM subject WHERE name=%s ", (str(row[0]),))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Smth went wrong. Check table and try again")
        self.update_sub_table()

    def delete_teacher_row(self, rowNumb, tname):
        row = list()
        for i in range(tname.columnCount()):
            try:
                row.append(tname.item(rowNumb, i).text())
            except:
                row.append(None)
        print(row)
        try:
            self.cursor.execute("DELETE FROM teacher WHERE full_name=%s AND subject=%s AND id=%s",
                                (str(row[1]), str(row[2]), int(row[0])))
            self.conn.commit()
        except:
             QMessageBox.about(self, "Error", "Smth went wrong. Check table and try again")
        self.update_teacher_table()


if __name__ =='__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.argv(app.exec_())