FROM ubuntu:22.04
WORKDIR /code
ARG DEBIAN_FRONTEND=noninteractive
#RUN apt-get update && apt-get install -y python3-dev python3-pip wget python3-tk build-essential libgl1-mesa-dev libxkbcommon-x11-0 libxcb-keysyms1 libxcb-render-util0 libxcb-xinerama0 libxcb-icccm4 libxcb-image0 cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev && pip3 install -U pip numpy && wget http://dlib.net/files/dlib-19.9.tar.bz2 && tar xvf dlib-19.9.tar.bz2 && cd dlib-19.9/ && mkdir build && cd build && cmake .. && cmake --build . --config Release && make install && ldconfig && cd .. && pkg-config --libs --cflags dlib-1
RUN apt-get update && apt-get install -y python3-dev python3-pip wget python3-tk openssl libssl-dev libssl1.0 libgl1-mesa-dev libqt5x11extras5 tkMessageBox tkinter build-essential cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev && pip3 install -U pip numpy && wget http://dlib.net/files/dlib-19.9.tar.bz2 && tar xvf dlib-19.9.tar.bz2 && cd dlib-19.9/ && mkdir build && cd build && cmake .. && cmake --build . --config Release && make install && ldconfig && cd .. && pkg-config --libs --cflags dlib-1
COPY ./requirements.txt /code/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
# RUN useradd -u 8877 admin
# USER admin
ENTRYPOINT ["python3", "vehicleGeneral.py"]
#ENTRYPOINT ["python3", "vehicle.py", "00000000L", "Alba Cruz Torres"]