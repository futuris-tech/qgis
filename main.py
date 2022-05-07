import qgis
from qgis.core import *

def print_points():
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
	
	
def print_nearest_points(x, y):
	app = QgsApplication([], True, None)
	app.setPrefixPath("/usr", True)
	app.initQgis()

	path_to_layer = "/home/ivan/qgis_sample_data/shapefiles/regions.shp"
	vlayer = QgsVectorLayer(path_to_layer, "Airports layer", "ogr")
	if not vlayer.isValid():
		print("Layer failed to load!")

	key = QgsGeometry.fromPointXY(QgsPointXY(x, y))

	for feature in vlayer.getFeatures():
		if (feature.hasGeometry()):
			p = feature.geometry().nearestPoint(key).asPoint()
			print(str(p.x()) + ' ' + str(p.y()))

	app.exitQgis()

print_nearest_points(727500, 4236000)
