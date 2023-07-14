from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtCore import pyqtSlot, pyqtSignal

class MainMenu(QMenuBar):

    teacher_mode_request = pyqtSignal()


    def __init__(self, parent=None):
        super().__init__(parent)

        teacher = self.addMenu('Учитель')
        self.__add_teacher = teacher.addAction('Добавить...')
        self.__edt_teacher = teacher.addAction('Редактировать...')
        self.__del_teacher = teacher.addAction('Удалить')

        help_menu = self.addMenu('Справка')
        self.__about = help_menu.addAction('О программе...')
        self.__about_qt = help_menu.addAction('О библиотеке Qt...')





    @property
    def about(self):
        return self.__about
    
    @property
    def about_qt(self):
        return self.__about_qt

    @property
    def add_teacher(self):
        return self.__add_teacher

    @property
    def edt_teacher(self):
        return self.__edt_teacher

    @property
    def del_teacher(self):
        return self.__del_teacher


    def set_mode_teacher(self, widget):
        self.__teacher_add.triggered.connect(widget.add)
        self.__teacher_edit.triggered.connect(widget.update)
        self.__teacher_delete.triggered.connect(widget.delete)
        self.__teacher_add.setEnabled(True)
        self.__teacher_edit.setEnabled(True)
        self.__teacher_delete.setEnabled(True)
        self.__teacher_menu_action.setEnabled(True)
        self.__teacher_menu_action.setVisible(True)