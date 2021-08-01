A VPC
    - EC2 a : VPN 연결하는 서버
B VPC
    - EC2 b : VPN 사용시의 network interface가 되는 서버
    - EC2 b2 : 실제 접속하고자 하는 서버.

EC2 a의 public ip로 open vpn에 연결
vpn에 등록된 ip로 접속시, vpn을 통해 접속하게 됨
EC2 b2가 vpn에 등록되었고, b2에 접속하려고 할 경우, EC2 b의 public ip로 접속하여, b2의 private ip로 접속하게 됨.

VPN에 연결하여, private ip로 접속하고 싶은 경우, EC2 b와 VPC가 같아야 하고, VPN에 해당 private ip가 등록되어야 함.

static IP addressing
https://openvpn.net/vpn-server-resources/assigning-a-static-vpn-client-ip-address-to-a-user/