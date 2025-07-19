import os

def process_file(filename, keep_lines):
    """
    处理单个文件：按 #genre# 分组去重
    - filename: 要处理的文件名
    - keep_lines: 每组保留的重复频道行数
    """
    # 1. 读取文件内容
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 2. 按 "#genre#" 分组
    groups = []
    current_group = []
    for line in lines:
        if ",#genre#" in line:
            if current_group:
                groups.append(current_group)
            current_group = [line]
        else:
            current_group.append(line)
    # 补充最后一组
    if current_group:
        groups.append(current_group)

    # 3. 组内去重（保留前 N 个重复频道）
    output_lines = []
    for group in groups:
        seen = {}  # 记录频道名出现次数
        for line in group:
            #  genre 行直接保留
            if ",#genre#" in line:
                output_lines.append(line)
                continue
            
            # 拆分频道名和内容
            parts = line.strip().split(",", 1)
            if len(parts) < 2:
                output_lines.append(line)
                continue
            
            name = parts[0].strip()
            count = seen.get(name, 0)
            
            # 保留前 N 个重复项
            if count < keep_lines:
                output_lines.append(line)
                seen[name] = count + 1

    # 4. 写入输出文件
    output_dir = "output"
    with open(os.path.join(output_dir, filename), "w", encoding="utf-8") as f:
        f.writelines(output_lines)


def main():
    """
    主逻辑：遍历目录下所有 .txt 文件并处理
    """
    # 从环境变量获取参数（Workflow 里配置的）
    keep_lines = int(os.environ.get("KEEP_LINES", "1"))  
    input_dir = "."  # 当前目录（与 actions/checkout 拉取的代码目录一致）
    
    # 确保输出目录存在
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # 遍历处理所有 .txt 文件
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            process_file(filename, keep_lines)


if __name__ == "__main__":
    main()
