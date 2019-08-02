#!/bin/bash
function install_from_zip {
  INSTALL_PATH=/opt/es/$2
  if [ ! -d "$INSTALL_PATH" ]; then
    wget $1 -O out
    unzip out
    sudo mv $2 $INSTALL_PATH
    /opt/es/$2/bin/elasticsearch -Vv
  fi
}

function install_from_targz {
  INSTALL_PATH=/opt/es/$2
  if [ ! -d "$INSTALL_PATH" ]; then
    wget $1 -O out
    tar -zxf out
    sudo mv $2 $INSTALL_PATH
    /opt/es/$2/bin/elasticsearch -Vv
  fi
}

install_from_zip https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.16.zip elasticsearch-5.6.16
install_from_zip https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.8.2.zip elasticsearch-6.8.2
install_from_targz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.3.0-linux-x86_64.tar.gz elasticsearch-7.3.0
