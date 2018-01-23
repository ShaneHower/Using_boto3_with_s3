import boto3
import os, time

path_to_watch_pycharm =  '/Users/shanehower/PycharmProjects'
files = os.listdir(path_to_watch_pycharm)
# first get a list of all files in s3
# this will be used to compare files in the desired directory
# and files already uploaded in the bucket
s3_resource = boto3.resource('s3')
my_bucket = s3_resource.Bucket('my-first-backup-bucket0328')
files_in_bucket = []

# boto3.client() used for uploading and downloading
s3_client = boto3.client('s3')

# append the keys of the files in the bucket to a list
for object in my_bucket.objects.filter(Prefix = path_to_watch_pycharm):
    path, file_name = os.path.split(object.key)
    files_in_bucket.append('{0}/{1}'.format(path, file_name))

def get_folders_in_directory(path):
    # now unpack the folders in the desired directory into a list
    files_in_dir = []
    for i in files:
        if i != '.DS_Store' and i != 'Anaconda':
            path_to_watch_folders_in_pycharm = '/Users/shanehower/PycharmProjects/{0}'.format(i)
            files_in_dir.append(path_to_watch_folders_in_pycharm)
    return files_in_dir

def find_len_of_desired_path(path):
    length = 0

    for i in path:
        # this is the last path to search. returns the list of files in each folder.
        new_dir = os.listdir(i)
        length = len(new_dir) + length
    return length


def find_directory_of_desired_path(path):
    list_of_files_in_final_path = []
    # compare the two lists, files_in_bucket and new_dir (which is created below).
    # if there is a file that is not present in the bucket but is
    # present in the directory, upload that file to the bucket.
    for i in path:
        # this is the last path to search. returns the list of files in each folder.
        new_dir = os.listdir(i)
        # Finally compare each value in the list new_dir with files_in_bucket.
        for j in new_dir:
            if (j not in files_in_bucket) and (j != '.DS_Store' and j != '.idea'):
                # must compare the full path so path_to_load is the path to the file we want to upload
                path_to_upload = '{0}/{1}'.format(i, j)
                list_of_files_in_final_path.append(path_to_upload)
    return list_of_files_in_final_path

folders = get_folders_in_directory(files)
desired_files = find_directory_of_desired_path(folders)
old_length = find_len_of_desired_path(folders)

while True:
    #run every 12 hours
    time.sleep(43200)
    new_length = find_len_of_desired_path(folders)

    # have to refine these variables because the length changed and the new file
    # needs to be included
    folders = get_folders_in_directory(files)
    desired_files = find_directory_of_desired_path(folders)
    if new_length > old_length:
        for i in desired_files:
            s3_client.upload_file(i, 'my-first-backup-bucket0328', i)
            old_length = new_length
