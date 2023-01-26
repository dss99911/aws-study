
## Storage Class
- Standard
- Standard-IA
- Glacier Deep Archive (잘 사용안하는 경우 사용)
  - 복사와 같은 과정인데 prefix 별로 벌크작업이 안되고,
    object listing -> 각 object 별로 restore 명령 실행 -> 하루 ~ 이틀 정도 지난 후 STANDARD 인지 확인 과정을 거쳐야 해서 매우 까다롭습니다. 거의 쓸일 없다고 생각하고 넣는 것입니다. 

### Storage Class Analysis
- bucket의 metrics 탭에서 확인 가능
- Create analytics configuration를 통해, 특정 prefix의 storage class별 사용량, 조회량등을 확인할 수 있음


### s3fs
- mount해서, 실제 File system인 것 처럼 사용.
- spark에서 s3에 바로 접근할 수 있는 이유가 이것.
- https://github.com/s3fs-fuse/s3fs-fuse
- goofys가 속도가 더 빠르다고 함. emr studio에서도 선택할 수 있음
  - https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-studio-magics.html
  ```shell
  sudo wget https://github.com/kahing/goofys/releases/latest/download/goofys -P /usr/bin/
  sudo chmod ugo+x /usr/bin/goofys
  ```
