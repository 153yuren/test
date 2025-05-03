import os
import random
from pathlib import Path

def detect_delimiter(content):
    """检测文件分隔符（兼容逗号和换行混合格式）"""
    if ',' in content:
        return ','
    return '\n'

def parse_numbers(content):
    """通用解析方法，处理混合分隔符"""
    return [num.strip() for num in content.replace('\n', ',').split(',') if num.strip()]

def has_arithmetic_sequence(arr, length=4):
    """优化后的等差序列检测算法"""
    for i in range(len(arr) - length + 1):
        a, b, c, d = arr[i:i+length]
        if (b - a == c - b == d - c):
            return True
    return False

def process_large_file(input_path, max_attempts=100):
    # 读取文件并解析数字
    with open(input_path, 'r') as f:
        content = f.read().strip()
    
    delimiter = detect_delimiter(content)
    numbers = list(map(int, parse_numbers(content)))
    
    # 内存优化策略：分块处理百万级数据
    chunk_size = 100000
    chunks = [numbers[i:i+chunk_size] for i in range(0, len(numbers), chunk_size)]
    
    # 多轮打乱验证逻辑
    for _ in range(max_attempts):
        # 分块打乱后合并
        for chunk in chunks:
            random.shuffle(chunk)
        shuffled = [num for chunk in chunks for num in chunk]
        
        # 滑动窗口检测等差序列
        if not has_arithmetic_sequence(shuffled):
            break
    else:
        raise ValueError("无法生成符合条件的序列")

    # 构建输出路径
    input_file = Path(input_path)
    output_path = input_file.with_name(f"{input_file.stem}.change{input_file.suffix}")
    
    # 流式写入优化（网页6][网页8]）
    with open(output_path, 'w') as f:
        if delimiter == ',':
            f.write(','.join(map(str, shuffled)))
        else:
            f.write('\n'.join(map(str, shuffled)))
    
    return output_path

if __name__ == "__main__":
    input_file = input("请输入文件路径：").strip()
    try:
        result_path = process_large_file(input_file)
        print(f"处理完成，结果已保存至：{result_path}")
    except Exception as e:
        print(f"处理失败：{str(e)}")