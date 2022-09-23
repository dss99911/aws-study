# AWS  VPC, subnet, region, AZ

![img.png](img.png)


## Subnet
VPC안에 subnet이 존재한다.

## CIDR
- subnet의 ip address 할당 방식
- 기존에는 network address와 host address로 구분하고, class A~E 까지의 클래스를 나눠서 ip address를 할다앟였는데, 유연성이 떨어져서, 별도의 ip address할당 방식을 사용
```
198.168.32.0/24 198.168.32.0~198.168.32.255 = 256

198.168.33.0/24 198.168.33.0~198.168.33.255 = 256

198.168.34.0/24 198.168.34.0~198.168.34.255 = 256

198.168.35.0/24 198.168.35.0~198.168.35.255 = 256

198.168.32.0/22 198.168.32.0~198.168.35.255 = 1024(256*4)
```
- 위 4개의 할당 받은 subnet을 합쳐서, 묶는 것을 supernetting이라고 하고, `198.168.32.0/22`가 CIDR로 표현한 subnet의 대역폭. 22의 의미는 이진수 22개를 subnet으로 사용하고, subnet아래의 host들은 나머지 10개의 이진수로 할당 할 수 있게 함
https://dev.classmethod.jp/articles/vpc-3/

### public Subnet, private Subnet
- https://aws.amazon.com/ko/premiumsupport/knowledge-center/rds-connectivity-instance-subnet-vpc/
- public subnet에 있는 instance들은 public ip가 할당되어 접속이 가능


##EC2, RDS
- 특정 subnet에 속해있음
- Network Interface와 연결되어 있어서, Network Interface의 IP address로 접속 가능
  EC2
![img_1.png](img_1.png)

##RDS
![img_2.png](img_2.png)
##ELB
- 한 VPC안에 여러개의 subnet을 생성하고, network interface도 여러개 생성됨.
- ![img_3.png](img_3.png)

##Network Interfaces
- 하나의 subnet에 여러 Network Interface존재 가능
- 하나의 보안 그룹 설정하여, In/Out bound 설정 가능
![img_5.png](img_5.png)
- https://docs.aws.amazon.com/vpc/latest/privatelink/endpoint-services-overview.html
  - VPC외부의 서비스와 private하게 연결할 수 있음

## 탄력적 IP(elastic ip)
- Network Interface와 1:1대응(Network Interface는 탄력적 IP가 없을 수 있음
- public IP와 1:1 대응함.
- public ip는 동적 할당이라 바뀔 수 있는데, elastic ip는 정적으로 고정된 ip

## 보안그룹
-  VPC에 속함
![img_4.png](img_4.png)


## Region
- 지리적 분리된 것
  Availability Zone
- isolated location within each Region
- 어떤 문제가 발생해도,  격리되어 있어서, 특정 위치의 인스턴스에 문제가 발생해도, 다른 인스턴스에 영향이 가지 않게 물리적으로 처리해둔 영역
- 분산 시스템에서는 특정 한 노드에 문제가 발생할 경우, 다른 노드들 만으로도 돌아갈 수 있게 처리를 하는데, 보통 속도를 빠르게 하기 위해, 같은 지역에 여러 노드들을 둔다. 그런데, 만약 AZ가 같으면, 한 zone에 문제가 발생할 경우, 모든 노드가 마비되어, 분산시스템 자체에 문제가 발생할 수 있다.
- 그래서, zone을 격리시켜, 한 노드가 마비되었을 때, 다른 zone의 노드에는 영향이 없게 하여, 분산 시스템이 지속적으로 유지될 수 있게 한다.


## Peering
https://docs.aws.amazon.com/ko_kr/vpc/latest/peering/create-vpc-peering-connection.html
- private ip외에는 접근을 막은 경우, 다른 VPC에서 접근을 하고 싶을 때, peering이라는 것을 설정해서, 다른 VPC에서도 private ip로 접근이 가능하다.
- 보통 로컬에서의 접근은 VPN으로 VPC에 접근을 하게 해놓고, 서버 내부에서의 통신은 다른 VPC에서 접근할 경우, peering을 통해서 접근을 할 수 있게 한다
- 보통 VPC는 10.50.0.0/16 와 같이 CIDR을 통해 private ip 대역폭을 설정 가능
- peering이 정상 작동하기 위해서는 routing table에 특정 Ip대역폭은 해당 Peering을 이용하도록 설정한다.