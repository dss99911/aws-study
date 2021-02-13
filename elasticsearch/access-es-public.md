Elasticsearch Service를 VPC로 생성시, 외부에서 접속이 안됨.
외부에서 접속 할 수 있도록 하기 위한 진행 상황 설명

ec2에서 curl https://vpc-all-log-tuy2yuhu36tmxbaioql54ldfde.us-east-2.es.amazonaws.com 을 하면 응답이 옴

local 에서 위와 동일하게 하면, 대기중으로, 중간에 보안 그룹이 허용 안된 느낌이 듬.


nslookup vpc-all-log-tuy2yuhu36tmxbaioql54ldfde.us-east-2.es.amazonaws.com 을하면,
Address: 172.31.45.8 와 같이 나옴.

172.31.45.8 의 network interface 는 public ip주소를 갖지 않고, private ip 주소만 존재. 그런데, local에서도 172.31.45.8를 인지할 수 있는 이유는 잘 모르겠음

172.31.45.8에 public으로 접속할 수 있게 할 방법을 마련해줘야함.

load balancing으로 연결하면, http에러가 남.


https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-vpc.html#es-vpc-security

ES vpc로 설정햇을 때, public접근이 어려움
1. public으로 ES다시 생성할 수 있는지 확인
2. VPC로 했을 때, public접근 하려면 어떻게 하는지 확인


ec2에서 포트포워딩 하여, 접속 성공
https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-vpc.html#kibana-test
ssh -i {pem-file} ec2-user@{ec2-ip} -N -L 9200:vpc-all-log-tuy2yuhu36tmxbaioql54ldfde.us-east-2.es.amazonaws.com:443
- EC2에 https로 접속 허용
- 포트포워딩
- 접속

VPC내부에서 접속시 접속이 가능하다는 얘기인데.
왜 접속이 안되나 봤더니.. 로드 밸런싱 리스너 설정시에, 301로 영구 이동되는 걸로 설정한 적있는데, 이게 브라우저에 캐싱되어 있어서, 로드밸런서가 IP포워딩하는게 아니라, redirection을 계속 하고 있었고, 해당 url은 외부에서 접속이 안되니, 접속이 안됐던 것.. 아래 참조하여, 캐시 삭제함
https://stackoverflow.com/questions/9130422/how-long-do-browsers-cache-http-301s#:~:text=There%20is%20a%20very%20simple,to%20remove%20the%20cached%20redirection.

이제 접속하니, 아래와 같은 에러가 뜬다. http로 접속해서 에러가 난다는 것 같은데...
400 Bad Request
The plain HTTP request was sent to HTTPS port
대상 그룹에서 포트는 443으로 설정했는데, HTTP로 설정해놔서, 에러 발생. HTTPS접속시 443포트를 쓰지만, HTTPS가 443포트를 의미하는 건 아니라서, 443으로 평문 통신을 요청해서 그런듯..

