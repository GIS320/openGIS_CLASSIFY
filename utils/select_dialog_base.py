# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_dialog_base.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(500, 185)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.mindistButton = QtWidgets.QRadioButton(self.groupBox)
        self.mindistButton.setGeometry(QtCore.QRect(120, 40, 71, 16))
        self.mindistButton.setObjectName("mindistButton")
        self.svmButton = QtWidgets.QRadioButton(self.groupBox)
        self.svmButton.setGeometry(QtCore.QRect(120, 90, 83, 16))
        self.svmButton.setObjectName("svmButton")
        self.mahalanobisButton = QtWidgets.QRadioButton(self.groupBox)
        self.mahalanobisButton.setGeometry(QtCore.QRect(270, 40, 71, 16))
        self.mahalanobisButton.setChecked(True)
        self.mahalanobisButton.setObjectName("mahalanobisButton")
        self.annButton = QtWidgets.QRadioButton(self.groupBox)
        self.annButton.setGeometry(QtCore.QRect(270, 90, 71, 16))
        self.annButton.setObjectName("annButton")
        self.randomforestButton = QtWidgets.QRadioButton(self.groupBox)
        self.randomforestButton.setGeometry(QtCore.QRect(10, 88, 71, 16))
        self.randomforestButton.setObjectName("randomforestButton")
        self.adaboostButton = QtWidgets.QRadioButton(self.groupBox)
        self.adaboostButton.setGeometry(QtCore.QRect(400, 90, 71, 16))
        self.adaboostButton.setObjectName("adaboostButton")
        self.anotherButton = QtWidgets.QRadioButton(self.groupBox)
        self.anotherButton.setGeometry(QtCore.QRect(400, 40, 47, 16))
        self.anotherButton.setObjectName("anotherButton")
        self.maxlikelihoodButton = QtWidgets.QRadioButton(self.groupBox)
        self.maxlikelihoodButton.setGeometry(QtCore.QRect(10, 40, 71, 16))
        self.maxlikelihoodButton.setObjectName("maxlikelihoodButton")
        self.verticalLayout.addWidget(self.groupBox)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "监督分类方法"))
        self.mindistButton.setText(_translate("Dialog", "最小距离"))
        self.svmButton.setText(_translate("Dialog", "支持向量机"))
        self.mahalanobisButton.setText(_translate("Dialog", "马氏距离"))
        self.annButton.setText(_translate("Dialog", "神经网络"))
        self.randomforestButton.setText(_translate("Dialog", "随机森林"))
        self.adaboostButton.setText(_translate("Dialog", "AdaBoost"))
        self.anotherButton.setText(_translate("Dialog", "其他"))
        self.maxlikelihoodButton.setText(_translate("Dialog", "最大似然"))
        self.pushButton.setText(_translate("Dialog", "确认"))

