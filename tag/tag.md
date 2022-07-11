https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html
- tag로 비용 확인하기
  - https://docs.amazonaws.cn/en_us/awsaccountbilling/latest/aboutv2/custom-tags.html
  - https://www.amazonaws.cn/en/new/2021/now-use-tags-track-allocate-amazon-sagemaker-studio-notebooks-costs/
  - megazone 서비스중 awsbilling이 있는데, 여기에서도 tag로 비용 관리 가능
    - aws billing을 megazone에 전적으로 위임하는 형태라, aws계정으로도, billing에 접근을 못한다고 함
    - 알람이나, api등의 기능이 없어서, 팀별 비용 알람등을 사용하기 쉽지 않음
- tag-based IAM policy restriction
  - https://docs.aws.amazon.com/ko_kr/emr/latest/ManagementGuide/emr-managed-iam-policies.html#manually-tagged-resources