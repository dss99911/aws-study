sudo yum update -y
sudo yum install docker -y
sudo service docker start
systemctl enable docker.service

#if doesn't create directory. docker create, and it's created by root permission
mkdir /home/ec2-user/static
sudo docker run -d \
  --restart unless-stopped \
  -p 80:80 \
  -v /home/ec2-user/static:/usr/share/nginx/html:ro \
  nginx