# EMR Auto scaling

## Reference
- https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-scale-on-demand.html



## EMR managed scaling
- 특별한 경우 아니면, 이걸로 하는게 편할 듯
- 총 instance갯수, 총 core instance갯수, 총 on demand갯수만 설정 할 수 있음
  - instance type을 core나 task에 여러개 설정하기 위해서는 instance fleet으로 각 instance type별 weight를 지정해주면 되는 듯

## Custom automatic scaling
