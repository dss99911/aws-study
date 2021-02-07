[Doc](https://docs.aws.amazon.com/firehose/latest/dev/writing-with-agents.html)
[Configuration Setting](https://docs.aws.amazon.com/firehose/latest/dev/writing-with-agents.html#agent-config-settings)

Start the agent manually. whenever config is changed. restart the service
```shell
sudo service aws-kinesis-agent start
sudo service aws-kinesis-agent stop
sudo service aws-kinesis-agent restart

```

(Optional) Configure the agent to start on system startup:
```shell
sudo chkconfig aws-kinesis-agent on
```

Configuration for Slackbot
```json
{
  "firehose.endpoint": "firehose.us-east-2.amazonaws.com",
  "cloudwatch.emitMetrics": "false",
  "flows": [
    {
      "filePattern": "/tmp/logs/app/slackbot-aya/kim.jeonghyeon.slackbotaya.*",
      "deliveryStream": "slackbot-aya-stream",
      "dataProcessingOptions": [
                {
                    "optionName": "LOGTOJSON",
                    "logFormat": "COMMONAPACHELOG",
                    "matchPattern": "^([\\d-]+ [\\d:.]+) - (.+?) - (.+?) - (.+?) - (.+?) - (.*)",
                    "customFieldNames": [ "time", "service", "thread", "logLevel", "logger", "message" ]
                }
            ]
    }
  ]
}
```