# qgis

```sudo docker build -t test3 .```

```sudo docker run -v /tmp/.X11-unix:/tmp/.X11-unix -v /home/ivan/docker/output:/home/output -v /home/ivan/docker/input:/home/input -e DISPLAY=$DISPLAY --rm test3```
