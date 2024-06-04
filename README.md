# [RIME](https://rime.im/) 部件拆字 | 拼音输入方案

配方：℞ rime-radical-pinyin

码表：[汉字拆字字典](https://github.com/mirtlecn/chaizi-re)

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![GitHub Release](https://img.shields.io/github/v/release/mirtlecn/rime-radical-pinyin)](https://github.com/mirtlecn/rime-radical-pinyin/releases/latest)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/mirtlecn/rime-radical-pinyin/build.yml)](https://github.com/mirtlecn/rime-radical-pinyin/actions/workflows/build.yml)

<!-- TOC -->

- [简介](#简介)
- [安装](#安装)
    - [1. 东风破 plum](#1-东风破-plum)
    - [2. 手动安装](#2-手动安装)
- [作为反查方案挂载](#作为反查方案挂载)
- [作为辅助码（反查候选）挂载](#作为辅助码反查候选挂载)
- [注音](#注音)
- [反查带声调注音](#反查带声调注音)
- [已知问题](#问题)
- [Credit](#credit)

<!-- /TOC -->

## 简介

用拼音输入一个汉字的每一个组成部分（偏旁、部首等部件），组合拼出字来，例如输入 `wu niao`（敄 鸟）或者 `mao wen niao`（矛 夂 鸟）得 `鹜`。

适配双拼（例图为小鹤双拼）。

不适于用作输入常用字的主要翻译器。

可以应用于反查，便于打出不清楚读音的生僻字，演示（`禺+页=颙`，`王+炎=琰`，`讠+益=谥`）：

![image](res/reverse.gif)

可以用作辅助码，快速找到候选字词（`镓锗砷锡溴氪铷锶钇锆->钅钅石钅氵气钅钅钅钅`）（使用请参考 [search.lua](search.lua.md)）：

![image](res/fuma.gif)

## 安装

### 1. 东风破 [plum](https://github.com/rime/plum)

<details>

<summary>安装 /plum/ </summary>

```bash
# install git first

cd ~
git clone https://github.com/rime/plum.git

# use plum install stroke to default location
cd ~/plum
bash rime-install stroke

# or install to a sepcific folder
cd ~/plum
rime_dir='D:/RIME' bash rime-install stroke
```

</details>

```bash
# 安装词典文件
bash rime-install mirtlecn/rime-radical-pinyin@v1

# 双拼请额外执行
# 请将命令末尾（schema=?）替换为你想要安装的双拼名称，支持
#   - flypy（小鹤双拼）
#   - double_pinyin（自然码双拼）
#   - mspy（微软双拼）
#   - sogou（搜狗双拼）
#   - abc（智能 ABC 双拼）
#   - ziguang（紫光双拼

bash rime-install mirtlecn/rime-radical-pinyin@v1:config:schema=flypy
```

<details>

<summary>只使用小鹤双拼 --></summary>

```bash
bash rime-install mirtlecn/rime-radical-pinyin@v1:flypy
```

</details>


### 2. 手动安装

前往本仓库的 Release 界面，找到最新的 1.x 的 tag，下载 `radical_pinyin.zip`，解压后复制到 Rime 用户目录。

双拼用户请直接或以打补丁的方式修改方案文件的 algebra 的 __include 部分

补丁示例：

```yaml
# radical_pinyin.custom.yaml
patch:
  speller/algebra:
    __include: radical_pinyin.schema.yaml:/algebra_flypy
    # __include: radical_pinyin.schema.yaml:/algebra_double_pinyin
    # __include: radical_pinyin.schema.yaml:/algebra_mspy
    # __include: radical_pinyin.schema.yaml:/algebra_abc
    # __include: radical_pinyin.schema.yaml:/algebra_ziguang
    # __include: radical_pinyin.schema.yaml:/algebra_sogou
```

## 作为反查方案挂载

在主要输入方案或其补丁（注意使用补丁语法，与下面所示不同）的如下部分写入信息：

使用 `reverse_lookup_translator`:

```yaml
schema:
  dependencies:
    - radical_pinyin

engine:
  translators:
    - reverse_lookup_translator

reverse_lookup:
  dictionary: radical_pinyin
  enable_completion: true
  prefix: "u"
  tips:〔拆〕

recognizer:
  patterns:
    reverse_lookup: "u[a-z;]*?$"
```

**或者**使用 `reverse_lookup_filter`：

```yaml
# apply to example.schema.yaml
schema:
    dependencies:
        - radical_pinyin
engine:
    segmentors:
        - affix_segmentor@radical_lookup
    translators:
        - table_translator@radical_lookup
    filters:
        - reverse_lookup_filter@radical_reverse_lookup
radical_reverse_lookup:
    tags: [ radical_lookup ]
    overwrite_comment: true
    dictionary: example # 提示码词表
    comment_format:
        - xform/^/(/
        - xform/$/)/
radical_lookup:
    tag: radical_lookup
    dictionary: radical_pinyin
    enable_sentence: false
    enable_user_dict: false
    prefix: '~'
    tips: "[拆字]"
    # closing_tips:
    suffix: "'"
    comment_format:
        - erase/^.*$//
recognizer:
    patterns:
        radical_lookup: "~[a-z]+'?$"
```

## Credit

字典由 [汉字拆字字典](https://github.com/mirtlecn/chaizi-re)（@開放詞典 / henrysting / Mirtle CC BY-SA 4.0），转换而成。

除在文件内另行注明的，本仓库文件均发布在 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 许可协议下。
