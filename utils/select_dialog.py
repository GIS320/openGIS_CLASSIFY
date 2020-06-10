import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QButtonGroup, QMessageBox, QDialog
from utils.select_dialog_base import Ui_Dialog
class Select_Dialog(QDialog,Ui_Dialog):
    def __init__(self):
        super(QDialog, self).__init__()
        super(Ui_Dialog,self).__init__()
        super().setupUi(self)
        self.bg=QButtonGroup()
        self.bg.addButton(self.maxlikelihoodButton, 0)
        self.bg.addButton(self.mindistButton, 1)
        self.bg.addButton(self.mahalanobisButton,2)
        self.bg.addButton(self.anotherButton,3)
        self.bg.addButton(self.randomforestButton,4)
        self.bg.addButton(self.svmButton, 5)
        self.bg.addButton(self.annButton,6)
        self.bg.addButton(self.adaboostButton,7)
        self.pushButton.clicked.connect(self.submit)
    def submit(self):
        self.chosen=self.bg.checkedButton().text()
        self.close()
