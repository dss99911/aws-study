# EMR

- EMR클러스터는 사용 완료 후, 종료 하는식으로 보통 쓰는 것 같음
- zeppelin 접속은 해당 포트를 열기만 해도 됨.
    - [ ] [disable anonymous](https://docs.aws.amazon.com/whitepapers/latest/teaching-big-data-skills-with-amazon-emr/step-2-disabling-anonymous-access.html)
    - vpn을 통해서만 접속하게 하는 걸 권장
- cluster hadoop 마스터 서버 접속방법
  - 22 포트 허용
  - `ssh -i {pem-file} hadoop@{master-server-ip}`
  - 클러스터의 요약 정보에 접속 방식 설명되어 있음
  ![img.png](img.png)
  

- [x] EMR에서 S3 접속하기 (자신의 s3는 기본 role에 등록되어 있음)
- [ ] glue를 통해, Hive로 sql쿼리해보기
- [ ] Athena 를 통해, s3의 