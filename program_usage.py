from automated_upload_to_s3.py import S3Synchronizer

while True:
    s3 = S3Synchronizer('/Users/shanehower/PycharmProjects','my-first-backup-bucket0328',10)
    bucket = s3.get_files_bucket()
    folders = s3.get_folder_in_directory()
    files = s3.get_files_in_directory(folders,bucket)
    s3.start_upload(files)
