set -ex
sudo yum update -y

# docker
sudo yum install docker -y
sudo systemctl start docker.service

# python
python3 -m ensurepip --upgrade

# nginx
mkdir /home/ec2-user/static
mkdir /home/ec2-user/nginx
curl https://raw.githubusercontent.com/dss99911/aws-study/main/ec2/default.conf > /home/ec2-user/nginx/default.conf
sudo docker run -d \
  --restart unless-stopped \
  -p 80:80 \
  -v /home/ec2-user/static:/usr/share/nginx/html:ro \
  -v /home/ec2-user/nginx:/etc/nginx/conf.d:ro \
  nginx

# fingerprint ads
cat <<END >/home/ec2-user/static/app-ads.txt
google.com, pub-9477841224623557, DIRECT, f08c47fec0942fa0
END

# virtual memory
sudo /bin/dd if=/dev/zero of=/var/swap.1 bs=1M count=4048
sudo /sbin/mkswap /var/swap.1
sudo chmod 600 /var/swap.1
sudo /sbin/swapon /var/swap.1
echo "/var/swap.1   swap    swap    defaults        0   0" | sudo tee -a /etc/fstab


