#!/bin/bash -v
function install_from_zip {
  INSTALL_PATH=/opt/es/$2
  if [ ! -d "$INSTALL_PATH" ]; then
    wget $1 -O out
    unzip out
    sudo mv $2 $INSTALL_PATH
  fi
  /opt/es/$2/bin/elasticsearch -Vv
  remove_if_erroneus $2

}

function install_from_targz {
  INSTALL_PATH=/opt/es/$2
  if [ ! -d "$INSTALL_PATH" ]; then
    wget $1 -O out
    tar -zxf out
    sudo mv $2 $INSTALL_PATH
  fi
  /opt/es/$2/bin/elasticsearch -Vv
  remove_if_erroneus $2
}

function remove_if_erroneus {
  if [ ! -f "/opt/es/$1/bin/elasticsearch" ]; then
    rm -rv /opt/es/$1
  fi
}

install_from_zip https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.16.zip elasticsearch-5.6.16
install_from_zip https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.8.12.zip elasticsearch-6.8.12
install_from_targz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.4.2-linux-x86_64.tar.gz elasticsearch-7.4.2
install_from_targz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.5.2-linux-x86_64.tar.gz elasticsearch-7.5.2
install_from_targz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-linux-x86_64.tar.gz elasticsearch-7.6.2
install_from_targz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.7.1-linux-x86_64.tar.gz elasticsearch-7.7.1
install_from_targz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.8.1-linux-x86_64.tar.gz elasticsearch-7.8.1
install_from_targz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.9.0-linux-x86_64.tar.gz elasticsearch-7.9.0
