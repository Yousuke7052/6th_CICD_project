import os
import subprocess

# 从环境变量中读取OSS相关信息
OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID')
OSS_SECRET_ACCESS_KEY = os.getenv('OSS_SECRET_ACCESS_KEY')
OSS_ENDPOINT = os.getenv('OSS_ENDPOINT')
OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME')

# GitHub仓库信息
GITHUB_REPO_URL = os.getenv('GITHUB_REPO_URL')
LOCAL_REPO_PATH = os.getenv('LOCAL_REPO_PATH', '/tmp/github-repo')

def clone_or_pull_repo(repo_url, local_path):
    if not os.path.exists(local_path):
        subprocess.run(['git', 'clone', repo_url, local_path], check=True)
    else:
        os.chdir(local_path)
        subprocess.run(['git', 'pull'], check=True)

def upload_file_to_oss(file_path, destination_path):
    try:
        oss_url = f'oss://{OSS_BUCKET_NAME}/{destination_path}'
        subprocess.run([
            'ossutil', 'cp', file_path,
            oss_url,
            '--access-key-id', OSS_ACCESS_KEY_ID,
            '--access-key-secret', OSS_SECRET_ACCESS_KEY,
            '--endpoint', OSS_ENDPOINT
        ], check=True)
        print(f"File {file_path} uploaded to OSS successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to upload file {file_path}: {e}")

if __name__ == '__main__':
    if not all([OSS_ACCESS_KEY_ID, OSS_SECRET_ACCESS_KEY, OSS_ENDPOINT, OSS_BUCKET_NAME, GITHUB_REPO_URL]):
        print("Missing required environment variables.")
        exit(1)

    clone_or_pull_repo(GITHUB_REPO_URL, LOCAL_REPO_PATH)

    for root, _, files in os.walk(LOCAL_REPO_PATH):
        for file in files:
            local_file_path = os.path.join(root, file)
            oss_path = os.path.join(os.path.relpath(root, LOCAL_REPO_PATH), file).replace("\\", "/")
            upload_file_to_oss(local_file_path, oss_path)