import sys
import qgis
from qgis.core import*
from qgis.PyQt.QtGui import (
    QPolygonF,
    QColor,
)
from qgis.PyQt.QtCore import (
    QPointF,
    QRectF,
    QSize,
)

app = QgsApplication([], True, None)
app.setPrefixPath("/usr", True)
app.initQgis()

sys.path.append('/usr/share/qgis/python/plugins')
from processing.core.Processing import Processing
Processing.initialize()
from processing.tools import *

def f():
	path_to_layer = "input/airports.shp"
	vlayer = QgsVectorLayer(path_to_layer, "Airports layer", "ogr")
	if not vlayer.isValid():
		print("Layer failed to load!")
		return



	vlayer2 = Processing.runAlgorithm("qgis:voronoipolygons", {
		'INPUT': vlayer,
		'OUTPUT': 'memory:'
	})['OUTPUT']

	rect = vlayer2.extent()
	k = 3000 / (rect.width() + rect.height())

	settings = QgsMapSettings()
	settings.setLayers([vlayer, vlayer2])
	settings.setBackgroundColor(QColor(255, 255, 255))
	settings.setOutputSize(QSize(int(rect.width()*k), int(rect.height()*k)))
	settings.setExtent(vlayer.extent())
	render = QgsMapRendererSequentialJob(settings)
	render.start()
	render.waitForFinished()
	img = render.renderedImage()
	img.save("output/out.png", "png")
	print("Done!!!")

f()
Processing.deinitialize()
app.exitQgis()
