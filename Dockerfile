FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y gnupg software-properties-common && apt-get update && apt-get install wget && wget -qO - https://qgis.org/downloads/qgis-2021.gpg.key | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import && chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg && add-apt-repository "deb https://qgis.org/ubuntu $(lsb_release -c -s) main" && apt update && apt install -y qgis qgis-plugin-grass
COPY main.py /home/main.py
CMD cd /home && python3 main.py
