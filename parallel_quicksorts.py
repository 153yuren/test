import os
import sys
import mmap
import argparse
from multiprocessing import Pool, cpu_count
from functools import partial

# 全局进程池对象
_global_pool = None

def output_result(sorted_numbers, output_flag):
    """输出控制函数"""
    if output_flag == 1:
        print(','.join(map(str, sorted_numbers)))

def chunk_reader(file_path, chunk_size=1024*1024):
    """改进的分块读取（避免行截断）"""
    with open(file_path, "rb") as f:
        mmap_obj = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        remaining = b''
        while True:
            chunk = mmap_obj.read(chunk_size)
            if not chunk:
                break
            # 查找最后一个换行符
            last_newline = chunk.rfind(b'\n')
            if last_newline != -1:
                yield remaining + chunk[:last_newline+1]
                remaining = chunk[last_newline+1:]
            else:
                remaining += chunk
        if remaining:
            yield remaining

def parallel_quicksort(arr, is_top=True, depth=0):
    """优化的并行快速排序"""
    if len(arr) <= dynamic_threshold(arr) or depth > 3:
        return sorted(arr)
    
    # 改进的三数取中法
    mid = len(arr)//2
    candidates = sorted([arr[0], arr[mid], arr[-1], arr[len(arr)//4], arr[-len(arr)//4]])
    pivot = candidates[2]

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    global _global_pool
    if is_top:
        if _global_pool is None:
            _global_pool = Pool(processes=min(4, cpu_count()*2))
            
        task_args = [(left, False, depth+1), (right, False, depth+1)]
        left_sorted, right_sorted = _global_pool.starmap(parallel_quicksort, task_args)
    else:
        left_sorted = parallel_quicksort(left, False, depth+1)
        right_sorted = parallel_quicksort(right, False, depth+1)
    
    return left_sorted + middle + right_sorted

def dynamic_threshold(arr):
    """优化的动态阈值"""
    cpu_num = max(1, os.cpu_count()//2)
    return max(5000, len(arr) // cpu_num)

def process_file(input_path, output_flag):
    """增强的文件处理逻辑"""
    original_count = 0
    numbers = []
    
    try:
        # 第一遍扫描验证数据完整性
        with open(input_path, "rb") as f:
            for line in f:
                original_count += 1
                line = line.strip()
                if not line:
                    continue
                if not line.isdigit():
                    raise ValueError(f"非数字内容: {line.decode()}")

        # 第二遍实际读取
        for chunk in chunk_reader(input_path):
            lines = chunk.split(b'\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                numbers.append(int(line))
                
        if len(numbers) != original_count:
            raise RuntimeError(f"数据计数不一致: 原始{original_count} 实际{len(numbers)}")
            
    except ValueError as e:
        print(f"错误：检测到非数字内容 - {str(e)}")
        sys.exit(2)
    except FileNotFoundError:
        print(f"错误：文件 {input_path} 未找到")
        sys.exit(3)
    
    sorted_numbers = parallel_quicksort(numbers)
    
    # 结果校验
    if len(sorted_numbers) != original_count:
        print(f"错误：数据丢失/重复 原始:{original_count} 结果:{len(sorted_numbers)}")
        sys.exit(8)
    
    # 路径处理
    dir_name, base_name = os.path.split(input_path)
    base, ext = os.path.splitext(base_name)
    output_path = os.path.join(dir_name, f"{base}.change{ext}")
    
    # 改进的写入逻辑
    try:
        with open(output_path, 'w+b') as f:
            content = '\n'.join(map(str, sorted_numbers)).encode()
            f.write(content)
            
        # 二次验证写入结果
        result_count = sum(1 for _ in open(output_path))
        if result_count != original_count:
            raise RuntimeError(f"写入验证失败: 预期{original_count} 实际{result_count}")
            
    except PermissionError:
        print(f"错误：无权限写入文件 {output_path}")
        sys.exit(6)
    
    output_result(sorted_numbers, output_flag)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="并行快速排序工具")
    parser.add_argument("dir", help="输入文件所在目录")
    parser.add_argument("file", help="输入文件名")
    parser.add_argument("output_flag", type=int, choices=[0,1], 
                      help="输出模式 (0=静默模式, 1=打印结果)")
    args = parser.parse_args()

    try:
        input_path = os.path.join(args.dir, args.file)
        
        if not os.path.isfile(input_path):
            raise FileNotFoundError
        
        process_file(input_path, args.output_flag)
        
        if _global_pool is not None:
            _global_pool.close()
            _global_pool.join()
            
    except FileNotFoundError:
        print(f"错误：输入文件 {input_path} 不存在")
        sys.exit(5)