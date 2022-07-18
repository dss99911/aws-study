#!/bin/bash

set -x -e

# link /home to mount
sudo cp -rp /home /mnt/
sudo rm -r /home
sudo ln -s /mnt/home /home

mkdir $HOME/tmp
export TMPDIR=$HOME/tmp

## spark nlp
echo -e 'export PYSPARK_PYTHON=/usr/bin/python3
export HADOOP_CONF_DIR=/etc/hadoop/conf
export SPARK_JARS_DIR=/usr/lib/spark/jars
export SPARK_HOME=/usr/lib/spark' >> $HOME/.bashrc && source $HOME/.bashrc

sudo python3 -m pip install --cache-dir $TMPDIR awscli boto spark-nlp

sudo yum -y update
sudo yum -y install yum-utils
sudo yum -y groupinstall development
sudo yum list python3*
sudo yum -y install python3 python3-dev python3-pip python3-virtualenv
sudo python -V
sudo python3 -V
sudo pip3 install --cache-dir $TMPDIR --upgrade pip

sudo pip3 install --cache-dir $TMPDIR -U pandas requests pyarrow


if grep isMaster /mnt/var/lib/info/instance.json | grep false;
then        
    echo "This is not master node, do nothing,exiting"
    set +x
    exit 0
fi

sudo pip3 install --cache-dir $TMPDIR -U awswrangler matplotlib beautifulsoup4 scikit-learn

set +x
