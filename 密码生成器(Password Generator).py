import secrets
import string
import os
from datetime import datetime

def generate_secure_password(length, special_ratio):
    """生成符合安全规范的密码[1,5](@ref)"""
    # 增强输入验证
    if not isinstance(length, int) or length < 1:
        raise ValueError("密码长度必须≥1")
    if not 0 <= special_ratio <= 100:
        raise ValueError("特殊符号占比需在0-100之间")

    # 动态字符集配置
    special_chars = string.punctuation
    normal_chars = string.ascii_letters + string.digits
    
    # 计算字符分布
    special_count = int(length * special_ratio / 100)
    normal_count = length - special_count
    
    # 处理边界情况[4](@ref)
    if special_ratio == 0:
        return ''.join(secrets.choice(normal_chars) for _ in range(length))
    if special_ratio == 100:
        return ''.join(secrets.choice(special_chars) for _ in range(length))

    # 生成密码组件
    password = []
    password.extend(secrets.choice(special_chars) for _ in range(special_count))
    password.extend(secrets.choice(normal_chars) for _ in range(normal_count))
    
    # 加密级随机打乱[1](@ref)
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

def save_password(password, save_dir):
    """安全保存密码到文件[3](@ref)"""
    timestamp = datetime.now().strftime("%m月%d日%H时%M分%S秒")
    filename = f"{timestamp}.txt"
    filepath = os.path.join(save_dir, filename)
    
    os.makedirs(save_dir, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"生成时间：{timestamp}\n密码：{password}")
    return filepath

def main_loop():
    """交互式主循环[6](@ref)"""
    while True:
        try:
            # 参数输入
            length = int(input("\n请输入密码长度（1-1024）: "))
            ratio = int(input("请输入特殊符号占比（0-100）: "))
            
            # 生成密码
            password = generate_secure_password(length, ratio)
            print(f"\n生成的密码：{password}")
            
            # 保存功能
            if input("\n是否保存密码？（Y/N）: ").lower() == 'y':
                save_dir = input("保存目录路径（默认当前目录）: ").strip() or "."
                saved_path = save_password(password, save_dir)
                print(f"已保存至：{saved_path}")
            
            # 循环控制
            if input("\n继续生成新密码？（Y/N）: ").lower() != 'y':
                print("\n感谢使用，再见！")
                break
                
        except ValueError as e:
            print(f"输入错误：{e}")
        except Exception as e:
            print(f"系统错误：{e}")
            break

if __name__ == "__main__":
    print("===== 密码生成器-cn v1.0 =====")
    main_loop()