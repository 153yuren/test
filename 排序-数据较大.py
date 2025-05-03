import os
import re

output = 1

def process_number_file(file_path):
    # 分解文件路径
    file_dir = os.path.dirname(file_path)
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))
    
    # 读取并提取数字（改进正则表达式）
    numbers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 改进点1：支持匹配负数和浮点数[6,8](@ref)
            line_nums = re.findall(r'-?\d+\.?\d*', line.strip())  # 匹配负数、整数和浮点数
            numbers.extend(map(float, line_nums))  # 改进点2：转换为float类型
    
    # 仅排序不去重
    sorted_numbers = sorted(numbers)
    
    # 终端输出（改进显示格式）
    if output == 1:
        # 改进点3：整数显示为整数，浮点保留小数[6](@ref)
        formatted = [str(int(num)) if num.is_integer() else f"{num:.2f}".rstrip('0').rstrip('.') 
                    for num in sorted_numbers]
        print(','.join(formatted))
    
    # 用户确认保存
    choice = input("是否保存结果？(Y/y/直接回车确认): ").strip().lower()
    if choice in ('y', ''):
        new_filename = f"{file_name}.change{file_ext}"
        save_path = os.path.join(file_dir, new_filename)
        
        # 写入文件（改进格式处理）
        with open(save_path, 'w', encoding='utf-8') as f:
            for num in sorted_numbers:
                # 整数去掉小数部分，浮点保留两位小数[6](@ref)
                if num.is_integer():
                    f.write(f"{int(num)}\n")
                else:
                    f.write(f"{num:.2f}\n")
        print(f"文件已保存至：{save_path}")

if __name__ == "__main__":
    input_path = input("请输入文件路径：").strip()
    process_number_file(input_path)