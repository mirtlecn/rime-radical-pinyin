# I copy from another place some years ago but do not remember the original author
"""
define pinyin table
"""
first = {'ch': 'i',
         'sh': 'u',
         'zh': 'v'}

second = {
    'ua': 'x',
    'ei': 'w',
    'e': 'e',
    'ou': 'z',
    'iu': 'q',
    've': 't',
    'ue': 't',
    'u': 'u',
    'i': 'i',
    'o': 'o',
    'uo': 'o',
    'ie': 'p',
    'a': 'a',
    'ong': 's',
    'iong': 's',
    'ai': 'd',
    'ing': 'k',
    'uai': 'k',
    'ang': 'h',
    'uan': 'r',
    'an': 'j',
    'en': 'f',
    'ia': 'x',
    'iang': 'l',
    'uang': 'l',
    'eng': 'g',
    'in': 'b',
    'ao': 'c',
    'v': 'v',
    'ui': 'v',
    'un': 'y',
    'iao': 'n',
    'ian': 'm'
}

# 特殊，只有䪨母，且总长不过 3
# 零声母，单双三䪨母
special = {
    'a': 'aa',
    'ai': 'ai',
    'an': 'an',
    'ang': 'ah',
    'ao': 'ao',
    'e': 'ee',
    'ei': 'ei',
    'en': 'en',
    'er': 'er',
    'o': 'oo',
    'ou': 'ou'
}


def tofly(s: str) -> str:
    """
    传入单汉字的全拼编码，返回双拼编码

    :param s: 全拼编码
    :return: 双拼编码
    """
    new_s = ''
    # 特列情况: 无声母，a, an, ang
    if len(s) <= 3 and s[0] in ['a', 'e', 'o']:
        if s in special.keys():
            return special[s]
        # else:
            # print('未知情况1', s)

    # 一般: 声母 + 䪨母

    # 最长的情况：first+second，例如 chuang = ch + uang
    # 2 位声母 + 最多 4 位韵母
    if s[:2] in first.keys():
        new_s += first[s[:2]]
        # 最多 4 位䪨母
        if s[2:] in second.keys():
            new_s += second[s[2:]]
    # 较短的情况：second+second，例如 h uang, x iang
    # 1 位声母 + 最多 4 位䪨母
    else:
        new_s += s[0]  # 1 位声母
        # 最多 4 位䪨母
        if s[1:] in second.keys():
            new_s += second[s[1:]]
        else:
            new_s += s[1:]

    return new_s
