import os
import subprocess

# OSS相关环境变量
OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID')
OSS_SECRET_ACCESS_KEY = os.getenv('OSS_SECRET_ACCESS_KEY')
OSS_ENDPOINT = os.getenv('OSS_ENDPOINT')
OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME')

def upload_file_to_oss(file_path, destination_path):
    try:
        # 使用旧版字符串格式化方法
        oss_url = 'oss://%s/%s' % (OSS_BUCKET_NAME, destination_path)
        
        subprocess.run([
            'ossutil', 'cp', file_path,
            oss_url,
            '--access-key-id', OSS_ACCESS_KEY_ID,
            '--access-key-secret', OSS_SECRET_ACCESS_KEY,
            '--endpoint', OSS_ENDPOINT
        ], check=True)
        print("File %s uploaded to OSS successfully." % file_path)
    except subprocess.CalledProcessError as e:
        print("Failed to upload file %s: %s" % (file_path, e))

if __name__ == '__main__':
    # 假设你要上传的是名为hello.txt的文件
    file_path = 'index.html'  # 相对路径
    destination_path = 'index.html'  # OSS中的目标路径
    
    # 检查文件是否存在
    if os.path.exists(file_path):
        upload_file_to_oss(file_path, destination_path)
    else:
        print("File %s does not exist." % file_path)
