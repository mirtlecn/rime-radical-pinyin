"""re is needed if set def is_chinese_char_regex"""
# import re

# Find (^(\S\t)(.*)䖵(.*)$\n)
# Replace $1$2$3囗 禾$4\n

radical = []
yaml = set()
radical_file_path = "dict/radical.yaml"

# def is_chinese_char_regex(char_set):
#     """Checks if a character is likely a Chinese character using a regular expression."""
#     return bool(re.match(r"[\u4e00-\u9fff]", char))

with open(radical_file_path, 'r', encoding='utf-8' ) as f:
    radical = f.readlines()

for line in radical:
    line = line.strip()

    if len(line) == 0 or line.startswith("#"):
        yaml.add(line)
        continue
        # continue

    char, units = line.split(None, 1)
    if (
        char == "□"
        or len(char) != 1               # Ensures char is only one character
        # or not is_chinese_char_regex(char)    # Checks if char is a valid Chinese character
        # or char in units               # Checks if units contains the character
        # or len(units) == 1
        or not units
        ):
        print('\033[91m' + line + ' >> ' + char + '\033[0m')
        raise ValueError("Format error!")
        # continue

    # unit 是单个拆法不同的拆字部件
    for unit in units.split('\t'):
        for i in unit.split():
            if len(i) > 1:
                print('\033[91m' + line + ' >> ' + unit + '\033[0m')
                raise ValueError("Format error!")
        UNIT = ' '.join(unit.split())
        item = f"{char.strip()}\t{UNIT}"
        yaml.add(item)

with open(radical_file_path,"w",encoding='utf-8') as f:
    f.write("\n".join(sorted(yaml)) + '\n')
    print(f"格式检查通过，已写入 {radical_file_path}")
