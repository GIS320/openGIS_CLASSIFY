# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'band_synthesis_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Band_Synthesis_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(352, 499)
        self.groupBox_path = QtWidgets.QGroupBox(Dialog)
        self.groupBox_path.setGeometry(QtCore.QRect(10, 20, 331, 101))
        self.groupBox_path.setObjectName("groupBox_path")
        self.label = QtWidgets.QLabel(self.groupBox_path)
        self.label.setGeometry(QtCore.QRect(10, 30, 72, 21))
        self.label.setObjectName("label")
        self.input_file_path = QtWidgets.QLineEdit(self.groupBox_path)
        self.input_file_path.setGeometry(QtCore.QRect(100, 30, 181, 21))
        self.input_file_path.setObjectName("input_file_path")
        self.input_file_browser = QtWidgets.QPushButton(self.groupBox_path)
        self.input_file_browser.setGeometry(QtCore.QRect(290, 30, 31, 21))
        self.input_file_browser.setObjectName("input_file_browser")
        self.add_img_button = QtWidgets.QPushButton(self.groupBox_path)
        self.add_img_button.setGeometry(QtCore.QRect(262, 60, 61, 28))
        self.add_img_button.setObjectName("add_img_button")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 130, 331, 241))
        self.groupBox.setObjectName("groupBox")
        self.raw_img_list = QtWidgets.QListWidget(self.groupBox)
        self.raw_img_list.setGeometry(QtCore.QRect(10, 20, 311, 211))
        self.raw_img_list.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.raw_img_list.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.raw_img_list.setProperty("showDropIndicator", True)
        self.raw_img_list.setDragEnabled(True)
        self.raw_img_list.setDragDropOverwriteMode(False)
        self.raw_img_list.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.raw_img_list.setViewMode(QtWidgets.QListView.ListMode)
        self.raw_img_list.setObjectName("raw_img_list")
        self.groupBox_path_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_path_2.setGeometry(QtCore.QRect(10, 380, 331, 101))
        self.groupBox_path_2.setObjectName("groupBox_path_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_path_2)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 72, 21))
        self.label_2.setObjectName("label_2")
        self.output_file_path = QtWidgets.QLineEdit(self.groupBox_path_2)
        self.output_file_path.setGeometry(QtCore.QRect(100, 30, 181, 21))
        self.output_file_path.setObjectName("output_file_path")
        self.output_file_browser = QtWidgets.QPushButton(self.groupBox_path_2)
        self.output_file_browser.setGeometry(QtCore.QRect(290, 30, 31, 21))
        self.output_file_browser.setObjectName("output_file_browser")
        self.execute_button = QtWidgets.QPushButton(self.groupBox_path_2)
        self.execute_button.setGeometry(QtCore.QRect(262, 60, 61, 28))
        self.execute_button.setObjectName("execute_button")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "波段合成"))
        self.groupBox_path.setTitle(_translate("Dialog", "路径设置"))
        self.label.setText(_translate("Dialog", "输入影像："))
        self.input_file_browser.setText(_translate("Dialog", "..."))
        self.add_img_button.setText(_translate("Dialog", "添加"))
        self.groupBox.setTitle(_translate("Dialog", "波段排序"))
        self.groupBox_path_2.setTitle(_translate("Dialog", "路径设置"))
        self.label_2.setText(_translate("Dialog", "输出影像："))
        self.output_file_browser.setText(_translate("Dialog", "..."))
        self.execute_button.setText(_translate("Dialog", "执行"))
