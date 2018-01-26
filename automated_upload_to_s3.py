import os
import boto3


class S3Sychronizer:
    def __init__(self, path, bucket, sec):
        self.path = path
        self.bucket = bucket
        self.sec = sec

    def get_path(self):
        check_files = []
        for dir, subdir, files in os.walk(self.path):
            for file in files:
                if file != '.DS_Store':
                    check_files.append('{0}/{1}'.format(dir, file))
        return check_files

    def get_files_bucket(self):
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(self.bucket)

        files_in_bucket = []
        for object in my_bucket.objects.all():
            path, file_name = os.path.split(object.key)
            files_in_bucket.append('{0}/{1}'.format(path, file_name))
        return files_in_bucket

    def files_not_s3(self,check_files, files_in_bucket):
        upload_files = []
        for i in check_files:
            if i not in files_in_bucket:
                upload_files.append(i)
        return upload_files

    def start_upload(self,upload_files):
        s3_client = boto3.client('s3')
        
        if len(upload_files) > 0:
            for i in upload_files:
                s3_client.upload_file(i, self.bucket, i)
                print('File uploaded: {0}'.format(i))
        else:
            print('Not uploaded, no new files.')

