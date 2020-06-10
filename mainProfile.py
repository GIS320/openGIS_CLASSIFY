import os, sys
from qgis.core import QgsProject, QgsApplication, QgsVectorLayer, QgsRasterLayer, QgsLayerTreeModel, QgsMapLayerLegend, \
    QgsSimpleLegendNode, QgsLayerTreeLayer
from qgis.gui import QgsMapCanvas, QgsMapToolPan, QgsMapToolZoom, QgsLayerTreeMapCanvasBridge, QgsLayerTreeView
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QFileDialog, QMessageBox
from mypyqgis import Ui_MainWindow
from imgLayout import layerOut
from utils.mapTool import PolygonMapTool
from menuprovider import MenuProvider
from CommonHelper import CommonHelper
from utils.kmeans_component import KMeans_Component
from utils.meanshift_component import MeanShift_Component
from utils.dbscan_component import DBScan_Component
from utils.band_synthesis_component import Band_Synthesis_Component


def main():
    # 实例化QGIS应用对象
    qgs = QgsApplication([], True)
    qgs.setPrefixPath('qgis', True)  # 启动QGIS
    qgs.initQgis()
    window = MapExplorer()
    window.show()
    exit_code = qgs.exec_()
    # 退出QGIS
    maskList=os.listdir('mask')
    sampleList=os.listdir('samples')
    if len(maskList)!=0 or len(sampleList)!=0:
        reply = QMessageBox.question(None, '提示', '是否删除已有样区？', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            for file in maskList:
                path = os.path.join('mask', file)
                os.remove(path)
            for file in sampleList:
                path = os.path.join('samples', file)
                os.remove(path)
    qgs.exitQgis()
    sys.exit(exit_code)


class MapExplorer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MapExplorer, self).__init__()
        self.project = QgsProject()
        self.band_synthesis_window = Band_Synthesis_Component()
        self.kmeans_window = KMeans_Component()
        self.meanshift_window = MeanShift_Component()
        self.dbscan_window = DBScan_Component()
        self.setupUi(self)
        self.init_mapcanvas()
        self.slot_connect()
        self.init_layerTree()

        self.style_stand()

    def init_layerTree(self):
        self.layer_tree_view = QgsLayerTreeView(self)
        layout = QVBoxLayout(self.layerTreeWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.layer_tree_view)
        model = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot(), self)
        model.setFlag(QgsLayerTreeModel.AllowNodeRename)
        model.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        model.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
        model.setAutoCollapseLegendNodes(10)
        self.layer_tree_view.setModel(model)
        provider = MenuProvider(self.layer_tree_view, self.mapCanvas, self.project.instance())
        self.layer_tree_view.setMenuProvider(provider)

        # 注意self.layer_tree_bridge必须有
        self.layer_tree_bridge = QgsLayerTreeMapCanvasBridge(self.project.instance().layerTreeRoot(), self.mapCanvas)

    def slot_connect(self):
        self.actionopen_file.triggered.connect(self.action_open_triggered)
        self.actionzoom_in.triggered.connect(self.action_zoomin_triggered)
        self.actionzoom_out.triggered.connect(self.action_zoomout_triggered)
        self.actionpan.triggered.connect(self.action_pan_triggered)
        self.actionfull_extent.triggered.connect(self.action_fullextent_triggered)
        self.action_select.triggered.connect(self.action_select_triggered)
        self.actionsave.triggered.connect(self.action_save_triggered)
        self.mapdecoration.triggered.connect(self.mapDecoration_show)

        self.actionAqua.triggered.connect(self.style_Aqua)
        self.actionstand.triggered.connect(self.style_stand)
        self.actionConsoleStule.triggered.connect(self.style_ConsoleStyle)
        self.actionElegantDark.triggered.connect(self.style_ElegantDark)
        self.actionManjaroMix.triggered.connect(self.style_ManjaroMix)
        self.actionMaterialDark.triggered.connect(self.style_MaterialDark)
        self.actionUbuntu.triggered.connect(self.style_Ubuntu)

        self.action_KMeans.triggered.connect(self.action_KMeans_triggered)
        self.action_DBScan.triggered.connect(self.action_DBScan_triggered)
        self.action_MeanShift.triggered.connect(self.action_Meanshift_triggered)
        self.action_band_synthesis.triggered.connect(self.action_band_synthesis_triggered)
        self.kmeans_window.add_layer_signal.connect(self.action_add_kmeans_result)
        self.dbscan_window.add_layer_signal.connect(self.action_add_dbscan_result)
        self.meanshift_window.add_layer_signal.connect(self.action_add_meanshift_result)
        self.band_synthesis_window.add_layer_signal.connect(self.action_add_band_synthesis_result)

    def init_mapcanvas(self):
        # 实例化地图画布
        self.mapCanvas = QgsMapCanvas()
        self.mapCanvas.xyCoordinates.connect(self.show_lonlat)
        self.mapCanvas.setCanvasColor(QColor(60, 63, 65, 100))
        # self.mapCanvas.show()
        layout = QVBoxLayout(self.mapWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.mapCanvas)

    def loadMap(self, fullpath, classArray=None):
        print(fullpath[-3:-1] + fullpath[-1])
        imgClass = fullpath[-3:-1] + fullpath[-1]

        basename = os.path.splitext(os.path.basename(fullpath))[0]

        if imgClass == 'shp':
            self.layer = QgsVectorLayer(fullpath, basename, "ogr")
        else:
            self.layer = QgsRasterLayer(fullpath, basename)
        # 添加图例
        if classArray:
            self.node = QgsLayerTreeLayer(self.layer)
            # self.classArray = [{'name':'class1','color':QColor(0,0,0)},{'name':'class1','color':QColor(0,255,0)}]
            self.legend = CustomViewerLegend(classArray)
            self.legend.createLayerTreeModelLegendNodes(self.node)
            self.layer.setLegend(self.legend)
        # 注册图层
        self.project.instance().addMapLayer(self.layer)
        self.mapCanvas.setLayers([self.layer])
        # 设置图层范围
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()
        self.layer_tree_view.setCurrentLayer(self.layer)

    def action_open_triggered(self):
        fullpath, format = QFileDialog.getOpenFileName(self, '打开数据', '', '*.shp;;*.jpg;;*.png;;*.tif')
        if os.path.exists(fullpath):
            self.loadMap(fullpath)

    def action_save_triggered(self):
        fullpath, format = QFileDialog.getSaveFileName(self, '保存数据', '', '*.tif')
        if os.path.exists(fullpath):
            self.mapCanvas.saveAsImage(fullpath)

    def action_zoomin_triggered(self):
        self.maptool = QgsMapToolZoom(self.mapCanvas, False)
        self.mapCanvas.setMapTool(self.maptool)

    def action_zoomout_triggered(self):
        self.maptool = QgsMapToolZoom(self.mapCanvas, True)
        self.mapCanvas.setMapTool(self.maptool)

    def action_pan_triggered(self):
        self.maptool = QgsMapToolPan(self.mapCanvas)
        self.mapCanvas.setMapTool(self.maptool)

    def action_fullextent_triggered(self):
        self.mapCanvas.setExtent(self.layer.extent())
        self.mapCanvas.refresh()

    def action_select_triggered(self):
        self.maptool = PolygonMapTool(self)
        self.mapCanvas.setMapTool(self.maptool, True)
        self.mapCanvas.refresh()

    def mapDecoration_show(self):
        self.mapdecoration_dia = layerOut(QgsProject.instance(), self.qssStyleDia)
        self.mapdecoration_dia.show()

    # 显示鼠标点的经纬度信息
    def show_lonlat(self, point):
        x = point.x()
        y = point.y()
        self.statusbar.showMessage(f'经度:{x},纬度:{y}')

    def style_stand(self):
        styleFile = './QSS-master/style.qss'
        self.qssStyle = CommonHelper.readQSS(styleFile)
        self.qssStyleDia = CommonHelper.readQSS('./QSS-master/ElegantDark.qss')
        QMainWindow.setStyleSheet(self, self.qssStyle)

    def style_Aqua(self):
        styleFile = './QSS-master/Aqua.qss'
        self.qssStyle = CommonHelper.readQSS(styleFile)
        self.qssStyleDia = CommonHelper.readQSS(styleFile)
        QMainWindow.setStyleSheet(self, self.qssStyle)

    def style_ConsoleStyle(self):
        styleFile = './QSS-master/ConsoleStyle.qss'
        self.qssStyle = CommonHelper.readQSS(styleFile)
        self.qssStyleDia = CommonHelper.readQSS(styleFile)
        QMainWindow.setStyleSheet(self, self.qssStyle)

    def style_ElegantDark(self):
        styleFile = './QSS-master/ElegantDark.qss'
        self.qssStyle = CommonHelper.readQSS(styleFile)
        self.qssStyleDia = CommonHelper.readQSS(styleFile)
        QMainWindow.setStyleSheet(self, self.qssStyle)

    def style_ManjaroMix(self):
        styleFile = './QSS-master/ManjaroMix.qss'
        self.qssStyle = CommonHelper.readQSS(styleFile)
        self.qssStyleDia = CommonHelper.readQSS(styleFile)
        QMainWindow.setStyleSheet(self, self.qssStyle)

    def style_MaterialDark(self):
        styleFile = './QSS-master/MaterialDark.qss'
        self.qssStyle = CommonHelper.readQSS(styleFile)
        self.qssStyleDia = CommonHelper.readQSS(styleFile)
        QMainWindow.setStyleSheet(self, self.qssStyle)

    def style_Ubuntu(self):
        styleFile = './QSS-master/Ubuntu.qss'
        self.qssStyle = CommonHelper.readQSS(styleFile)
        self.qssStyleDia = CommonHelper.readQSS(styleFile)
        QMainWindow.setStyleSheet(self, self.qssStyle)

    def action_band_synthesis_triggered(self):
        self.band_synthesis_window.show()

    def action_KMeans_triggered(self):
        self.kmeans_window.show()

    def action_DBScan_triggered(self):
        self.dbscan_window.show()

    def action_Meanshift_triggered(self):
        self.meanshift_window.show()

    def action_add_kmeans_result(self, kmeans_img_path, layer_legends):
        self.loadMap(kmeans_img_path, layer_legends)

    def action_add_dbscan_result(self, dbscan_img_path, layer_legends):
        self.loadMap(dbscan_img_path, layer_legends)

    def action_add_meanshift_result(self, meanshift_img_path, layer_legends):
        self.loadMap(meanshift_img_path, layer_legends)

    def action_add_band_synthesis_result(self, multiband_img_path):
        self.loadMap(multiband_img_path)


class CustomViewerLegend(QgsMapLayerLegend):
    def __init__(self, classArray, parent=None):
        QgsMapLayerLegend.__init__(self, parent)
        self.classArray = classArray

    def createLayerTreeModelLegendNodes(self, layer_tree_layer):
        nodeArray = []
        for classItem in self.classArray:
            m = QgsSimpleLegendNode(layer_tree_layer, classItem['name'], self.createIcon(classItem['color']), self)
            nodeArray.append(m)
        return nodeArray

    def createIcon(self, color):
        pix = QPixmap(16, 16);
        pix.fill(color)
        return QIcon(pix)


if __name__ == '__main__':
    main()
