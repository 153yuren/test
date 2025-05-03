import random
import os
from datetime import datetime

def generate_numbers(lower, upper, count, data_type):
    """生成指定范围的随机数集合"""
    numbers = []
    for _ in range(count):
        if data_type == '整数':
            num = random.randint(lower, upper)
        else:
            num = random.uniform(lower, upper)
        numbers.append(str(num))
    return numbers

def save_to_file(numbers, directory):
    """保存到带时间戳的文件"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}.txt"
    filepath = os.path.join(directory, filename)
    
    try:
        with open(filepath, 'w') as f:
            f.write('\n'.join(numbers))
        print(f"\n数据已保存至：{filepath}")
    except Exception as e:
        print(f"保存失败：{str(e)}")

def main_loop():
    """主程序循环"""
    print("="*40)
    print("随机数生成器 v1.0.0".center(40))
    print("="*40)
    
    while True:
        try:
            # 获取用户输入
            lower = float(input("请输入下界："))
            upper = float(input("请输入上界："))
            count = int(input("请输入生成数量："))
            data_type = input("生成整数还是浮点数？(输入'整数'或'浮点数')：")
            save_choice = input("是否保存到文件？(y/n)：").lower()
            
            # 验证输入有效性
            if upper <= lower:
                raise ValueError("上界必须大于下界")
            if count <= 0:
                raise ValueError("生成数量必须大于0")
            if data_type not in ['整数', '浮点数']:
                raise ValueError("请输入有效的类型（整数/浮点数）")

            # 生成随机数
            numbers = generate_numbers(
                int(lower) if data_type == '整数' else lower,
                int(upper) if data_type == '整数' else upper,
                count,
                data_type
            )

            # 输出结果
            if save_choice == 'y':
                directory = input("请输入保存目录：")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                save_to_file(numbers, directory)
            else:
                print("\n生成的随机数：")
                print('\n'.join(numbers))

        except ValueError as e:
            print(f"输入错误：{str(e)}")
        except Exception as e:
            print(f"发生未知错误：{str(e)}")

        # 循环控制
        if input("\n是否继续生成？(y/n)：").lower() != 'y':
            print("感谢使用！")
            break

if __name__ == "__main__":
    main_loop()