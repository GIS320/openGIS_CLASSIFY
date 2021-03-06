import os,sys
import numpy as np
from osgeo import gdal
from utils.dbscan_dialog import DBScan_Dialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog,QFileDialog,QMessageBox
from PyQt5.QtGui import QColor
from sklearn.cluster import dbscan

class DBScan_Component(QDialog,DBScan_Dialog):
    add_layer_signal = pyqtSignal(str,list)
    color_list = [[238, 157, 168], [35, 148, 177], [181, 45, 43], [55, 60, 71], [6, 177, 152], [249, 2, 150],
                  [242, 43, 18], [98, 15, 53],
                  [110, 24, 225], [87, 121, 140], [255, 69, 83], [255, 0, 0], [0, 255, 0], [0, 0, 255], [220, 220, 220]]

    def __init__(self):
        super(DBScan_Component, self).__init__()
        self.setupUi(self)
        self.execute_log.setVisible(False)
        self.execute_progress.setVisible(False)
        self.slot_connect()

    def slot_connect(self):
        self.input_file_browser.clicked.connect(self.action_input_file_browser_clicked)
        self.output_file_browser.clicked.connect(self.action_output_file_browser_clicked)
        self.execute_button.clicked.connect(self.action_execute_button_clicked)

    def action_input_file_browser_clicked(self):
        input_path, type = QFileDialog.getOpenFileName(self, "导入待聚类影像", os.getcwd(), "*.tif;;*.jpg;;*.jpeg;;*.bmp;;*.png")
        self.input_file_path.setText(input_path)

    def action_output_file_browser_clicked(self):
        output_path, type = QFileDialog.getSaveFileName(self,"导出聚类影像",os.getcwd(), "*.tif")
        self.output_file_path.setText(output_path)

    def action_execute_button_clicked(self):
        #打开影像
        input_img = gdal.Open(self.input_file_path.text())
        img_rows = input_img.RasterYSize
        img_cols = input_img.RasterXSize
        img_bands=input_img.RasterCount
        img_geotrans = input_img.GetGeoTransform()
        img_proj = input_img.GetProjection()

        #将影像转为dbscan函数接受的数据格式
        input_features=[]
        for i in range(1, img_bands+1):
            band_img = input_img.GetRasterBand(i).ReadAsArray(0, 0, img_cols, img_rows)
            input_features.append(band_img.reshape(-1))
        input_features=np.array(input_features).T

        #执行dbscan算法
        dbscan_result=dbscan(input_features,eps=float(self.eps.currentText()),min_samples=int(self.minPts.currentText()))
        _, clustered_points = dbscan_result
        n_clusters = len(set(clustered_points)) - (1 if -1 in clustered_points else 0)

        #将各样本点灰度值转为对应聚类中心灰度值
        output_feature = []
        for index,item in enumerate(clustered_points):
            if item>0:
                while item>len(self.color_list)-1:
                    self.color_list.append(list(np.random.randint(256,size=3)))
                output_feature.append(self.color_list[item])
            else:
                output_feature.append([0,0,0])
        output_feature=np.array(output_feature).T
        output_feature = np.array(list(map(lambda x: x.reshape((img_rows, img_cols)), output_feature)))

        driver = gdal.GetDriverByName("GTiff")
        output_img=driver.Create(self.output_file_path.text(),img_cols,img_rows,3,gdal.GDT_Byte)
        output_img.SetGeoTransform(img_geotrans)
        output_img.SetProjection(img_proj)

        layer_legends = []  # 图例数组
        for i in range(n_clusters):
            layer_legends.append({'name': 'Cluster' + str(i + 1),
                                  'color': QColor(self.color_list[i][0], self.color_list[i][1],
                                                  self.color_list[i][2])})

        for i in range(1,4):
            output_img.GetRasterBand(i).WriteArray(output_feature[i-1])
        del output_img
        if (QMessageBox.question(self,"消息框","聚类完成，是否将结果添加到图层？",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)==QMessageBox.Yes):
            self.add_layer_signal.emit(self.output_file_path.text(),layer_legends)