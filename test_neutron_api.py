import subprocess
import time
from concurrent.futures import ThreadPoolExecutor


# 获取 token 的函数
def get_token():
    try:
        result = subprocess.run(
            ['openstack', 'token', 'issue'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )
        print("Token Issue Command Output:", result.stdout)
        if result.returncode != 0:
            print("Error issuing token:", result.stderr)
            return None

        # 解析 token
        token = None
        for line in result.stdout.splitlines():
            if line.strip().startswith('| id '):
                token = line.split()[-2].strip()
                break
        return token
    except Exception as e:
        print(f"Failed to get token: {e}")
        return None


# 使用 token 调用 Neutron CLI 命令
def get_subnet_list():
    try:
        result = subprocess.run(
            ['neutron', 'subnet-list'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )
        print("Subnet List Command Output:", result.stdout)

        if result.returncode == 0:
            print("Subnet List:\n", result.stdout)
        else:
            print(f"Failed to get subnet list: {result.stderr}")
    except Exception as e:
        print(f"Failed to run neutron subnet-list: {e}")

def request_neutron_api(token):
    try:
        url = "http://127.0.0.1:9696/v2.0/networks"
        headers = {
            "Accept": "application/json",
            "X-Auth-Token": token
        }

        # 构建 curl 命令
        curl_command = [
            "curl", "-g", "-i", "-X", "GET", url,
            "-H", f"Accept: {headers['Accept']}",
            "-H", f"X-Auth-Token: {headers['X-Auth-Token']}"
        ]

        # 执行命令
        result = subprocess.run(
            curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )

        print("Neutron API Response:", result.stdout)

        if result.returncode != 0:
            print("Failed to request Neutron API.")
            return None

        return result.stdout

    except Exception as e:
        print(f"Error while requesting Neutron API: {e}")
        return None


# 线程任务：执行 token 获取和 Neutron 请求
def task():
    token = get_token()
    if token:
        print(f"Successfully got token: {token}")
        request_neutron_api(token)
    else:
        print("Failed to get token. Skipping Neutron API call.")


# 主函数：启动多线程任务
def main():
    num_threads = 100  # 并发线程数

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(task)

        # Wait for all tasks to complete using shutdown
        executor.shutdown(wait=True)



if __name__ == "__main__":
    # 加载 OpenStack 环境变量
    env_file = "~/admin-openrc"
    source_cmd = f"source {env_file} && env"

    try:
        env_vars = subprocess.run(
            source_cmd, shell=True, executable="/bin/bash",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )
        if env_vars.returncode == 0:
            print("Environment Loaded Successfully.")
        else:
            print("Failed to load environment variables:", env_vars.stderr)
            exit(1)
    except Exception as e:
        print(f"Error loading environment variables: {e}")
        exit(1)

    main()
