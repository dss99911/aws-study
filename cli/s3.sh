aws s3 cp {local path} {s3 path}
aws s3 cp {s3 path} {s3 path}
aws s3 cp {s3 path} {local path}
aws s3 sync {folder_path} s3://{bucket}/{folder_path}
aws s3 cp s3://Bucket/Folder LocalFolder --recursive
aws s3 cp a* a.zip # when using *, don't use ""