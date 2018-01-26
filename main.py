from s3sync.py import S3Synchronizer

s3 = S3Sychronizer('/Users/shanehower/PycharmProjects','my-first-backup-bucket0328',2)
s3.start_upload()
