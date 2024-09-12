import os
import subprocess

# OSS相关信息
OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID')
OSS_SECRET_ACCESS_KEY = os.getenv('OSS_SECRET_ACCESS_KEY')
OSS_ENDPOINT = os.getenv('OSS_ENDPOINT')
OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME')

# 文件信息
LOCAL_FILE_PATH = 'index.html'
DESTINATION_PATH = 'index.html'

# 上传文件到OSS
try:
    oss_url = 'oss://%s/%s' % (OSS_BUCKET_NAME, DESTINATION_PATH)
    subprocess.run([
        'ossutil', 'cp', LOCAL_FILE_PATH,
        oss_url,
        '--access-key-id', OSS_ACCESS_KEY_ID,
        '--access-key-secret', OSS_SECRET_ACCESS_KEY,
        '--endpoint', OSS_ENDPOINT
    ], check=True)
    print("File %s uploaded to OSS successfully." % LOCAL_FILE_PATH)
except subprocess.CalledProcessError as e:
    print("Failed to upload file %s: %s" % (LOCAL_FILE_PATH, e))