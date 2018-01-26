import boto3
import os, time

class GetBucketFiles:
    def __init__(self, prefix_path, bucket):
        self.path = prefix_path
        self.bucket = bucket

        # first get a list of all files in s3
        # this will be used to compare files in the desired directory
        # and files already uploaded in the bucket
        s3_resource = boto3.resource('s3')
        self.my_bucket = s3_resource.Bucket(self.bucket)


    def get_files(self):
        files_in_bucket = []
        for object in self.my_bucket.objects.filter(Prefix= self.path):
            path, file_name = os.path.split(object.key)
            files_in_bucket.append('{0}/{1}'.format(path, file_name))
        return files_in_bucket

class GetPath:
    def __init__(self, path, bucket):
        self.path = path
        self.bucket = bucket
        self.folders = files = os.listdir(path)

    def get_folder_in_directory(self):
        # now unpack the folders in the desired directory into a list
        folders_in_dir = []
        for i in self.folders:
            if i != '.DS_Store' and i != 'Anaconda':
                path_to_watch_folders_in_pycharm = str(self.path) + '/{0}'.format(i)
                folders_in_dir.append(path_to_watch_folders_in_pycharm)
        return folders_in_dir

    def find_files_in_directory(self, folder):
        list_of_files = []
        bucket_files = GetBucketFiles(self.path,self.bucket).get_files()
        # compare the two lists, files_in_bucket and new_dir (which is created below).
        # if there is a file that is not present in the bucket but is
        # present in the directory, upload that file to the bucket.
        for i in folder:
            # this is the last path to search. returns the list of files in each folder.
            new_dir = os.listdir(i)
            # Finally compare each value in the list new_dir with files_in_bucket.
            for j in new_dir:
                if j != '.DS_Store' and j != '.idea':
                    path_to_upload = '{0}/{1}'.format(i, j)
                    if path_to_upload not in bucket_files:
                        # must compare the full path so path_to_load is the path to the file we want to upload
                        list_of_files.append(path_to_upload)
        return list_of_files

# boto3.client() used for uploading and downloading

class Run:
    def __init__(self, path, bucket, sec):
        self.path = path
        self.bucket = bucket
        self.sec = sec

    def start(self):
        s3_client = boto3.client('s3')
        get_path = GetPath(self.path, self.bucket)

        while True:
            #run every 12 hours
            print('sleeping')
            time.sleep(self.sec)

            # have to refine these variables because the length changed and the new file
            # needs to be included
            folders = get_path.get_folder_in_directory()
            desired_files = get_path.find_files_in_directory(folders)

            if len(desired_files) > 0:
                for i in desired_files:
                    s3_client.upload_file(i, self.bucket, i)
                print('Files uploaded onto s3')
            else:
                print('Not uploaded. No new files.')

Run('/Users/shanehower/PycharmProjects','my-first-backup-bucket0328',10).start()
