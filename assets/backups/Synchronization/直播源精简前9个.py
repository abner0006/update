def keep_top_n_sources(top_n=9):
    input_file = "/storage/emulated/0/下载/Document/xiaoran.txt"
    output_file = "/storage/emulated/0/下载/Document/xiaoran_精简.txt"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        if not lines:
            print("文件为空或不存在！")
            return
        
        result = []  # 最终结果列表
        current_group = []  # 临时存储当前标题下的内容（标题行+直播源）
        title_lines = []  # 记录所有标题行（用于判断）
        
        # 先收集所有标题行（含#genre#的行）
        for line in lines:
            if '#genre#' in line:
                title_lines.append(line)
        
        # 按标题行分组处理
        for line in lines:
            if line in title_lines:
                # 遇到新标题行：先处理上一组（如果有），再开始新组
                if current_group:
                    # 处理上一组：保留标题行，直播源按频道取前N条
                    processed_group = process_single_group(current_group, top_n)
                    result.extend(processed_group)
                # 新组开始，加入当前标题行
                current_group = [line]
            else:
                # 非标题行，加入当前组
                current_group.append(line)
        
        # 处理最后一组（文件末尾可能没有新标题行）
        if current_group:
            processed_group = process_single_group(current_group, top_n)
            result.extend(processed_group)
        
        # 写入结果
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result) + '\n')
        
        print(f"处理完成！\n原始文件：{input_file}\n精简后文件：{output_file}\n每个频道保留前{top_n}条直播源")
    
    except Exception as e:
        print(f"处理失败：{str(e)}")

def process_single_group(group_lines, top_n):
    """处理单个标题组：保留标题行，直播源按频道取前N条"""
    if not group_lines:
        return []
    # 标题行是组内第一条（含#genre#）
    title_line = group_lines[0]
    # 直播源是组内其他行
    sources = group_lines[1:]
    
    # 按频道分组，保留每个频道的前N条
    channel_sources = {}
    for line in sources:
        if ',' in line:
            channel, url = line.split(',', 1)
            channel = channel.strip()
            if channel not in channel_sources:
                channel_sources[channel] = []
            channel_sources[channel].append(f"{channel},{url}")
    
    # 组装当前组的结果：标题行 + 处理后的直播源
    processed = [title_line]
    for channel in channel_sources:
        processed.extend(channel_sources[channel][:top_n])  # 取前N条
    
    return processed

# 执行：每个频道保留前9条（可修改top_n=10保留前10条）
keep_top_n_sources(top_n=9)
