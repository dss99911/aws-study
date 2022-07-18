#!/bin/bash

set -ex

sudo chmod a+rwx -R /sys/fs/cgroup/cpu,cpuacct
sudo chmod a+rwx -R /sys/fs/cgroup/devices

echo -e 'export PYSPARK_PYTHON=/usr/bin/python3
export HADOOP_CONF_DIR=/etc/hadoop/conf
export SPARK_JARS_DIR=/usr/lib/spark/jars
export SPARK_HOME=/usr/lib/spark' >> $HOME/.bashrc && source $HOME/.bashrc

# link /home to mount
sudo cp -rp /home /mnt/
sudo rm -r /home
sudo ln -s /mnt/home /home

mkdir $HOME/tmp
export TMPDIR=$HOME/tmp

sudo python3 -m pip install --cache-dir $TMPDIR awscli boto spark-nlp

set +x
