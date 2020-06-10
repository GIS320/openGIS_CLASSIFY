import os, sys
from qgis.core import QgsProject, QgsApplication, QgsVectorLayer,QgsRasterLayer,QgsLayerTreeModel,QgsLayerTreeNode,QgsMapLayer,\
    QgsLayout,QgsLayoutItemMap,QgsMapSettings,QgsRectangle,QgsLayoutSize,QgsUnitTypes,QgsPrintLayout,QgsLayoutItemLabel,QgsLayoutPoint,\
    QgsLayoutItemLegend,QgsLayerTree,QgsLayoutItemScaleBar,QgsLayoutItemPolygon,QgsFillSymbol,QgsLayoutExporter,QgsMapLayerLegend,QgsSimpleLegendNode,QgsLayerTreeLayer
from qgis.gui import QgsMapCanvas,QgsLayoutView,QgsPreviewEffect,QgsLayoutViewMouseEvent,QgsLayoutViewToolSelect,QgsLayoutViewToolEditNodes
from PyQt5.QtCore import Qt, QRectF, QCoreApplication,QPointF
from PyQt5.QtGui import QColor, QPalette, QFont, QPolygonF,QIcon
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QFileDialog, QMenu, QAction, QDialog, QFontDialog, QColorDialog
from mapdecoration import Ui_decorationDialog

from CommonHelper import CommonHelper

