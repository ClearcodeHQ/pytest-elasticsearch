#!/bin/bash
function install_from_zip {
    wget $1 -O out
    unzip out
    sudo mv $2 /opt/$2
    /opt/$2/bin/elasticsearch -Vv
}

function install_from_targz {
    wget $1 -O out
    tar -zxf out
    sudo mv $2 /opt/$2
    /opt/$2/bin/elasticsearch -Vv
}

install_from_zip https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.16.zip elasticsearch-5.6.16
install_from_zip https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.8.2.zip elasticsearch-6.8.2
install_from_targz https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.3.0-linux-x86_64.tar.gz elasticsearch-7.3.0
