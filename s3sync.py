import os, time
import boto3


class S3Sychronizer:
    def __init__(self, path, bucket, sec):
        self.path = path
        self.bucket = bucket
        self.sec = sec

    def get_local_files(self):
        check_files = []
        for dir, subdir, files in os.walk(self.path):
            for file in files:
                if file != '.DS_Store':
                    check_files.append('{0}/{1}'.format(dir, file))
        return check_files

    def get_remote_files(self):
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

    def start_upload(self):
        s3_client = boto3.client('s3')

        while True:
            print('sleeping')
            time.sleep(self.sec)
            s3 = S3Sychronizer(self.path, self.bucket, self.sec)
            path = s3.get_local_files()
            bucket = s3.get_remote_files()
            files_to_upload = s3.files_not_s3(path, bucket)

            if len(files_to_upload) > 0:
                for i in files_to_upload:
                    s3_client.upload_file(i, self.bucket, i)
                    print('File uploaded: {0}'.format(i))
            else:
                print('Not uploaded, no new files.')


