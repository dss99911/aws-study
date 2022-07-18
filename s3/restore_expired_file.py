import datetime
import boto3

# lifecycle에 의해, 삭제된 파일을 복구하는 방법.
# aws console에서 show versions를 하면, 삭제된 파일이 표시되는데,
# delete marker 타입으로 설정되어 있는 파일을 삭제하면,복구됨.

bucket = 'hyun'
s3cli = boto3.client('s3', region_name='ap-south-1')
bucket = boto3.resource('s3').Bucket(bucket)

res = s3cli.list_object_versions(
    Bucket=bucket,
    Prefix='temp/folder/')

last_modified = res['DeleteMarkers'][0]['LastModified']

del_markers = [{'key': item['Key'], 'version': item['VersionId']} for item in res['DeleteMarkers'] if item['LastModified'] == last_modified]

for del_item in del_markers:
    del_obj = bucket.Object(del_item['key'])
    del_obj.delete(VersionId=del_item['version'])