echo 'apt-get update'
sudo apt-get update
echo 'install pip'
sudo apt-get install python-pip python-dev build-essential
echo 'install git'
sudo apt-get install git
echo 'install protobuf'
sudo pip install protobuf
echo 'install bitarray'
sudo pip install bitarray
echo 'git clone https://github.com/adegtiar/fawnlog'
git clone https://github.com/adegtiar/fawnlog
echo 'install protobuf socketrpc'
sudo easy_install fawnlog/protobuf.socketrpc-1.3.2-py2.7.egg
echo 'start sequencer'
sudo python fawnlog/fawnlog/get_token_service.py
