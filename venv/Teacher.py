from PyQt5.QtSql import QSqlQueryModel
from PyQt5.QtWidgets import QTableView, QMessageBox, QDialog, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout
import settings as st
import psycopg2

INSERT = '''INSERT INTO teacher(f_fio, f_phone, f_email, f_comment)
            VALUES ('%s', '%s', '%s', '%s');'''

SELECT_ONE = '''
            select f_fio, f_email, f_comment
            from teacher
            where id = '%s';
'''


UPDATE = '''
         update teacher set
         f_fio = '%s',
         f_phone = '%s',
         f_email = '%s',
         f_comment = '%s'
         where id = '%s';         
'''

DELETE = '''
         delete from teacher where id = '%s';
'''

class Model(QSqlQueryModel):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.obnovit()

    def obnovit(self):
        sql = '''
              select id, f_fio, f_email, f_comment
              from teacher
              '''
        self.setQuery(sql)


    def add(self, fio, phone, email, comment):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (fio, phone, email, comment)
        cursor.execute(INSERT, data)
        conn.commit()
        conn.close()
        self.obnovit()

    def update(self, id_teacher, fio, phone, email, comment):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (fio, phone, email, comment, id_teacher)
        cursor.execute(UPDATE, data)
        conn.commit()
        conn.close()
        self.obnovit()

    def delete(self, id_teacher):
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (id_teacher, )
        cursor.execute(DELETE, data)
        conn.commit()
        conn.close()
        self.obnovit()



class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        model = Model(parent=self)
        self.setModel(model)

        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.SingleSelection)
        self.hideColumn(0)
        self.setWordWrap(False)

        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.Fixed)

        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeToContents)
        hh.setSectionResizeMode(4, hh.Stretch)


    @pyqtSlot()
    def add(self):
        dia = Dialog(parent=self)
        if dia.exec():
            self.model().add(dia.fio, dia.phone, dia.email, dia.comment)


    @pyqtSlot()
    def update(self):
        dia = Dialog(parent=self)
        row = self.currentIndex().row()
        id_teacher = self.model().record(row).value(0)
        conn = psycopg2.connect(**st.db_params)
        cursor = conn.cursor()
        data = (id_teacher, )
        cursor.execute(SELECT_ONE, data)
        dia.fio, dia.phone, dia.email, dia.comment = cursor.fetchone()
        conn.close()
        if dia.exec():
           self.model().update(id_teacher, dia.fio, dia.phone, dia.email, dia.comment)



    @pyqtSlot()
    def delete(self):
        row = self.currentIndex().row()
        id_teacher = self.model().record(row).value(0)
        ans = QMessageBox.question(self, 'Учитель', 'Вы уверены?')
        if ans == QMessageBox.Yes:
            self.model().delete(id_teacher)

class Dialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Учитель')

        fio_lbl = QLabel('Фамилия И.О.', parent=self)
        self.__fio_edt = QLineEdit(parent=self)

        phone_lbl = QLabel('Телефон', parent=self)
        self.__phone_edt = QLineEdit(parent=self)

        email_lbl = QLabel('e-mail', parent=self)
        self.__email_edt = QLineEdit(parent=self)

        comment_lbl = QLabel('Примечание', parent=self)
        self.__comment_edt = QTextEdit(parent=self)

        ok_btn = QPushButton('OK', parent=self)
        cancel_btn = QPushButton('Отмена', parent=self)

        lay = QVBoxLayout(self)

        lay_fam = QVBoxLayout()
        lay_fam.setSpacing(0)
        lay_fam.addWidget(fio_lbl)
        lay_fam.addWidget(self.__fio_edt)
        lay.addLayout(lay_fam)

        lay3 = QHBoxLayout()

        lay_phone = QVBoxLayout()
        lay_phone.setSpacing(0)
        lay_phone.addWidget(phone_lbl)
        lay_phone.addWidget(self.__phone_edt)
        lay3.addLayout(lay_phone)

        lay_mail = QVBoxLayout()
        lay_mail.setSpacing(0)
        lay_mail.addWidget(email_lbl)
        lay_mail.addWidget(self.__email_edt)
        lay3.addLayout(lay_mail)

        lay.addLayout(lay3)

        lay_comm = QVBoxLayout
        lay_comm.setSpacing(0)
        lay_comm.addWidget(comment_lbl)
        lay_comm.addWidget(self.__comment_edt)
        lay.addLayout(lay_comm)

        lay2 = QHBoxLayout()
        lay2.addStretch()
        lay2.addWidget(ok_btn)
        lay2.addWidget(cancel_btn)
        lay.addLayout(lay2)

        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.finish)


    @pyqtSlot()
    def finish(self):
        if self.fio is None:
            return
        self.accept()

    @property
    def fio(self):
        result = self.__fio_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @fio.setter
    def fio(self, value):
        self.__fio_edt.setText(value)



    @property
    def phone(self):
        result = self.__phone_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @phone.setter
    def phone(self, value):
        self.__phone_edt.setText(value)

    @property
    def email(self):
        result = self.__email_edt.text().strip()
        if result == '':
            return None
        else:
            return result

    @email.setter
    def email(self, value):
        self.__email_edt.setText(value)

    @property
    def comment(self):
        result = self.__comment_edt.toPlainText().strip()
        if result == '':
            return None
        else:
            return result

    @comment.setter
    def comment(self, value):
        self.__comment_edt.setPlainText(value)
