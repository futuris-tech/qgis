import sys
from qgis.core import*
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtCore import QSize

from typing import Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, Response

app1 = QgsApplication([], True, None)
app1.setPrefixPath("/usr", True)
app1.initQgis()
sys.path.append('/usr/share/qgis/python/plugins')
from processing.core.Processing import Processing
from processing.tools import *
name = ""

def f():
	vlayer = QgsVectorLayer(name, "Airports layer", "ogr")
	if not vlayer.isValid():
		return False

	Processing.initialize()
	vlayer2 = Processing.runAlgorithm("qgis:voronoipolygons", {
		'INPUT': vlayer,
		'OUTPUT': 'memory:'
	})['OUTPUT']
	Processing.deinitialize()

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
	img.save("out.png", "png")
	return True


app = FastAPI()
app1.exitQgis()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global name
    try:
        contents = await file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        name = file.filename
        await file.close()
        
    return {"message": f"Successfuly uploaded {file.filename}"}

@app.get("/result")
def result():
	result = f()
	if (result):
		return FileResponse("out.png")
	else:
		return "Layer failed to load!"
