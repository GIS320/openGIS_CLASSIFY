# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'meanshift_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

class MeanShift_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(362, 295)
        self.groupBox_parameter = QtWidgets.QGroupBox(Dialog)
        self.groupBox_parameter.setGeometry(QtCore.QRect(10, 150, 181, 81))
        self.groupBox_parameter.setFlat(False)
        self.groupBox_parameter.setCheckable(False)
        self.groupBox_parameter.setObjectName("groupBox_parameter")
        self.label_2 = QtWidgets.QLabel(self.groupBox_parameter)
        self.label_2.setGeometry(QtCore.QRect(10, 21, 101, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_parameter)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 101, 21))
        self.label_3.setObjectName("label_3")
        self.bandwidth_estimate = QtWidgets.QComboBox(self.groupBox_parameter)
        self.bandwidth_estimate.setGeometry(QtCore.QRect(120, 20, 51, 22))
        self.bandwidth_estimate.setEditable(True)
        self.bandwidth_estimate.setObjectName("bandwidth_estimate")
        self.bandwidth_estimate.addItem("")
        self.bandwidth_estimate.addItem("")
        self.bandwidth_estimate.addItem("")
        self.bandwidth_estimate.addItem("")
        self.bandwidth_estimate.addItem("")
        self.bandwidth_estimate.addItem("")
        self.bandwidth_estimate.addItem("")
        self.bandwidth_estimate.addItem("")
        self.bandwidth_estimate.addItem("")
        self.iter_num = QtWidgets.QComboBox(self.groupBox_parameter)
        self.iter_num.setGeometry(QtCore.QRect(120, 50, 51, 22))
        self.iter_num.setEditable(True)
        self.iter_num.setObjectName("iter_num")
        self.iter_num.addItem("")
        self.iter_num.addItem("")
        self.iter_num.addItem("")
        self.iter_num.addItem("")
        self.iter_num.addItem("")
        self.iter_num.addItem("")
        self.iter_num.addItem("")
        self.iter_num.addItem("")
        self.iter_num.addItem("")
        self.iter_num.addItem("")
        self.groupBox_path = QtWidgets.QGroupBox(Dialog)
        self.groupBox_path.setGeometry(QtCore.QRect(10, 20, 331, 101))
        self.groupBox_path.setObjectName("groupBox_path")
        self.output_file_browser = QtWidgets.QPushButton(self.groupBox_path)
        self.output_file_browser.setGeometry(QtCore.QRect(290, 60, 31, 21))
        self.output_file_browser.setObjectName("output_file_browser")
        self.label_4 = QtWidgets.QLabel(self.groupBox_path)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 72, 21))
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(self.groupBox_path)
        self.label.setGeometry(QtCore.QRect(10, 30, 72, 21))
        self.label.setObjectName("label")
        self.output_file_path = QtWidgets.QLineEdit(self.groupBox_path)
        self.output_file_path.setGeometry(QtCore.QRect(100, 60, 181, 21))
        self.output_file_path.setObjectName("output_file_path")
        self.input_file_path = QtWidgets.QLineEdit(self.groupBox_path)
        self.input_file_path.setGeometry(QtCore.QRect(100, 30, 181, 21))
        self.input_file_path.setObjectName("input_file_path")
        self.input_file_browser = QtWidgets.QPushButton(self.groupBox_path)
        self.input_file_browser.setGeometry(QtCore.QRect(290, 30, 31, 21))
        self.input_file_browser.setObjectName("input_file_browser")
        self.execute_button = QtWidgets.QPushButton(Dialog)
        self.execute_button.setGeometry(QtCore.QRect(250, 200, 93, 28))
        self.execute_button.setObjectName("execute_button")
        self.execute_progress = QtWidgets.QProgressBar(Dialog)
        self.execute_progress.setEnabled(False)
        self.execute_progress.setGeometry(QtCore.QRect(157, 250, 181, 23))
        self.execute_progress.setAutoFillBackground(False)
        self.execute_progress.setProperty("value", 24)
        self.execute_progress.setTextVisible(True)
        self.execute_progress.setObjectName("execute_progress")
        self.execute_log = QtWidgets.QLabel(Dialog)
        self.execute_log.setEnabled(False)
        self.execute_log.setGeometry(QtCore.QRect(20, 250, 72, 21))
        self.execute_log.setObjectName("execute_log")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MeanShift"))
        self.groupBox_parameter.setTitle(_translate("Dialog", "参数设置"))
        self.label_2.setText(_translate("Dialog", "带宽估计比例："))
        self.label_3.setText(_translate("Dialog", "迭代次数："))
        self.bandwidth_estimate.setItemText(0, _translate("Dialog", "0.1"))
        self.bandwidth_estimate.setItemText(1, _translate("Dialog", "0.15"))
        self.bandwidth_estimate.setItemText(2, _translate("Dialog", "0.2"))
        self.bandwidth_estimate.setItemText(3, _translate("Dialog", "0.25"))
        self.bandwidth_estimate.setItemText(4, _translate("Dialog", "0.3"))
        self.bandwidth_estimate.setItemText(5, _translate("Dialog", "0.35"))
        self.bandwidth_estimate.setItemText(6, _translate("Dialog", "0.4"))
        self.bandwidth_estimate.setItemText(7, _translate("Dialog", "0.45"))
        self.bandwidth_estimate.setItemText(8, _translate("Dialog", "0.5"))
        self.iter_num.setItemText(0, _translate("Dialog", "10"))
        self.iter_num.setItemText(1, _translate("Dialog", "20"))
        self.iter_num.setItemText(2, _translate("Dialog", "30"))
        self.iter_num.setItemText(3, _translate("Dialog", "40"))
        self.iter_num.setItemText(4, _translate("Dialog", "50"))
        self.iter_num.setItemText(5, _translate("Dialog", "60"))
        self.iter_num.setItemText(6, _translate("Dialog", "70"))
        self.iter_num.setItemText(7, _translate("Dialog", "80"))
        self.iter_num.setItemText(8, _translate("Dialog", "90"))
        self.iter_num.setItemText(9, _translate("Dialog", "100"))
        self.groupBox_path.setTitle(_translate("Dialog", "路径设置"))
        self.output_file_browser.setText(_translate("Dialog", "..."))
        self.label_4.setText(_translate("Dialog", "输出影像："))
        self.label.setText(_translate("Dialog", "输入影像："))
        self.input_file_browser.setText(_translate("Dialog", "..."))
        self.execute_button.setText(_translate("Dialog", "执行"))
        self.execute_log.setText(_translate("Dialog", "TextLabel"))
