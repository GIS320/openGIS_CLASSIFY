# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapdecoration.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_decorationDialog(object):
    def setupUi(self, decorationDialog):
        decorationDialog.setObjectName("decorationDialog")
        decorationDialog.resize(1199, 822)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(decorationDialog)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.widget = QtWidgets.QWidget(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet("background-color:white;")
        self.widget.setObjectName("widget")
        self.horizontalLayout_7.addWidget(self.widget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(decorationDialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(300, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.addMap = QtWidgets.QPushButton(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addMap.sizePolicy().hasHeightForWidth())
        self.addMap.setSizePolicy(sizePolicy)
        self.addMap.setMaximumSize(QtCore.QSize(80, 16777215))
        self.addMap.setObjectName("addMap")
        self.horizontalLayout.addWidget(self.addMap)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_6 = QtWidgets.QLabel(decorationDialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_9.addWidget(self.label_6)
        self.effect = QtWidgets.QComboBox(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.effect.sizePolicy().hasHeightForWidth())
        self.effect.setSizePolicy(sizePolicy)
        self.effect.setMinimumSize(QtCore.QSize(200, 0))
        self.effect.setMaximumSize(QtCore.QSize(300, 16777215))
        self.effect.setObjectName("effect")
        self.horizontalLayout_9.addWidget(self.effect)
        self.changeEffect = QtWidgets.QPushButton(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.changeEffect.sizePolicy().hasHeightForWidth())
        self.changeEffect.setSizePolicy(sizePolicy)
        self.changeEffect.setMaximumSize(QtCore.QSize(80, 16777215))
        self.changeEffect.setObjectName("changeEffect")
        self.horizontalLayout_9.addWidget(self.changeEffect)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.getColor = QtWidgets.QPushButton(decorationDialog)
        self.getColor.setObjectName("getColor")
        self.horizontalLayout_6.addWidget(self.getColor)
        self.getFont = QtWidgets.QPushButton(decorationDialog)
        self.getFont.setObjectName("getFont")
        self.horizontalLayout_6.addWidget(self.getFont)
        self.deleteItem = QtWidgets.QPushButton(decorationDialog)
        self.deleteItem.setObjectName("deleteItem")
        self.horizontalLayout_6.addWidget(self.deleteItem)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(decorationDialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.title = QtWidgets.QLineEdit(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        self.title.setMinimumSize(QtCore.QSize(200, 0))
        self.title.setMaximumSize(QtCore.QSize(300, 16777215))
        self.title.setObjectName("title")
        self.horizontalLayout_2.addWidget(self.title)
        self.addTitle = QtWidgets.QPushButton(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addTitle.sizePolicy().hasHeightForWidth())
        self.addTitle.setSizePolicy(sizePolicy)
        self.addTitle.setMaximumSize(QtCore.QSize(80, 16777215))
        self.addTitle.setObjectName("addTitle")
        self.horizontalLayout_2.addWidget(self.addTitle)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(decorationDialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.addLegend = QtWidgets.QPushButton(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addLegend.sizePolicy().hasHeightForWidth())
        self.addLegend.setSizePolicy(sizePolicy)
        self.addLegend.setMaximumSize(QtCore.QSize(80, 16777215))
        self.addLegend.setObjectName("addLegend")
        self.horizontalLayout_3.addWidget(self.addLegend)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(decorationDialog)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.addScale = QtWidgets.QPushButton(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addScale.sizePolicy().hasHeightForWidth())
        self.addScale.setSizePolicy(sizePolicy)
        self.addScale.setMaximumSize(QtCore.QSize(80, 16777215))
        self.addScale.setObjectName("addScale")
        self.horizontalLayout_4.addWidget(self.addScale)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(decorationDialog)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.exportPDF = QtWidgets.QPushButton(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportPDF.sizePolicy().hasHeightForWidth())
        self.exportPDF.setSizePolicy(sizePolicy)
        self.exportPDF.setMaximumSize(QtCore.QSize(80, 16777215))
        self.exportPDF.setObjectName("exportPDF")
        self.horizontalLayout_5.addWidget(self.exportPDF)
        self.exportIMG = QtWidgets.QPushButton(decorationDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportIMG.sizePolicy().hasHeightForWidth())
        self.exportIMG.setSizePolicy(sizePolicy)
        self.exportIMG.setMaximumSize(QtCore.QSize(80, 16777215))
        self.exportIMG.setObjectName("exportIMG")
        self.horizontalLayout_5.addWidget(self.exportIMG)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7.addLayout(self.verticalLayout)

        self.retranslateUi(decorationDialog)
        QtCore.QMetaObject.connectSlotsByName(decorationDialog)

    def retranslateUi(self, decorationDialog):
        _translate = QtCore.QCoreApplication.translate
        decorationDialog.setWindowTitle(_translate("decorationDialog", "地图整饰"))
        self.label.setText(_translate("decorationDialog", "添加地图："))
        self.addMap.setText(_translate("decorationDialog", "添加"))
        self.label_6.setText(_translate("decorationDialog", "选择模式："))
        self.changeEffect.setText(_translate("decorationDialog", "确定"))
        self.getColor.setText(_translate("decorationDialog", "选择颜色"))
        self.getFont.setText(_translate("decorationDialog", "选择字体"))
        self.deleteItem.setText(_translate("decorationDialog", "删除元素"))
        self.label_2.setText(_translate("decorationDialog", "添加文本："))
        self.addTitle.setText(_translate("decorationDialog", "添加"))
        self.label_3.setText(_translate("decorationDialog", "添加 图例 ："))
        self.addLegend.setText(_translate("decorationDialog", "添加图例"))
        self.label_4.setText(_translate("decorationDialog", "添加比例尺："))
        self.addScale.setText(_translate("decorationDialog", "添加"))
        self.label_5.setText(_translate("decorationDialog", "输出 打印 ："))
        self.exportPDF.setText(_translate("decorationDialog", "输出pdf"))
        self.exportIMG.setText(_translate("decorationDialog", "输出img"))