class layerOut(QDialog,Ui_decorationDialog):
    def __init__(self, proj,qssStyle):
        super(layerOut, self).__init__()
        self.setupUi(self)
        self.project = proj

        print(self.project)
        self.initLayerOut()
        self.slot_connect()

        self.font = QFont('Arial', 24)
        self.color = QColor('black')

        # styleFile = './QSS-master/ElegantDark.qss'
        # qssStyle = CommonHelper.readQSS(styleFile)
        QDialog.setStyleSheet(self, qssStyle)

    def initLayerOut(self):

        self.layout = QgsPrintLayout(self.project)
        self.layout.initializeDefaults()
        self.QgsLayerView = QgsLayoutView()
        self.QgsLayerView.setPreviewModeEnabled(True)
        self.QgsLayerView.setContentsMargins(0,0,0,0)
        # self.QgsLayerView.resize(800,600)
        self.QgsLayerView.setCurrentLayout(self.layout)
        self.QgsLayerView.setPreviewMode(QgsPreviewEffect.PreviewDeuteranope)
        # self.QgsLayerView.setPreviewMode(QgsPreviewEffect.PreviewMode)

        self.QgsLayerView.unlockAllItems()
        self.layout.refresh()
        self.QgsLayerView.cursorPosChanged.connect(self.show_lonlat)

        self.selectTool = QgsLayoutViewToolSelect(self.QgsLayerView)
        self.selectTool.setLayout(self.layout)

        Layout = QVBoxLayout(self.widget)
        Layout.setContentsMargins(0, 0, 0, 0)
        Layout.addWidget(self.QgsLayerView)

        for layer in self.project.mapLayers().values():
            self.comboBox.addItem(layer.name())

        self.effect.addItem('PreviewGrayscale')
        self.effect.addItem('PreviewMono')
        self.effect.addItem('PreviewProtanope')
        self.effect.addItem('PreviewDeuteranope')

    def slot_connect(self):
        self.addMap.clicked.connect(self.createMap)
        self.addTitle.clicked.connect(self.createTittle)
        self.addLegend.clicked.connect(self.createLegend)
        self.addScale.clicked.connect(self.createScaleBar)
        self.exportPDF.clicked.connect(self.saveAsPDF)
        self.exportIMG.clicked.connect(self.saveAsIMG)
        self.getFont.clicked.connect(self.setFont)
        self.getColor.clicked.connect(self.setColor)
        self.deleteItem.clicked.connect(self.deleteSelectItem)
        self.changeEffect.clicked.connect(self.setEffect)

    def createMap(self):
        try:
            self.map = QgsLayoutItemMap(self.layout)
            self.map.setLocked(False)
            self.map.attemptSetSceneRect(QRectF(8.5, 20, 200, 160))
            self.map.setFrameEnabled(True)

            layer = self.project.mapLayersByName(self.comboBox.currentText())[0]

            # layer.renderer().setRedBand(3)
            # layer.renderer().setGreenBand(2)
            # layer.renderer().setBlueBand(1)

            self.map.setLayers([layer])

            self.map.setBackgroundColor(QColor(255, 255, 255))
            self.map.zoomToExtent(layer.extent())
            self.layout.addItem(self.map)
        except:
            pass
        # polygon = QPolygonF()
        # polygon.append(QPointF(0.0, 0.0))
        # polygon.append(QPointF(100.0, 0.0))
        # polygon.append(QPointF(200.0, 100.0))
        # polygon.append(QPointF(100.0, 200.0))
        #
        # polygonItem = QgsLayoutItemPolygon(polygon, self.layout)
        # self.layout.addItem(polygonItem)
        #
        # props = {}
        # props["color"] = "green"
        # props["style"] = "solid"
        # props["style_border"] = "solid"
        # props["color_border"] = "black"
        # props["width_border"] = "10.0"
        # props["joinstyle"] = "miter"
        #
        # symbol = QgsFillSymbol.createSimple(props)
        # polygonItem.setSymbol(symbol)

    def createTittle(self):
        title = QgsLayoutItemLabel(self.layout)
        # title.setLocked(False)
        title.setText(self.title.text())
        title.setFont(self.font)
        title.setFontColor(self.color)
        title.adjustSizeToText()
        self.layout.addLayoutItem(title)
        title.attemptMove(QgsLayoutPoint(130, 5, QgsUnitTypes.LayoutMillimeters))

    def createLegend(self):
        try:
            legend = QgsLayoutItemLegend(self.layout)
            legend.setTitle("Legend")
            legend.setLinkedMap(self.map)  # map is an instance of QgsLayoutItemMap
            self.layout.addItem(legend)

            legend.attemptMove(QgsLayoutPoint(230, 15, QgsUnitTypes.LayoutMillimeters))
        except:
            pass

    def createScaleBar(self):
        try:
            scalebar = QgsLayoutItemScaleBar(self.layout)
            scalebar.setStyle('Line Ticks Up')
            scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
            scalebar.setNumberOfSegments(6)
            scalebar.setNumberOfSegmentsLeft(0)
            scalebar.setUnitsPerSegment(2)
            scalebar.setLinkedMap(self.map)
            scalebar.setUnitLabel('km')
            scalebar.setFont(QFont('Arial', 14))
            scalebar.update()
            self.layout.addLayoutItem(scalebar)
            scalebar.attemptMove(QgsLayoutPoint(180, 190, QgsUnitTypes.LayoutMillimeters))
        except:
            pass

    def saveAsPDF(self):
        fullpath, format = QFileDialog.getSaveFileName(self, '存储为pdf', '', '*.pdf')
        print(fullpath)
        exporter = QgsLayoutExporter(self.layout)
        exporter.exportToPdf(fullpath, QgsLayoutExporter.PdfExportSettings())

    def saveAsIMG(self):
        fullpath, format = QFileDialog.getSaveFileName(self, '存储为img', '', '*.jpg;;*.png')
        print(fullpath)
        exporter = QgsLayoutExporter(self.layout)
        exporter.exportToImage(fullpath, QgsLayoutExporter.ImageExportSettings())

    def setFont(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.font = font

    def setColor(self):
        self.color = QColorDialog.getColor()
        print(self.color)

    def show_lonlat(self, point):
        # print(point)
        self.mousePos = point

    def deleteSelectItem(self):
        print('delete...')
        # print(self.QgsLayerView.itemFocused())
        try:
            self.QgsLayerView.deleteSelectedItems()
        except:
            pass

    def setEffect(self):
        # self.effect.addItem('PreviewGrayscale')
        # self.effect.addItem('PreviewMono')
        # self.effect.addItem('PreviewProtanope')
        # self.effect.addItem('PreviewDeuteranope')
        if self.effect.currentText() == 'PreviewGrayscale':
            self.QgsLayerView.setPreviewMode(QgsPreviewEffect.PreviewGrayscale)
        elif self.effect.currentText() == 'PreviewMono':
            self.QgsLayerView.setPreviewMode(QgsPreviewEffect.PreviewMono)
        elif self.effect.currentText() == 'PreviewProtanope':
            self.QgsLayerView.setPreviewMode(QgsPreviewEffect.PreviewProtanope)
        elif self.effect.currentText() == 'PreviewDeuteranope':
            self.QgsLayerView.setPreviewMode(QgsPreviewEffect.PreviewDeuteranope)
