import os
import subprocess

# OSS相关信息
OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID')
OSS_SECRET_ACCESS_KEY = os.getenv('OSS_SECRET_ACCESS_KEY')
OSS_ENDPOINT = os.getenv('OSS_ENDPOINT')
OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME')

# 目录信息
LOCAL_DIR_PATH = 'project_2'
DESTINATION_PATH = 'project_2'

# 上传目录到OSS
try:
    oss_url = 'oss://%s/%s' % (OSS_BUCKET_NAME, DESTINATION_PATH)
    subprocess.run([
        'ossutil', 'cp', LOCAL_DIR_PATH,
        oss_url,
        '-r',  # 递归选项
        '--access-key-id', OSS_ACCESS_KEY_ID,
        '--access-key-secret', OSS_SECRET_ACCESS_KEY,
        '--endpoint', OSS_ENDPOINT
    ], check=True)
    print("Directory %s uploaded to OSS successfully." % LOCAL_DIR_PATH)
except subprocess.CalledProcessError as e:
    print("Failed to upload directory %s: %s" % (LOCAL_DIR_PATH, e))