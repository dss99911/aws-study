#!/bin/sh

pushd /home/hadoop
n=0
e=5
until [ $n -ge $e ]
do
    sudo yum groupinstall -y "Development Tools" &&
    # cmake installation
    sudo yum -y install cmake3 && sudo ln -s /usr/bin/cmake3 /usr/bin/cmake &&
    # Install python36
    sudo yum -y install python37 python37-devel python37-libs python37-pip python37-setuptools python37-test python37-tools &&
    # Install pip packages - default
    sudo pip-3.7 install --upgrade pip
    sudo /usr/local/bin/pip3.7 install --no-deps geopandas==0.5.0 &&
    sudo /usr/local/bin/pip3.7 install pyproj==2.4.0 Fiona==1.8.9 pandas==0.23.4 Shapely==1.7.1 &&
    sudo /usr/local/bin/pip3.7 install boto3==1.9.145 slackclient==1.3.1 scikit-learn==0.20.3 scipy==1.2.1 geopy==1.19.0 matplotlib==3.0.3 tilemapbase==0.4.3 pyarrow==1.0.1 --use-feature=2020-resolver&&
    # Install pip packages - dataflow
    sudo /usr/local/bin/pip3.7 install cryptography==2.3.1 fire==0.1.3 sqlalchemy==1.3.3 pymysql==0.9.3 influxdb==5.2.2 &&
    # Install pip packages - etc
    sudo /usr/local/bin/pip3.7 install google-api-python-client==1.7.8 requests==2.21.0 beautifulsoup4==4.6.3 h3==3.6.4 &&
    break
    n=$[$n+1]
    sleep 5
done
if [ $n -eq $e ]
then
    exit 1
fi
popd
exit 0
