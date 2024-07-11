import os
from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QFileDialog
from qgis.core import QgsProject, QgsVectorLayer

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'tnm_builder_dialog_base.ui'))

class TNMBuilderDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(TNMBuilderDialog, self).__init__(parent)
        self.setupUi(self)
        self.populate_layers()
        self.updateFileButton.clicked.connect(self.accept)
        self.browseExistingButton.clicked.connect(self.browse_existing_file)
        self.browseOutputButton.clicked.connect(self.browse_output_file)

    def populate_layers(self):
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            if isinstance(layer, QgsVectorLayer):
                self.roadLayerComboBox.addItem(layer.name(), layer.id())
                self.receiversLayerComboBox.addItem(layer.name(), layer.id())
                self.buildingsLayerComboBox.addItem(layer.name(), layer.id())
                self.existingBarriersLayerComboBox.addItem(layer.name(), layer.id())
                self.elevationContoursLayerComboBox.addItem(layer.name(), layer.id())
                self.terrainLinesLayerComboBox.addItem(layer.name(), layer.id())

    def browse_existing_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select existing TNM .txf File", "", "*.txf")
        if file_path:
            self.existingFileLineEdit.setText(file_path)

    def browse_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select output TNM .txf File", "", "*.txf")
        if file_path:
            self.outputFileLineEdit.setText(file_path)
