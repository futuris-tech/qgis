import qgis
from qgis.core import *

app = QgsApplication([], True, None)
app.setPrefixPath("/usr", True)
app.initQgis()

path_to_layer = "/home/ivan/QGIS-Sample-Data-master/qgis_sample_data/shapefiles/airports.shp"
vlayer = QgsVectorLayer(path_to_layer, "Airports layer", "ogr")
if not vlayer.isValid():
    print("Layer failed to load!")

for feature in vlayer.getFeatures():
	if (feature.hasGeometry()):
		print(feature.geometry())

app.exitQgis()
