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