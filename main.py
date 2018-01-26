from automated_upload_to_s3.py import S3Synchronizer
import time

while True:
    print('sleeping')
    time.sleep(10)
    s3 = S3Sychronizer('/Users/shanehower/PycharmProjects','my-first-backup-bucket0328',10)
    path = s3.get_path()
    bucket = s3.get_files_bucket()
    files_to_upload = s3.files_not_s3(path,bucket)
    s3.start_upload(files_to_upload)    
