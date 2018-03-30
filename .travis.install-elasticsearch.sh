#!/bin/bash
function install_from_zip {
    wget $1 -O out
    unzip out
    sudo mv $2 /opt/$2
}

install_from_zip https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.5.2.zip elasticsearch-1.5.2
install_from_zip https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.2.3.zip elasticsearch-6.2.3
