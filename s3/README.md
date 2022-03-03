
## Storage Class
- Standard
- Standard-IA
- Glacier Deep Archive (잘 사용안하는 경우 사용)
  - 복사와 같은 과정인데 prefix 별로 벌크작업이 안되고,
    object listing -> 각 object 별로 restore 명령 실행 -> 하루 ~ 이틀 정도 지난 후 STANDARD 인지 확인 과정을 거쳐야 해서 매우 까다롭습니다. 거의 쓸일 없다고 생각하고 넣는 것입니다. 

### Storage Class Analysis
- bucket의 metrics 탭에서 확인 가능
- Create analytics configuration를 통해, 특정 prefix의 storage class별 사용량, 조회량등을 확인할 수 있음
