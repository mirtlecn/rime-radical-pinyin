# 本脚本从此项目衍生 https://github.com/maxchang3/rime-chaizi (MIT)"""
"""
pypinyin -> get pinyin
pypinyin_dict -> load custom pinyin data
"""
import csv
import sys
from datetime import datetime
from itertools import product
import re
import pypinyin
import collections
from pypinyin import pinyin, load_phrases_dict
from pypinyin_dict.pinyin_data import kmandarin_8105

radical = []
yaml = set()
comment = set()
error = set()
pattern = re.compile("^[a-z']+$")
kmandarin_8105.load()

# 词典文件路径
src_dict_file = 'dict/radical.yaml'
src_dict_head_file = 'dict/dict-head-note.yaml'
src_dict_append_file = 'dict/append-dict.yaml'
src_weight_file = 'dict/zh-CN.weight.csv'
# 生成文件路径
des_dict_file = 'dict/temp.dict.yaml'
des_error_file = 'dict/todo.yaml'
des_pinyin_dict_file = '../radical_pinyin.dict.yaml'

custom_dict = {
    '一': [['heng2']], # 横
    '丨': [['shu4']], # 竖
    '丿': [['pie3']], # 撇
    '乁': [['na4']], # 捺
    '㇏': [['na4']], # 捺
    '乀': [['na4']], # 捺
    '乚': [['gou1']], # 钩
    '𠄌': [['gou1']], # 钩
    '亅': [['gou1']], # 钩
    '𠃌': [['zhe2','gou1']], # 折 & 钩
    '㇉': [['zhe2']], # 折
    '𠃊': [['zhe2']], # 折
    # '□': [['zhe2']], # 折
    '𠃍': [['zhe2']], # 折
    '乛': [['zhe2']], # 折
    '𠃋': [['zhe2']], # 折
    '丶': [['dian3','na4']],  # 点 & 捺
    # 一撇一横，牛字去掉十字，施字的右侧上部，视作「人」
    # 巣、尖、尙、尚等字上部，视为「小」
    '卜': [['bo1','bu3']],
    '厶': [['si1']],
    '爿': [['pian4']], # 牁 鼎
    '乂': [['yi4']],
    '亠': [['tou2','yi1']],
    '𫶧': [['chuan1']],
    '龶': [['feng1']],
    '⻀': [['cao3']],
    '𠂊': [['dao1']],
    '𫜹': [['shan1']],
    '廾': [['gong4','nong4']],
    '灬': [['huo3']], # 然
    '⺄': [['yi3']], # 飞去掉点，「乙」的变体
    '疋': [['ding4','pi3']], # 定
    '长': [['zhang3','chang2']],
    '凵': [['kan3','xiong1']],
    '冖': [['mi4','bao3']],
    '攵': [['wen2']],
    '夂': [['wen2']],
    '冂': [['tong2','jiong1']], # 同、周等字的外框
    '𡗗': [['chun1']], # 春、奉
    # 卷、眷等字的上部念 juan3
    '龴': [['si1']],
    '鳥': [['niao3']],
    '倉': [['cang1']],
    '龍': [['long2']],
    '屮': [['cao3']],
    '參': [['can1','shen1']],
    '□': [['ge1']],
    '': [['yi1']], # 「衣」去掉 亠 的下部，以及再去掉丿的变体（「展」的下部）
    '卩': [['er3']],
    '廴': [['jian4','yin3']],
    '宀': [['bao3']],
    '龷': [['gong4']],
    '罒': [['si4','wang3']],
    '癶': [['deng1']],
    '爫': [['zhua3','zhao3']],
    '彳': [['ren2','chi4']],
    '阝': [['er3']],
    '匚': [['fang1','kuang1']],
    '彐': [['shan1']],
    '刂': [['dao1']],
    '丬': [['jiang1','qiang2']],
    '囗': [['kou3','wei2','guo2']], # 国，围等字的外框
    '辶': [['zhi1']],
    '彡': [['shan1','san1']],
    '糸': [['mi4','si1']],
    '蟲': [['chong2']],
    '尃': [['fu1']],
    '頁': [['ye4']],
    '聶': [['nie4']],
    '孱': [['chan2']],
    '𡕩': [['man3']],
    '曰': [['yue1','ri4']],
    '𠙽': [['kuai4']],
    '𦉼': [['la4']],
    '重': [['zhong4','chong2']],
    '將': [['jiang1']],
    '𭕘': [['mei2']],
    '𣥚': [['zou3']],
    '𤽄': [['quan2']],
    '𦣞': [['yi2']]
    }
