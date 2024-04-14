# 本脚本从此项目衍生 https://github.com/maxchang3/rime-chaizi (MIT)"""
"""
pypinyin -> get pinyin
pypinyin_dict -> load custom pinyin data
"""
from datetime import datetime
from itertools import product
import re
import pypinyin
from pypinyin import pinyin, load_phrases_dict
from pypinyin_dict.pinyin_data import kmandarin_8105

radical = []
yaml = set()
comment = set()
pattern = re.compile("^[a-z']+$")
kmandarin_8105.load()
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
    '孱': [['chan2']],
    '𡕩': [['man3']],
    '曰': [['yue1','ri4']],
    '𠙽': [['kuai4']],
    '𦉼': [['la4']],
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

## 如果需要调整字频，注释掉上面一行（sort: original），然后取消注释下面两行

# 简体字频
# vocabulary: essay-zh-hans # 简体字频，需要安装 rime/essay-simp
# max_phrase_length: 1 # 仅调整单字

# 繁体字频
# vocabulary: essay # 繁体字频，需要安装 rime/essay（多数平台预装）
# max_phrase_length: 1 # 仅调整单字
...\n\n'''

def is_not_empty(s):
    "pinyin should not be null or empty"
    return s is not None and s.strip() != ''

with open("dict/radical.yaml", 'r', encoding='utf-8' ) as f:
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
                print('\033[91m' + line + ' >> ' + PINYIN + '\033[0m')
                raise ValueError("error!")
                # continue
            item = f"{char.strip()}\t{PINYIN}"
            yaml.add(item)

with open("info.yaml", 'r', encoding='utf-8') as f:
    extra_content = f.read()

with open("add.yaml", 'r', encoding='utf-8') as f:
    add = f.read()

sorted_yaml = sorted(yaml,reverse=True)

with open("gen/radical.dict.yaml","w",encoding='utf-8') as f:
    f.write("\n".join(sorted(comment)) + "\n" + "\n".join(sorted_yaml) + '\n\n' + add )

with open("gen/radical_pinyin.dict.yaml","w",encoding='utf-8') as f:
    f.write(extra_content + '\n'  + HEADER + "\n".join(sorted(comment)) + "\n" + "\n".join(sorted_yaml) + '\n\n' + add )
