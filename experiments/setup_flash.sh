echo 'apt-get update'
sudo apt-get update
echo 'install pip'
sudo apt-get install python-setuptools python-dev build-essential
echo 'install git'
sudo apt-get install git
echo 'install protobuf'
sudo pip install protobuf
echo 'install bitarray'
sudo pip install bitarray
echo 'pull down codes'
sudo git clone code
echo 'git clone https://github.com/adegtiar/fawnlog'
sudo git clone https://github.com/adegtiar/fawnlog
echo 'install protobuf socketrpc'
sudo easy_install fawnlog/protobuf.socketrpc-1.3.2-py2.7.egg
echo 'start flash'
sudo python flash_service.py
