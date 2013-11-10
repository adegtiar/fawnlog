#!/bin/bash

DIR="protobuf-2.5.0"

echo "Install protobuf"
cd $DIR
./configure
make
make check
sudo make install
cd "python"
python setup.py build
python setup.py test
sudo python setup.py install
