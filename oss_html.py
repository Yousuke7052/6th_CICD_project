import os
import subprocess

# OSS相关环境变量
OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID')
OSS_SECRET_ACCESS_KEY = os.getenv('OSS_SECRET_ACCESS_KEY')
OSS_ENDPOINT = os.getenv('OSS_ENDPOINT')
OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME')

# GitHub仓库信息
GITHUB_REPO_URL = os.getenv('GITHUB_REPO_URL')
LOCAL_REPO_PATH = os.getenv('LOCAL_REPO_PATH', '/tmp/github-repo')

def clone_or_pull_repo(repo_url, local_path):
    if not os.path.exists(local_path):
        # 如果本地路径不存在，则克隆仓库
        subprocess.run(['git', 'clone', repo_url, local_path], check=True)
    else:
        # 如果本地路径存在，则拉取最新更改
        os.chdir(local_path)
        subprocess.run(['git', 'pull'], check=True)

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

def upload_directory_to_oss(local_path, prefix=''):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            oss_path = os.path.join(prefix, os.path.relpath(local_file_path, local_path)).replace("\\", "/")
            upload_file_to_oss(local_file_path, oss_path)

if __name__ == '__main__':
    # 检查必要的环境变量是否设置
    if not all([OSS_ACCESS_KEY_ID, OSS_SECRET_ACCESS_KEY, OSS_ENDPOINT, OSS_BUCKET_NAME, GITHUB_REPO_URL]):
        print("Missing required environment variables.")
        exit(1)

    # 克隆或拉取GitHub仓库
    clone_or_pull_repo(GITHUB_REPO_URL, LOCAL_REPO_PATH)

    # 上传目录到OSS
    upload_directory_to_oss(LOCAL_REPO_PATH)