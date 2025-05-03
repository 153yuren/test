import os

def optimized_bubble_sort(arr):
    """优化版冒泡排序(使用while循环)"""
    n = len(arr)
    swapped = True
    while n > 1 and swapped:
        swapped = False
        i = 0
        while i < n - 1:
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
            i += 1
        n -= 1
    return arr

def process_input_data(data_str, is_file=False):
    """处理输入数据为纯数字列表"""
    if is_file:
        # 处理文件分隔符（换行符或逗号）
        data = data_str.replace('\n', ',').split(',')
    else:
        # 处理手动输入（逗号分隔）
        data = data_str.split(',')
    return [int(x.strip()) for x in data if x.strip().isdigit()]

def save_output(sorted_list, input_path=None, output_dir=None):
    """保存排序结果到文件"""
    if input_path:
        # 自动生成输出路径
        dir_name = os.path.dirname(input_path)
        base_name = os.path.basename(input_path)
        name, ext = os.path.splitext(base_name)
        output_path = os.path.join(dir_name, f"{name}.change{ext}")
    else:
        # 手动输入需要指定目录
        output_path = os.path.join(output_dir, "sorted_result.txt")
    
    # 保存文件内容（每行一个数字）
    with open(output_path, 'w') as f:
        f.write('\n'.join(map(str, sorted_list)))
    print(f"结果已保存至：{output_path}")

def main():
    choice = input("选择输入方式 (file/text): ").lower()
    
    if choice == 'file':
        file_path = input("请输入文件路径：")
        with open(file_path, 'r') as f:
            data = process_input_data(f.read(), is_file=True)
    elif choice == 'text':
        input_str = input("请输入数字（逗号分隔）：")
        data = process_input_data(input_str)
    else:
        print("无效的输入方式")
        return

    sorted_data = optimized_bubble_sort(data)
    
    # 终端显示格式（逗号分隔）
    print("排序结果：", ','.join(map(str, sorted_data)))

    # 保存文件处理
    save_choice = input("是否保存结果？(Y/y/直接回车确认，其他取消): ").strip().lower()
    if save_choice in ('y', ''):
        if choice == 'file':
            save_output(sorted_data, input_path=file_path)
        else:
            output_dir = input("请输入输出目录：")
            save_output(sorted_data, output_dir=output_dir)

if __name__ == "__main__":
    main()