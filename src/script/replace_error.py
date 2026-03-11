import argparse
import os

file_path = 'dict/radical.yaml'

def main():
    # 设置命令行参数
    parser = argparse.ArgumentParser(description='替换 radical.yaml 中的组成部分')
    parser.add_argument('-f', required=True, help='要被替换的文字')
    parser.add_argument('-t', nargs='+', required=True, help='替换后的文字（支持多个空格隔开的字符）')
    # 添加 -a 参数，默认为 False，如果命令行中出现则为 True
    parser.add_argument('-a', action='store_true', help='保留原行，并在其后插入替换后的新行')
    
    args = parser.parse_args()
    
    target = args.f
    replacement = " ".join(args.t)
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return

    updated_lines = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' not in line:
                updated_lines.append(line)
                continue
            
            # 分割行内容
            char_part, components_part = line.split('\t', 1)
            components = components_part.strip().split(' ')
            
            # 检查当前行是否包含目标字符
            if target in components:
                # 执行替换逻辑
                new_components = [replacement if item == target else item for item in components]
                new_line = f"{char_part}\t{' '.join(new_components)}\n"
                
                if args.a:
                    # 如果有 -a 参数：先添加原始行，再添加新行
                    updated_lines.append(line)
                    updated_lines.append(new_line)
                else:
                    # 默认逻辑：只添加替换后的行
                    updated_lines.append(new_line)
            else:
                # 如果没有匹配到目标，直接保留原行
                updated_lines.append(line)

    # 将结果写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

if __name__ == "__main__":
    main()