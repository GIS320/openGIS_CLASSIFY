"""
Copyright (c) 2018 Iqua Robotics SL
This program is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, either version 2 of
the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.
"""

"""
 Manages the context menu options of the layers
 when the user right-clicks on a layer of the layers panel.
"""

import logging

from qgis.gui import (QgsLayerTreeViewMenuProvider,
                      QgsLayerTreeViewDefaultActions,
                      QgsRendererPropertiesDialog,
                      QgsSingleBandPseudoColorRendererWidget,
                      QgsProjectionSelectionDialog
                      )

from qgis.core import QgsVectorFileWriter, QgsVectorLayer, QgsStyle, QgsCoordinateReferenceSystem
from PyQt5.QtWidgets import QMenu, QFileDialog, QDialog, QVBoxLayout, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import QFileInfo, Qt

logger = logging.getLogger(__name__)


class MenuProvider(QgsLayerTreeViewMenuProvider):

    def __init__(self, view, canvas, proj):
        QgsLayerTreeViewMenuProvider.__init__(self)
        self.view = view
        self.canvas = canvas
        self.proj = proj
        self.defActions = QgsLayerTreeViewDefaultActions(self.view)
        self.name = None

    def createContextMenu(self):
        if not self.view.currentLayer():
            return None
        layer = self.view.currentLayer()
        self.connect_signal_name()
        m = QMenu()
        m.addAction("Zoom to Layer", self.zoom_to_layer)
        m.addAction("Rename Layer", self.rename_layer)
        # we only offer the option to save layer if it is a vector layer and has a valid geometry
        if layer.type() == 0 and layer.geometryType() not in [3, 4]:
            m.addAction("Save Layer", self.save_layer)
        m.addAction("Remove Layer", self.remove_layer)
        # properties option only for vector or raster layers that are single band (0 or 1)
        if layer.type() != 1 or layer.rasterType() < 2:
            m.addAction("Properties", self.layer_properties)
        m.addAction("Select CRS", self.layer_crs)
        return m

    def zoom_to_layer(self):
        self.defActions.zoomToLayer(self.canvas)

    def rename_layer(self):
        self.name = self.view.currentLayer().name()
        self.defActions.renameGroupOrLayer()

    def name_changed(self, node, name):
        n = 0
        # check every layer
        for layer in self.proj.mapLayers().values():
            if layer.name() == name:
                n += 1
        # if exists more than one layer with the same name
        if n > 1:
            logger.error("More than one layer was found with this name")
            # set previous name
            self.view.currentLayer().setName(self.name)
            QMessageBox.critical(None,
                                 "Error in renaming",
                                 "More than one layer was found with this name. Please enter another name.",
                                 QMessageBox.Close)
        if name.rfind('/') != -1:
            if self.view.currentLayer().name() == name:
                name = name.replace('/', '')
                self.view.currentLayer().setName(name)
                QMessageBox.warning(None, "Warning", "Usage of '/' is forbidden \n\n You may use '\\' instead")

    def remove_layer(self):
        self.defActions.removeGroupOrLayer()

    def save_layer(self):
        layer = self.view.currentLayer()
        # if it is a vector layer and has a valid geometry
        if layer.type() == 0 and layer.geometryType() not in [3, 4]:
            layer_name, selected_filter = QFileDialog.getSaveFileName(None,
                                                                      'Save Layer',
                                                                      "",
                                                                      'Shapefile (*.shp);;KML (*.kml);;GPX (*.gpx)')
            if layer_name != '':

                if selected_filter == "Shapefile (*.shp)":

                    if not layer_name.endswith('.shp'):
                        layer_name = layer_name + '.shp'
                    ret = QgsVectorFileWriter.writeAsVectorFormat(layer, layer_name, "utf-8",
                                                                  QgsCoordinateReferenceSystem(4326,
                                                                                               QgsCoordinateReferenceSystem.EpsgCrsId),
                                                                  "ESRI Shapefile")
                    if ret == QgsVectorFileWriter.NoError:
                        logger.info(layer.name() + " saved to " + layer_name)
                    # After saving always delete layer and reload from saved file
                    renderer = layer.renderer()
                    file_info = QFileInfo(layer_name)
                    base_name = file_info.baseName()
                    vlayer = QgsVectorLayer(layer_name, base_name, "ogr")
                    if not vlayer.isValid():
                        logger.warning("Layer failed to load!")
                    vlayer.setRenderer(renderer.clone())
                    self.remove_layer()
                    self.proj.addMapLayer(vlayer)

                elif selected_filter == "KML (*.kml)":

                    if not layer_name.endswith('.kml'):
                        layer_name = layer_name + '.kml'
                    file_info = QFileInfo(layer_name)

                    QgsVectorFileWriter.writeAsVectorFormat(layer, layer_name, "utf-8",
                                                            QgsCoordinateReferenceSystem(4326,
                                                                                         QgsCoordinateReferenceSystem.EpsgCrsId),
                                                            "KML")
                elif selected_filter == "GPX (*.gpx)":

                    if not layer_name.endswith('.gpx'):
                        layer_name = layer_name + '.gpx'
                    ds_options = list()
                    ds_options.append("GPX_USE_EXTENSIONS=TRUE")  # Option needed to write gpx correctly
                    QgsVectorFileWriter.writeAsVectorFormat(layer, layer_name, "utf-8",
                                                            QgsCoordinateReferenceSystem(4326,
                                                                                         QgsCoordinateReferenceSystem.EpsgCrsId),
                                                            "GPX",
                                                            datasourceOptions=ds_options)

    def layer_properties(self):
        layer = self.view.currentLayer()
        # if it is a vector layer and has a valid geometry
        if layer.type() == 0 and layer.geometryType() not in [3, 4]:
            # wrap style dialog with the buttons ok and cancel so that we can apply changes
            dlg = QDialog()
            dlg.widget = QgsRendererPropertiesDialog(self.view.currentLayer(), QgsStyle.defaultStyle(), True)
            dlg.layout = QVBoxLayout(dlg)
            dlg.buttons = QDialogButtonBox(dlg)
            dlg.layout.addWidget(dlg.widget)
            dlg.layout.addWidget(dlg.buttons)
            dlg.buttons.setOrientation(Qt.Horizontal)
            dlg.buttons.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

            # set signals
            def on_style_edit_accept(d):
                # this will update the layer's style
                dlg.widget.onOK()
                dlg.accept()

            dlg.buttons.accepted.connect(lambda d=dlg: on_style_edit_accept(d))
            dlg.buttons.rejected.connect(dlg.reject)
            dlg.exec_()
            self.canvas.refresh()
        elif layer.type() == 1 and layer.rasterType() != 2:
            dlg = QDialog()
            dlg.widget = QgsSingleBandPseudoColorRendererWidget(layer)
            dlg.layout = QVBoxLayout(dlg)
            dlg.buttons = QDialogButtonBox(dlg)
            dlg.layout.addWidget(dlg.widget)
            dlg.layout.addWidget(dlg.buttons)
            dlg.buttons.setOrientation(Qt.Horizontal)
            dlg.buttons.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

            # set signals
            def on_rasterstyle_edit_accept(d):
                # this will update the layer's style
                renderer = dlg.widget.renderer()
                layer.setRenderer(renderer)
                dlg.accept()

            dlg.buttons.accepted.connect(lambda d=dlg: on_rasterstyle_edit_accept(d))
            dlg.buttons.rejected.connect(dlg.reject)
            dlg.exec_()
            self.canvas.refresh()
        elif layer.type() == 1 and layer.rasterType() == 2:
            logger.info("multiband")

    # TODO: Check that it really changes CRS
    def layer_crs(self):
        self.projection_selector = QgsProjectionSelectionDialog()
        self.projection_selector.exec()
        crs = (self.projection_selector.crs())
        layer = self.view.currentLayer()
        layer.setCrs(crs)
        self.zoom_to_layer()

    def connect_signal_name(self):
        # catch signal nameChanged on name_changed slot
        while True:
            try:
                if self.view.currentNode() is not None:
                    # disconnect function name_changed for signal nameChanged
                    self.view.currentNode().nameChanged.disconnect(self.name_changed)
                else:
                    break
            except TypeError:
                break
        if self.view.currentNode() is not None:
            # connect function name_changed on signal nameChanged
            self.view.currentNode().nameChanged.connect(self.name_changed)