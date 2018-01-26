import boto3
import os, time

class S3Synchronizer:
    def __init__(self, path, bucket, sec):
        self.path = path
        self.bucket = bucket
        self.sec = sec

        # first get a list of all files in s3
        # this will be used to compare files in the desired directory
        # and files already uploaded in the bucket
        s3_resource = boto3.resource('s3')
        self.my_bucket = s3_resource.Bucket(self.bucket)

    def get_files_bucket(self):
        files_in_bucket = []
        for object in self.my_bucket.objects.filter(Prefix= self.path):
            path, file_name = os.path.split(object.key)
            files_in_bucket.append('{0}/{1}'.format(path, file_name))
        return files_in_bucket

    def get_folder_in_directory(self):
        folders = os.listdir(self.path)
        # now unpack the folders in the desired directory into a list
        clean_folders = []
        for i in folders:
            if i != '.DS_Store' and i != 'Anaconda':
                path_to_watch_folders_in_pycharm = str(self.path) + '/{0}'.format(i)
                clean_folders.append(path_to_watch_folders_in_pycharm)
        return clean_folders

    def get_files_in_directory(self,folders,files_in_bucket,):
        files = []
        # compare the two lists, files_in_bucket and new_dir (which is created below).
        # if there is a file that is not present in the bucket but is
        # present in the directory, upload that file to the bucket.
        for i in folders:
            # this is the last path to search. returns the list of files in each folder.
            new_dir = os.listdir(i)
            # Finally compare each value in the list new_dir with files_in_bucket.
            for j in new_dir:
                if j != '.DS_Store' and j != '.idea':
                    path_to_upload = '{0}/{1}'.format(i, j)
                    if path_to_upload not in files_in_bucket:
                        # must compare the full path so path_to_load is the path to the file we want to upload
                        files.append(path_to_upload)
        return files

    def start_upload(self,files):
        s3_client = boto3.client('s3')

        #run every x seconds
        print('sleeping')
        time.sleep(self.sec)

        # have to redefine these variables because the length changed and the new file
        # needs to be included
        if len(files) > 0:
            for i in files:
                s3_client.upload_file(i, self.bucket, i)
                print('Files uploaded onto s3: {0}'.format(i))
        else:
            print('Not uploaded. No new files.')