load_phrases_dict(custom_dict)


HEADER = f'''---
name: radical_pinyin
version: "{datetime.now().strftime("%Y.%m.%d")}"
sort: original
...\n\n'''

def is_not_empty(s):
    "pinyin should not be null or empty"
    return s is not None and s.strip() != ''

def load_weight_map(file_path):
    weights = {}
    with open(file_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or not {'character', 'weight'}.issubset(reader.fieldnames):
            raise ValueError(f"{file_path} must contain character and weight columns")
        for row_number, row in enumerate(reader, start=2):
            character = (row.get('character') or '').strip()
            weight_text = (row.get('weight') or '').strip()
            if not character and not weight_text:
                continue
            if not character or not weight_text:
                raise ValueError(f"{file_path}:{row_number} has incomplete weight data")
            try:
                weights[character] = int(weight_text)
            except ValueError as exc:
                raise ValueError(f"{file_path}:{row_number} has invalid weight: {weight_text}") from exc
    return weights

def get_weight(character, weights):
    return weights.get(character, 1)

def add_weighted_entry(entries, character, code, weights, weight=None):
    entry_weight = get_weight(character, weights) if weight is None else weight
    entries.add((entry_weight, f"{character}\t{code}\t{entry_weight}"))

def add_append_entries(entries, comments, content, weights):
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if len(line) == 0 or line.startswith("#"):
            comments.add(line)
            continue

        parts = line.split("\t")
        if len(parts) == 2:
            add_weighted_entry(entries, parts[0], parts[1], weights)
        elif len(parts) == 3:
            try:
                weight = int(parts[2])
            except ValueError as exc:
                raise ValueError(f"invalid append entry weight: {line}") from exc
            add_weighted_entry(entries, parts[0], parts[1], weights, weight)
        else:
            raise ValueError(f"invalid append entry: {line}")

def parse_params(args):
    params = {}
    for arg in args:
        key, value = arg.split('=', 1)
        params[key] = value
    return params

params = parse_params(sys.argv[1:])
src_weight_file = params.pop('weight_file_path', src_weight_file)
if params:
    raise ValueError(f"unknown arguments: {', '.join(sorted(params))}")

weights = load_weight_map(src_weight_file)

with open(src_dict_file, 'r', encoding='utf-8' ) as f:
    radical = f.readlines()

for line in radical:
    line = line.strip()

    if len(line) == 0 or line.startswith("#"):
        comment.add(line)
        continue

    char, units = line.split("\t", 1)
    # unit 是单个拆法不同的拆字部件
    for unit in units.split('\t'):
        pinyin_list = pypinyin.pinyin(unit.split(), style=pypinyin.Style.NORMAL, heteronym=True)
        for pinyin in product(*pinyin_list):
            PINYIN = "'".join(filter(is_not_empty, pinyin))
            if not pattern.match(PINYIN):
                error_line = line + ' >> ' + PINYIN
                error.add(error_line)
                continue
            add_weighted_entry(yaml, char.strip(), PINYIN, weights)

with open(src_dict_head_file, 'r', encoding='utf-8') as f:
    extra_content = f.read()

with open(des_error_file, 'w', encoding='utf-8') as f:
    error_info = ("\n".join(sorted(error)))
    
    exclude_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' \n\r\t")
    counter = collections.Counter()
    
    f.write("# 无法注音的汉字\t出现的次数\n")
    for line in error_info.splitlines():
        if '>>' in line:
            _, after_part = line.split('>>', 1)
            for char in after_part:
                if char not in exclude_chars:
                    counter[char] += 1
    for char, count in counter.most_common():
        f.write(f"{char}\t{count}\n")
    f.write("\n# 详细错误信息\n")
    f.write(error_info)
    print(f"错误信息已写入 {des_error_file}")

with open(src_dict_append_file, 'r', encoding='utf-8') as f:
    add = f.read()

add_append_entries(yaml, comment, add, weights)

sorted_yaml = [line for _, line in sorted(yaml, reverse=True)]

# 此文件用于进一步的转换
with open(des_dict_file,"w",encoding='utf-8') as f:
    f.write("\n".join(sorted(comment)) + "\n" + "\n".join(sorted_yaml) + "\n")

with open(des_pinyin_dict_file,"w",encoding='utf-8') as f:
    f.write(extra_content + '\n'  + HEADER + "\n".join(sorted(comment)) + "\n" + "\n".join(sorted_yaml) + "\n")
    print(f"拼音字典已写入 {des_pinyin_dict_file}")
