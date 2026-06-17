"""
os,sys: deal with files
datetime: set dict header
import converting methods
"""
import os
import sys
from datetime import datetime
from flypy import tofly
from mspy import toms

src_dict_file = 'dict/temp.dict.yaml'
src_dict_head_file = 'dict/dict-head-note.yaml'
src_dict_append_file = 'dict/append-dict.yaml'

with open(src_dict_head_file, 'r', encoding='utf-8') as f:
    extra_content = f.read()

def process_encoding(
    codes,
    method,
    separator):
    """convert given codes to pinyin or double pinyin"""
    if method == 'flypy':
        return tofly("".join(codes))
    elif method == 'mspy':
        return toms("".join(codes))
    elif method == 'py':
        return "".join(codes.replace(separator,''))

def gen_dict(
    input_file_path=src_dict_file,
    output_file_path=None,
    encoding_method='flypy',
    separator="'"):

    """generate dict file"""

    if output_file_path is None:
        ext = '.dict.yaml'
        output_file_path = f"radical_{encoding_method}{ext}"

    base_name = os.path.splitext(os.path.basename(output_file_path))[0].replace(".dict", "")

    file_header = f'''---
name: {base_name}
version: "{datetime.now().strftime("%Y.%m.%d")}"
sort: original
...\n\n'''

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(extra_content + '\n\n' + file_header)
        with open(input_file_path, 'r', encoding='utf-8') as input_file:
            for line in input_file:
                line = line.strip()
                # ignore empty lines and comented lines
                if len(line) == 0 or line.startswith('#'):
                    output_file.write(line)
                    output_file.write('\n')
                    continue

                parts = line.split('\t')
                if len(parts) in (2, 3):

                    chinese_char = parts[0]
                    codes = [code.strip() for code in parts[1].split(separator)]
                    weight = parts[2].strip() if len(parts) == 3 else None

                    # converting
                    converted_codes = [process_encoding(code,encoding_method,
                                                        separator) for code in codes]

                    # combining
                    output_line = f"{chinese_char}\t{''.join(converted_codes)}"
                    if weight is not None:
                        output_line += f"\t{weight}"
                    output_line += "\n"

                    # appending
                    output_file.write(output_line)
                else:
                    print('\033[91m' + line + '\033[0m')
                    raise ValueError("error!")

    print(input_file_path + " -> " + output_file_path)

if __name__ == "__main__":
    params = {}
    for arg in sys.argv[1:]:
        key, value = arg.split('=')
        params[key] = value
    gen_dict(**params)
