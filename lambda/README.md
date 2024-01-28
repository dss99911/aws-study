# AWS Lambda

## Lambda생성
- 블루프린트 : 어떤 용도에 맞추어, 미리 만들어진 스니펫.
    - Ex) Kinesis Firehose에서 Data transformation할 경우, 인풋과 아웃풋을 어떤식으로 설정하면 되는지 미리 형태를 제공해준다. 그래서, 로직만 변경하면 되도록 해놓음
- rupy, python, go, java, node, 등의 언어 선택 가능
-

테스트 input넣어서, 테스트 해볼 수 있음.
- Deploy를 눌러야, 수정된 코드가 반영되어, 테스트에서도 반영된다.
- Deploy만 해서는 실제 배포가 되는 건 아니고, 새 버전 발행을 눌러야 될 것 같은데, 확실한 건 아님.

모니터링에서 console.log로 찍은 값 확인 가능함.

## 람다로 EMR호출하기
https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/launch-a-spark-job-in-a-transient-emr-cluster-using-a-lambda-function.html


## 설정
- 안 쓰고 있어도, 최소 1개의 인스턴스는 켜놓을지, 꺼 놓을지 설정할 수 있음.
- 최대 병령 호출 가능 갯수가 제한 되어 있고, 요청을 통해 계정당 제한을 늘릴 수 있음


## cold start
https://aws.amazon.com/ko/blogs/korea/new-provisioned-concurrency-for-lambda-functions/
https://alphahackerhan.tistory.com/29 

## layer
- 다중 람다 function에서 코드 공유
- extension
  - used for monitoring, logging, or security check
- docker image를 layer로는 못 쓰는 듯
- 람다 함수를 image에서 생성한 경우, layer를 못 씀
https://docs.aws.amazon.com/lambda/latest/dg/invocation-layers.html?icmpid=docs_lambda_help
https://aws.amazon.com/blogs/compute/working-with-lambda-layers-and-extensions-in-container-images/
  - docker image에서 layer나 extension을 추가 하는 방법을 설명
