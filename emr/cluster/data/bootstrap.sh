#!/bin/bash

set -x -e

# link /home to mount
sudo cp -rp /home /mnt/
sudo rm -r /home
sudo ln -s /mnt/home /home

mkdir -p /mnt/usr/local/
sudo cp -rp /usr/local/lib /mnt/usr/local/
sudo cp -rp /usr/local/lib64 /mnt/usr/local/
sudo rm -r /usr/local/lib
sudo rm -r /usr/local/lib64
sudo ln -s /mnt/usr/local/lib /usr/local/lib
sudo ln -s /mnt/usr/local/lib64 /usr/local/lib64

# if use sudo, cache dir is /root/.cache/pip . and if use $HOME. it's /home/hadoop. and it's not able to use as the user is different
sudo mkdir -p /home/root/.cache/pip
export TMPDIR=/home/root/.cache/pip

## spark nlp
echo -e 'export PYSPARK_PYTHON=/usr/bin/python3
export HADOOP_CONF_DIR=/etc/hadoop/conf
export SPARK_JARS_DIR=/usr/lib/spark/jars
export SPARK_HOME=/usr/lib/spark' >> $HOME/.bashrc && source $HOME/.bashrc

sudo python3 -m pip install --cache-dir $TMPDIR awscli boto spark-nlp

sudo python -V
sudo python3 -V
sudo pip3 install --cache-dir $TMPDIR --upgrade pip

sudo pip3 install --cache-dir $TMPDIR -U pandas requests pyarrow boto3 torch


if grep isMaster /mnt/var/lib/info/instance.json | grep false;
then        
    echo "This is not master node, do nothing,exiting"
    set +x
    exit 0
fi

echo "This is master node"

sudo pip3 install --cache-dir $TMPDIR -U awswrangler matplotlib beautifulsoup4 scikit-learn

set +x
