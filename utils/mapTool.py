from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox, QColorDialog, QFileDialog
from qgis.core import QgsWkbTypes, QgsGeometry, QgsVectorLayer, QgsField, QgsFeature, QgsVectorFileWriter, \
    QgsVectorDataProvider
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand
from qgis.PyQt.QtCore import Qt, QVariant
from osgeo import gdal
from utils.select_dialog import Select_Dialog
from utils.MyThread import MyThread
import os
import time
import threading
import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier


class PolygonMapTool(QgsMapToolEmitPoint):
    def __init__(self, MapExplorer):
        self.mainWindow = MapExplorer
        self.canvas = MapExplorer.mapCanvas
        self.rasterlayer = MapExplorer.layer
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, True)
        self.rubberBand.setColor(QColor(255, 0, 0))
        self.rubberBand.setWidth(1)
        self.tmpRubberBand = QgsRubberBand(self.canvas, True)
        self.tmpRubberBand.setColor(QColor(255, 0, 0))
        self.tmpRubberBand.setWidth(1)
        self.categories = []
        self.reset()
        self.methodsDict = {
            "最小距离": self.MinDistance,
            "最大似然": self.MaxLikelihood,
            "马氏距离": self.Mahalanobis,
            "支持向量机": self.SVM,
            "神经网络": self.ANN,
            "随机森林": self.RandomForest,
            "AdaBoost": self.AdaBoost
        }

    def reset(self):
        self.isEmittingPoint = False
        self.chooseComplete = False
        self.rubberBand.reset(QgsWkbTypes.PolygonGeometry)
        self.tmpRubberBand.reset(True)

    def canvasReleaseEvent(self, e):
        current_point = self.toMapCoordinates(e.pos())
        if e.button() == Qt.LeftButton:
            self.isEmittingPoint = True
            self.tmpRubberBand.addPoint(current_point, True)
        elif e.button() == Qt.RightButton:
            if self.tmpRubberBand.numberOfVertices() > 2:
                lineString = self.tmpRubberBand.asGeometry()  # type:QgsGeometry
                self.tmpRubberBand.reset(True)
                self.rubberBand.addGeometry(QgsGeometry.convertToType(lineString, QgsWkbTypes.PolygonGeometry))
                self.rubberBand.setColor(QColor(255, 0, 0, 50))
                self.rubberBand.show()
                self.isEmittingPoint = False
                self.chooseComplete = True

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return
        self.tmpRubberBand.removeLastPoint(doUpdate=False)
        point = self.toMapCoordinates(e.pos())
        self.tmpRubberBand.addPoint(point, True)

    def keyReleaseEvent(self, e):
        if self.isEmittingPoint:
            if e.key() == Qt.Key_Backspace:
                self.tmpRubberBand.removeLastPoint(doUpdate=True)
        if self.chooseComplete:
            if e.key() + 1 == Qt.Key_Enter:  # 为啥会差一呢
                self.saveMask()
                self.reset()
                reply = QMessageBox.question(None, '提示', '继续加入类别？', QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    for category in self.categories:
                        maskFile = f'mask/{category["name"]}_clip_mask.shp'
                        sampleFile = f'samples/{category["name"]}.tif'
                        if os.path.exists(sampleFile):
                            os.remove(sampleFile)
                        cmd = f'gdalwarp -of GTiff -cutline {maskFile} -cl {category["name"]}_clip_mask -crop_to_cutline -dstnodata 0 {self.rasterlayer.dataProvider().dataSourceUri()} {sampleFile}'
                        os.system(cmd)
                    dlg = Select_Dialog()
                    dlg.exec_()
                    self.methodsDict[dlg.chosen]()

    def saveMask(self):
        dlg = QInputDialog()
        dlg.setModal(True)
        text, okPressed = dlg.getText(None, "类别标记", "输入该样本类别名:", QLineEdit.Normal, "")
        while text == '':
            QMessageBox.warning(None, '输入警告', '未输入任何内容！')
            text, okPressed = dlg.getText(None, "类别标记", "输入该样本类别名:", QLineEdit.Normal, "")
        if okPressed:
            self.chooseComplete = False
            color = QColorDialog.getColor()
            maskLayer = QgsVectorLayer("Polygon", "clip_mask", "memory")
            maskLayer.setCrs(self.rasterlayer.crs())
            pr = maskLayer.dataProvider()  # type:QgsVectorDataProvider
            pr.addAttributes([QgsField("类别名", QVariant.String)])
            maskLayer.updateFields()
            fet = QgsFeature()
            print(self.rubberBand.asGeometry())
            fet.setGeometry(self.rubberBand.asGeometry())
            fet.setAttributes([text])
            pr.addFeatures([fet])
            maskLayer.updateExtents()
            maskFile = f'mask/{text}_clip_mask.shp'
            if os.path.exists(maskFile):
                os.remove(maskFile)  # 文件存在的话就替换一下
            QgsVectorFileWriter.writeAsVectorFormat(layer=maskLayer, fileName=maskFile, fileEncoding='utf-8',
                                                    destCRS=self.rasterlayer.crs(), driverName="ESRI Shapefile")
            self.categories.append({"name": text, "color": color})

    def MinDistance(self):
        count_categories = len(self.categories)  # 类别数
        raster_source = self.rasterlayer.dataProvider().dataSourceUri()  # 源图像地址
        raster_dataset = gdal.Open(raster_source)  # type:gdal.Dataset
        bandCount = raster_dataset.RasterCount
        raster_arr = raster_dataset.ReadAsArray()
        all_md = np.zeros(shape=(count_categories, raster_arr.shape[1], raster_arr.shape[2]), dtype=np.float64)
        for i in range(count_categories):
            category = self.categories[i]
            path = f'samples/{category["name"]}.tif'
            dataset_arr = gdal.Open(path).ReadAsArray()
            mask = np.all(dataset_arr == 0, axis=0)
            pixels = dataset_arr[:, ~mask]  # type:np.ndarray
            # shape of pixels:(bandCount,number of sample pixels)
            mean = np.mean(pixels, axis=1)
            # shape of mean:(bandCount,)
            raster_arr_minus_mean = raster_arr - mean.reshape(bandCount, 1, 1)
            md = (raster_arr_minus_mean ** 2).sum(axis=0)
            all_md[i, :, :] = md
        min_md = np.argmin(all_md, axis=0)
        classification_result = np.zeros(shape=(min_md.shape[0], min_md.shape[1], 3), dtype=np.int)
        for i in range(min_md.shape[0]):
            for j in range(min_md.shape[1]):
                classification_result[i, j, :] = self.categories[min_md[i, j]]["color"].getRgb()[:3]
        driver = gdal.GetDriverByName('GTiff')
        save_path, format = QFileDialog.getSaveFileName(None, '存储分类结果', '', '*.tif')
        out_ds = driver.Create(save_path, raster_dataset.RasterXSize, raster_dataset.RasterYSize, 3, gdal.GDT_Byte)
        out_ds.SetProjection(raster_dataset.GetProjection())
        out_ds.SetGeoTransform(raster_dataset.GetGeoTransform())
        for i in range(3):
            out_band = out_ds.GetRasterBand(i + 1)
            out_band.WriteArray(classification_result[:, :, i])
            out_band.ComputeStatistics(False)
        out_ds.FlushCache()
        self.mainWindow.loadMap(save_path, self.categories)

    def MaxLikelihood(self):
        count_categories = len(self.categories)  # 类别数
        raster_source = self.rasterlayer.dataProvider().dataSourceUri()  # 源图像地址
        raster_dataset = gdal.Open(raster_source)  # type:gdal.Dataset
        bandCount = raster_dataset.RasterCount
        raster_arr = raster_dataset.ReadAsArray()
        all_md = np.zeros(shape=(count_categories, raster_arr.shape[1], raster_arr.shape[2]), dtype=np.float64)
        for i in range(count_categories):
            category = self.categories[i]
            path = f'samples/{category["name"]}.tif'
            dataset_arr = gdal.Open(path).ReadAsArray()
            mask = np.all(dataset_arr == 0, axis=0)
            pixels = dataset_arr[:, ~mask]  # type:np.ndarray
            # shape of pixels:(bandCount,number of sample pixels)
            cov = np.cov(m=pixels, rowvar=True, bias=False)
            # shape of cov:(bandCount,bandCount)
            mean = np.mean(pixels, axis=1)
            # shape of mean:(bandCount,)
            raster_arr_minus_mean = raster_arr - mean.reshape(bandCount, 1, 1)
            tmp = np.tensordot(np.linalg.inv(cov), raster_arr_minus_mean, axes=[[1], [0]])
            md = (tmp * raster_arr_minus_mean).sum(axis=0) * (-0.5)
            all_md[i, :, :] = md
        max_md = np.argmax(all_md, axis=0)
        classification_result = np.zeros(shape=(max_md.shape[0], max_md.shape[1], 3), dtype=np.int)
        for i in range(max_md.shape[0]):
            for j in range(max_md.shape[1]):
                classification_result[i, j, :] = self.categories[max_md[i, j]]["color"].getRgb()[:3]
        driver = gdal.GetDriverByName('GTiff')
        save_path, format = QFileDialog.getSaveFileName(None, '存储分类结果', '', '*.tif')
        out_ds = driver.Create(save_path, raster_dataset.RasterXSize, raster_dataset.RasterYSize, 3, gdal.GDT_Byte)
        out_ds.SetProjection(raster_dataset.GetProjection())
        out_ds.SetGeoTransform(raster_dataset.GetGeoTransform())
        for i in range(3):
            out_band = out_ds.GetRasterBand(i + 1)
            out_band.WriteArray(classification_result[:, :, i])
            out_band.ComputeStatistics(False)
        out_ds.FlushCache()
        self.mainWindow.loadMap(save_path, self.categories)

    def Mahalanobis(self):
        count_categories = len(self.categories)  # 类别数
        raster_source = self.rasterlayer.dataProvider().dataSourceUri()  # 源图像地址
        raster_dataset = gdal.Open(raster_source)  # type:gdal.Dataset
        bandCount = raster_dataset.RasterCount
        raster_arr = raster_dataset.ReadAsArray()
        all_md = np.zeros(shape=(count_categories, raster_arr.shape[1], raster_arr.shape[2]), dtype=np.float64)
        for i in range(count_categories):
            category = self.categories[i]
            path = f'samples/{category["name"]}.tif'
            dataset_arr = gdal.Open(path).ReadAsArray()
            mask = np.all(dataset_arr == 0, axis=0)
            pixels = dataset_arr[:, ~mask]  # type:np.ndarray
            # shape of pixels:(bandCount,number of sample pixels)
            cov = np.cov(m=pixels, rowvar=True, bias=False)
            # shape of cov:(bandCount,bandCount)
            mean = np.mean(pixels, axis=1)
            # shape of mean:(bandCount,)
            raster_arr_minus_mean = raster_arr - mean.reshape(bandCount, 1, 1)
            tmp = np.tensordot(np.linalg.inv(cov), raster_arr_minus_mean, axes=[[1], [0]])
            md = (tmp * raster_arr_minus_mean).sum(axis=0)
            all_md[i, :, :] = md
        min_md = np.argmin(all_md, axis=0)
        classification_result = np.zeros(shape=(min_md.shape[0], min_md.shape[1], 3), dtype=np.int)
        for i in range(min_md.shape[0]):
            for j in range(min_md.shape[1]):
                classification_result[i, j, :] = self.categories[min_md[i, j]]["color"].getRgb()[:3]
        driver = gdal.GetDriverByName('GTiff')
        save_path, format = QFileDialog.getSaveFileName(None, '存储分类结果', '', '*.tif')
        out_ds = driver.Create(save_path, raster_dataset.RasterXSize, raster_dataset.RasterYSize, 3, gdal.GDT_Byte)
        out_ds.SetProjection(raster_dataset.GetProjection())
        out_ds.SetGeoTransform(raster_dataset.GetGeoTransform())
        for i in range(3):
            out_band = out_ds.GetRasterBand(i + 1)
            out_band.WriteArray(classification_result[:, :, i])
            out_band.ComputeStatistics(False)
        out_ds.FlushCache()
        self.mainWindow.loadMap(save_path, self.categories)

    def SVM(self):
        count_categories = len(self.categories)
        X = []
        Y = []
        for i in range(count_categories):
            category = self.categories[i]
            path = f'samples/{category["name"]}.tif'
            dataset_arr = gdal.Open(path).ReadAsArray()
            mask = np.all(dataset_arr == 0, axis=0)
            pixels = dataset_arr[:, ~mask]  # type:np.ndarray
            X.append(pixels)
            Y.append([i] * pixels.shape[1])
        X = np.concatenate(X, axis=1)
        Y = np.concatenate(Y)
        # clf = svm.SVC(decision_function_shape='ovo',C=1,kernel='rbf',degree=3,gamma='auto')
        clf = svm.SVC(decision_function_shape='ovo')
        time_start = time.time()
        clf.fit(X.transpose(), Y)
        time_end = time.time()
        print("totally cost", time_end - time_start)
        raster_source = self.rasterlayer.dataProvider().dataSourceUri()
        raster_dataset = gdal.Open(raster_source)  # type:gdal.Dataset
        raster_arr = raster_dataset.ReadAsArray()
        row = raster_arr.shape[1]
        col = raster_arr.shape[2]
        classification_result = np.zeros(shape=(row, col, 3))
        predicts = clf.predict(raster_arr.reshape((raster_arr.shape[0], -1)).transpose())
        for i in range(row):
            for j in range(col):
                classification_result[i, j, :] = self.categories[predicts[i * col + j]]['color'].getRgb()[:3]
        driver = gdal.GetDriverByName('GTiff')
        save_path, format = QFileDialog.getSaveFileName(None, '存储分类结果', '', '*.tif')
        out_ds = driver.Create(save_path, raster_dataset.RasterXSize, raster_dataset.RasterYSize, 3, gdal.GDT_Byte)
        out_ds.SetProjection(raster_dataset.GetProjection())
        out_ds.SetGeoTransform(raster_dataset.GetGeoTransform())
        for i in range(3):
            out_band = out_ds.GetRasterBand(i + 1)
            out_band.WriteArray(classification_result[:, :, i])
            out_band.ComputeStatistics(False)
        out_ds.FlushCache()
        self.mainWindow.loadMap(save_path, self.categories)

    def ANN(self):
        count_categories = len(self.categories)
        raster_source = self.rasterlayer.dataProvider().dataSourceUri()
        raster_dataset = gdal.Open(raster_source)  # type:gdal.Dataset
        raster_arr = raster_dataset.ReadAsArray()
        row = raster_arr.shape[1]
        col = raster_arr.shape[2]
        mean = np.mean(raster_arr, axis=(1, 2))
        sigma = np.std(raster_arr, axis=(1, 2))
        raster_arr = (raster_arr - mean.reshape(mean.shape[0], 1, 1)) / sigma.reshape(sigma.shape[0], 1, 1)
        X = []
        Y = []
        for i in range(count_categories):
            category = self.categories[i]
            path = f'samples/{category["name"]}.tif'
            dataset_arr = gdal.Open(path).ReadAsArray()
            mask = np.all(dataset_arr == 0, axis=0)
            pixels = dataset_arr[:, ~mask]  # type:np.ndarray
            X.append(pixels)
            Y.append([i] * pixels.shape[1])
        X = np.concatenate(X, axis=1)
        Y = np.concatenate(Y)
        X = (X - mean.reshape(mean.shape[0], 1)) / sigma.reshape(sigma.shape[0], 1)  # 标准化
        clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(30, 30), shuffle=True, random_state=1)
        time_start = time.time()
        clf.fit(X.transpose(), Y)
        time_end = time.time()
        print("totally cost", time_end - time_start)
        classification_result = np.zeros(shape=(row, col, 3))
        predicts = clf.predict(raster_arr.reshape((raster_arr.shape[0], -1)).transpose())
        for i in range(row):
            for j in range(col):
                classification_result[i, j, :] = self.categories[predicts[i * col + j]]['color'].getRgb()[:3]
        driver = gdal.GetDriverByName('GTiff')
        save_path, format = QFileDialog.getSaveFileName(None, '存储分类结果', '', '*.tif')
        out_ds = driver.Create(save_path, raster_dataset.RasterXSize, raster_dataset.RasterYSize, 3, gdal.GDT_Byte)
        out_ds.SetProjection(raster_dataset.GetProjection())
        out_ds.SetGeoTransform(raster_dataset.GetGeoTransform())
        for i in range(3):
            out_band = out_ds.GetRasterBand(i + 1)
            out_band.WriteArray(classification_result[:, :, i])
            out_band.ComputeStatistics(False)
        out_ds.FlushCache()
        self.mainWindow.loadMap(save_path, self.categories)

    def RandomForest(self):
        count_categories = len(self.categories)
        X = []
        Y = []
        for i in range(count_categories):
            category = self.categories[i]
            path = f'samples/{category["name"]}.tif'
            dataset_arr = gdal.Open(path).ReadAsArray()
            mask = np.all(dataset_arr == 0, axis=0)
            pixels = dataset_arr[:, ~mask]  # type:np.ndarray
            X.append(pixels)
            Y.append([i] * pixels.shape[1])
        X = np.concatenate(X, axis=1)
        Y = np.concatenate(Y)
        clf = RandomForestClassifier()
        time_start = time.time()
        clf.fit(X.transpose(), Y)
        time_end = time.time()
        print("totally cost", time_end - time_start)
        raster_source = self.rasterlayer.dataProvider().dataSourceUri()
        raster_dataset = gdal.Open(raster_source)  # type:gdal.Dataset
        raster_arr = raster_dataset.ReadAsArray()
        row = raster_arr.shape[1]
        col = raster_arr.shape[2]
        classification_result = np.zeros(shape=(row, col, 3))
        predicts = clf.predict(raster_arr.reshape((raster_arr.shape[0], -1)).transpose())
        for i in range(row):
            for j in range(col):
                classification_result[i, j, :] = self.categories[predicts[i * col + j]]['color'].getRgb()[:3]
        driver = gdal.GetDriverByName('GTiff')
        save_path, format = QFileDialog.getSaveFileName(None, '存储分类结果', '', '*.tif')
        out_ds = driver.Create(save_path, raster_dataset.RasterXSize, raster_dataset.RasterYSize, 3, gdal.GDT_Byte)
        out_ds.SetProjection(raster_dataset.GetProjection())
        out_ds.SetGeoTransform(raster_dataset.GetGeoTransform())
        for i in range(3):
            out_band = out_ds.GetRasterBand(i + 1)
            out_band.WriteArray(classification_result[:, :, i])
            out_band.ComputeStatistics(False)
        out_ds.FlushCache()
        self.mainWindow.loadMap(save_path, self.categories)

    def AdaBoost(self):
        count_categories = len(self.categories)
        X = []
        Y = []
        for i in range(count_categories):
            category = self.categories[i]
            path = f'samples/{category["name"]}.tif'
            dataset_arr = gdal.Open(path).ReadAsArray()
            mask = np.all(dataset_arr == 0, axis=0)
            pixels = dataset_arr[:, ~mask]  # type:np.ndarray
            X.append(pixels)
            Y.append([i] * pixels.shape[1])
        X = np.concatenate(X, axis=1)
        Y = np.concatenate(Y)
        clf = AdaBoostClassifier(n_estimators=50, random_state=0)
        time_start = time.time()
        clf.fit(X.transpose(), Y)
        time_end = time.time()
        print("totally cost", time_end - time_start)
        raster_source = self.rasterlayer.dataProvider().dataSourceUri()
        raster_dataset = gdal.Open(raster_source)  # type:gdal.Dataset
        raster_arr = raster_dataset.ReadAsArray()
        row = raster_arr.shape[1]
        col = raster_arr.shape[2]
        classification_result = np.zeros(shape=(row, col, 3))
        predicts = clf.predict(raster_arr.reshape((raster_arr.shape[0], -1)).transpose())
        for i in range(row):
            for j in range(col):
                classification_result[i, j, :] = self.categories[predicts[i * col + j]]['color'].getRgb()[:3]
        driver = gdal.GetDriverByName('GTiff')
        save_path, format = QFileDialog.getSaveFileName(None, '存储分类结果', '', '*.tif')
        out_ds = driver.Create(save_path, raster_dataset.RasterXSize, raster_dataset.RasterYSize, 3, gdal.GDT_Byte)
        out_ds.SetProjection(raster_dataset.GetProjection())
        out_ds.SetGeoTransform(raster_dataset.GetGeoTransform())
        for i in range(3):
            out_band = out_ds.GetRasterBand(i + 1)
            out_band.WriteArray(classification_result[:, :, i])
            out_band.ComputeStatistics(False)
        out_ds.FlushCache()
        self.mainWindow.loadMap(save_path, self.categories)

    def deactivate(self):
        super(PolygonMapTool, self).deactivate()
        self.deactivated.emit()
        self.reset()
