import argparse
import re
import os
import glob
# 克隆 https://gitlab.chise.org/CHISE/ids.git
# 执行  python ids2radical.py -i "IDS-UCS-Ext-*.txt" -o ext.yaml
# 执行  python ids2radical.py -i "IDS-UCS-Basic.txt" -o basic.yaml
def process_files(input_arg, output_path):
    # 匹配表意文字描述字符 (IDC)，范围为 U+2FF0-U+2FFB
    idc_re = re.compile(r'[\u2FF0-\u2FFB]')
    
    # 1. 解析输入参数：支持逗号分隔，并展开通配符
    input_parts = [p.strip() for p in input_arg.split(',') if p.strip()]
    all_files = []
    for part in input_parts:
        # glob.glob 支持 * 和 ? 等通配符，recursive=True 支持 ** 递归路径
        matched = glob.glob(part, recursive=True)
        all_files.extend(matched)
    
    # 去重并排序，确保处理顺序可预测
    all_files = sorted(list(set(all_files)))

    if not all_files:
        print(f"错误：未找到匹配 '{input_arg}' 的文件")
        return

    try:
        with open(output_path, 'w', encoding='utf-8') as f_out:
            for file_path in all_files:
                if not os.path.isfile(file_path):
                    continue
                
                print(f"正在处理: {file_path}")
                
                with open(file_path, 'r', encoding='utf-8') as f_in:
                    for line in f_in:
                        line = line.strip()
                        
                        # 忽略空行和以分号开头的行
                        if not line or line.startswith(';'):
                            continue
                        
                        parts = line.split('\t')
                        if len(parts) < 3:
                            continue
                        
                        char = parts[1]
                        description = parts[2]
                        
                        # 忽略 @apparent= 后面的内容
                        description = description.split('@apparent=')[0]
                        
                        # 忽略含有 &; 特殊编码的行
                        if '&' in description and ';' in description:
                            continue
                        
                        # 删除所有结构符号 (IDC)
                        clean_description = idc_re.sub('', description).strip()
                        
                        # 提取部件列表
                        components = [c for c in clean_description if not c.isspace()]
                        
                        # 只有一个部件或没有部件的行忽略
                        if len(components) <= 1:
                            continue
                        
                        # 写入结果：汉字 + Tab + 部件（空格分隔）
                        f_out.write(f"{char}\t{' '.join(components)}\n")
                        
        print(f"---")
        print(f"处理完成！")
        print(f"总计处理文件数: {len(all_files)}")
        print(f"结果已保存至: {output_path}")

    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="支持通配符的汉字部件拆解数据清洗工具")
    parser.add_argument("-i", "--input", required=True, 
                        help="输入路径，支持通配符 (*) 和逗号分隔。例如: 'data/*.txt,ids.txt'")
    parser.add_argument("-o", "--output", default="radical.yaml", 
                        help="输出文件路径 (默认: radical.yaml)")
    
    args = parser.parse_args()
    
    process_files(args.input, args.output)