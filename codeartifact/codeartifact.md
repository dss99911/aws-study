# CodeArtifact

pypi, maven, gradle, etc server

https://docs.aws.amazon.com/codeartifact/latest/ug/using-python.html


## Issues
### run on EMR bootstrap
```shell
# pip doesn't exist on sudo
sudo ln -s /usr/local/bin/pip3 /bin/pip
sudo aws codeartifact login --tool pip --region {add region}
```