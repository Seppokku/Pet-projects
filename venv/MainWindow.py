import Teacher
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSlot
from MainMenu import MainMenu


class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)

        main_menu = MainMenu(parent=self)
        self.setMenuBar(main_menu)

        v = Teacher.View(parent=self)
        self.setCentralWidget(v)

        main_menu.about_qt.triggered.connect(self.about_qt)
        main_menu.about.triggered.connect(self.about)

        main_menu.add_teacher.triggered.connect(v.add)
        main_menu.del_teacher.triggered.connect(v.delete)
        main_menu.edt_teacher.triggered.connect(v.update)




    @pyqtSlot()
    def about(self):
        title = 'Управление заданиями для учащихся'
        text = 'Программа для управления задачами\n' \
               'и заданиями для учащихся школы'

        QMessageBox.about(self, title, text)

    @pyqtSlot()
    def about_qt(self):
        QMessageBox.aboutQt(self, 'Управление заданиями для учащихся')



