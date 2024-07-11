import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from qgis.PyQt.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.core import QgsProject, QgsVectorLayer
from .resources import *
from .tnm_builder_dialog import TNMBuilderDialog
import os.path
from .roadways_conversion import convert_roadways
from .receivers_conversion import convert_receivers
from .barriers_conversion import convert_barriers
from .terrain_lines_conversion import convert_terrain_lines

class TNMBuilder:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.actions = []
        self.menu = self.tr(u'&TNM Builder')
        self.toolbar = self.iface.addToolBar(u'TNMBuilder')
        self.toolbar.setObjectName(u'TNMBuilder')

    def tr(self, message):
        return QCoreApplication.translate('TNMBuilder', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)

        return action

    def initGui(self):
        icon_path = ':/plugins/tnm_builder/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'TNM Builder'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&TNM Builder'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        dialog = TNMBuilderDialog()
        dialog.show()
        result = dialog.exec_()
        if result:
            self.update_tnm_file(dialog)

    def update_tnm_file(self, dialog):
        existing_file_path = dialog.existingFileLineEdit.text()
        output_file_path = dialog.outputFileLineEdit.text()
        if not existing_file_path:
            QMessageBox.critical(None, "Error", "No existing TNM .txf file selected.")
            return
        if not output_file_path:
            QMessageBox.critical(None, "Error", "No output TNM .txf file selected.")
            return

        road_layer_id = dialog.roadLayerComboBox.currentData()
        receivers_layer_id = dialog.receiversLayerComboBox.currentData()
        buildings_layer_id = dialog.buildingsLayerComboBox.currentData()
        existing_barriers_layer_id = dialog.existingBarriersLayerComboBox.currentData()
        elevation_contours_layer_id = dialog.elevationContoursLayerComboBox.currentData()
        terrain_lines_layer_id = dialog.terrainLinesLayerComboBox.currentData()

        road_layer = QgsProject.instance().mapLayer(road_layer_id) if road_layer_id else None
        receivers_layer = QgsProject.instance().mapLayer(receivers_layer_id) if receivers_layer_id else None
        buildings_layer = QgsProject.instance().mapLayer(buildings_layer_id) if buildings_layer_id else None
        existing_barriers_layer = QgsProject.instance().mapLayer(existing_barriers_layer_id) if existing_barriers_layer_id else None
        elevation_contours_layer = QgsProject.instance().mapLayer(elevation_contours_layer_id) if elevation_contours_layer_id else None
        terrain_lines_layer = QgsProject.instance().mapLayer(terrain_lines_layer_id) if terrain_lines_layer_id else None

        # Read and parse the existing TNM .txf file
        tree = ET.parse(existing_file_path)
        root = tree.getroot()

        # Convert and update only if the corresponding layer is selected
        if road_layer:
            root = convert_roadways(root, road_layer)
        if receivers_layer:
            root = convert_receivers(root, receivers_layer)
        if buildings_layer or existing_barriers_layer:
            root = convert_barriers(root, buildings_layer, existing_barriers_layer)
        if elevation_contours_layer or terrain_lines_layer:
            root = convert_terrain_lines(root, elevation_contours_layer, terrain_lines_layer)

        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml_as_string)

        QMessageBox.information(None, "Success", "TNM .txf file updated successfully.")
