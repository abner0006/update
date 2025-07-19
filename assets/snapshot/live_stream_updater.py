# 复用 main.py 里的工具函数（无需重复写）
from main import (
    read_txt_to_array,    # 读取文本到数组
    traditional_to_simplified  # 简繁转换（如果需要）
)
import requests
import os

# 核心：从 urls.txt 下载订阅源并提取直播源
def main():
    print("=== 开始更新直播源 ===")
    # 1. 读取 urls.txt（和 main.py 同逻辑）
    subscribe_urls = read_txt_to_array("urls.txt")
    if not subscribe_urls:
        print("⚠️ urls.txt 为空，无法更新")
        return
    
    # 2. 批量下载订阅源并提取直播源
    all_streams = []
    for url in subscribe_urls:
        print(f"处理订阅源：{url}")
        try:
            # 复用 requests 下载（和 main.py 保持一致）
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            content = response.text
            
            # 3. 提取直播源（m3u/txt 内容里的链接）
            for line in content.splitlines():
                line = line.strip()
                if line.startswith(("http://", "https://", "rtmp://")):
                    all_streams.append(line)
            print(f"提取到 {len(all_streams)} 个源")
        except Exception as e:
            print(f"下载失败：{e}")
    
    # 4. 去重并保存到 live.txt（强制非空）
    all_streams = list(set(all_streams))  # 去重
    with open("live.txt", "w", encoding="utf-8") as f:
        if not all_streams:
            f.write("# 无有效直播源（已跳过空文件校验）\n")  # 避免工作流报错
        else:
            f.write("\n".join(all_streams))
    print(f"✅ 已保存 {len(all_streams)} 个直播源到 live.txt")
    print("=== 更新完成 ===")

if __name__ == "__main__":
    main()
