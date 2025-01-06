# Multi-Threaded dahua-ICC Vulnerability Checker

这个工具用于从 CSV 文件中读取链接，并发送 POST 请求检查是否存在GetClassValue.jsp的漏洞，使用id命令判断返回值是否存在（`uid=0(root)`）。通过多线程并发处理请求，提高了处理大量链接时的效率。工具使用 `pandas` 读取 CSV 文件，`requests` 库发送 HTTP 请求，并使用 `ThreadPoolExecutor` 实现多线程。可以直接处理fofa导出的CSV文件。 结果会导出到CSV。
脚本用于快速检测公网ICC是否还存在漏洞，需要尽快修复！！！

## 功能

- 从输入的 CSV 文件中读取链接（`link` 列）。
- 对每个链接发送 POST 请求，检查返回内容中是否包含 `uid=0(root)`。
- 如果发现漏洞（`uid=0(root)`），会打印相关信息。
- 将检查结果（包括链接、城市信息、检查结果）保存到新的 CSV 文件中。

## 运行环境

- Python 3.x
- `pandas` 库
- `requests` 库
- `urllib3` 库

## 安装依赖

首先，确保已安装以下 Python 库：

```bash
pip install pandas requests
```

## 配置

1. **输入 CSV 文件**：确保输入的 CSV 文件中包含以下两列：
   - `link`：要检查的链接。
   - `city`：对应的城市信息。

2. **输出 CSV 文件**：工具会生成一个新的 CSV 文件，保存每个链接的检查结果，列包括：
   - `link`：原始链接。
   - `city`：原始城市信息。
   - `result`：检查结果（是否发现漏洞）。

## 使用方法

1. 将你的链接 CSV 文件命名为 `list.csv`，并确保其格式如下：

```csv
link,city
https://61.174.210.74:4443,CityA
https://113.214.15.134:4443,CityB
```

2. 将此工具的脚本保存为 `icc-check.py`，并确保它与你的 `list.csv` 文件位于同一目录下。

3. 在命令行中运行脚本：

```bash
python icc-check.py
```

4. 运行结束后，结果将保存在 `check_results.csv` 文件中，格式如下：

```csv
link,city,result
https://61.174.210.74:4443,CityA,Find vulnerability
https://113.214.15.134:4443,CityB,Not vulnerability
```

## 代码结构

- **process_csv(file_path)**：读取输入的 CSV 文件并返回 DataFrame。
- **check_single_link(row, headers, payload)**：检查单个链接是否包含漏洞。
- **check_uid(dataframe)**：使用多线程对每个链接进行检查。
- **save_results_to_csv(results, output_file)**：将检查结果保存到输出 CSV 文件。

## 线程配置

该工具使用 `ThreadPoolExecutor` 实现多线程，默认使用 8 个线程并发执行 POST 请求。你可以根据需要调整线程数，方法是在 `ThreadPoolExecutor(max_workers=8)` 中修改 `max_workers` 参数。

## 注意事项

- 如果目标服务器启用了 HTTPS 并使用自签名证书，可能会出现证书验证警告。此脚本已禁用 SSL 证书验证，避免该警告。
- 确保目标链接响应时间不超过 3 秒（超时设置），否则请求将会被视为超时。

## 贡献

欢迎提交 issues 和 pull requests。如果你有改进意见或发现 bug，请随时提出来。

## License

MIT License

---

这个 README 文件提供了关于工具的功能、安装和使用的详细说明，确保其他用户能够快速了解并使用该工具。
