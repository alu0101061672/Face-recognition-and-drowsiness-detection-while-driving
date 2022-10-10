FROM python:3.10
WORKDIR /code
RUN apt-get update && apt-get install -y build-essential cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev && pip3 install -U pip numpy && wget http://dlib.net/files/dlib-19.9.tar.bz2 && tar xvf dlib-19.9.tar.bz2 && cd dlib-19.9/ && mkdir build && cd build && cmake .. && cmake --build . --config Release && make install && ldconfig && cd .. && pkg-config --libs --cflags dlib-1
COPY ./requirements.txt /code/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .
ENTRYPOINT ["python3", "main.py"]