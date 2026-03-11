# 汉字拆字字典 & Radical 词典构建脚本

## 拆分规则

`dict/radical.yaml` 内每一行为某个汉字的一种拆法。

```yaml
<汉字><tab><部件甲><space><部件乙>……
```

汉字 | 拆法 (一) | 拆法 (二) | 拆法 (三)
--- | -------- | -------- | --------
拆 | 手 斥 | 扌 斥 | 才 斥
字 | 宀 子
驠 | 馬 燕
鳢 | 鱼 豊
馦 | 香 兼
覗 | 司 見
馫 | 香 香 香
靐 | 雷 雷 雷

井号开头的行为注释行，方便脚本处理。

拆字时以容易打出来的字为先，然后尽量列出其余所有不同拆法，包括正确部首和部件（若包含于统一汉字表内）和异体字。

## Build & Contribute

构建 rime-radical-pinyin 词典：

```bash
# Python 3 环境
git clone https://github.com/mirtlecn/rime-radical-pinyin.git
cd src # 工作目录在 src
make
```

文件说明：

- `dict/radical.yaml`: 拆字源数据，如需添加新子，请修改该文件
- `todo.yaml`：由脚本生成。包含未能注音的字，一般是拆分出的部件无法识别，需要人工校正

## History

- 合入了部分 ids 数据；
- 合并了繁简两份码表，合入了 [henrysting](https://github.com/henrysting/chaizi/) 的添补；
- 加入了大量未收录的常用字，日常缺字补漏；
- 更正、添加了大量拆法；
- 删除了编码不正确的汉字。

## Credits

GPLv3

Thanks to:

- https://github.com/kfcd/chaizi（CC-BY 3.0）
- https://gitlab.chise.org/CHISE/ids （GPLv2 or later）
- https://github.com/yi-bai/ids （MIT）
