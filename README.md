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
bash rime-install mirtlecn/rime-radical-pinyin

# 双拼请额外执行
# 请将命令末尾（schema=?）替换为你想要安装的双拼名称，支持
#   - flypy（小鹤双拼）
#   - double_pinyin（自然码双拼）
#   - mspy（微软双拼）
#   - sogou（搜狗双拼）
#   - abc（智能 ABC 双拼）
#   - ziguang（紫光双拼

bash rime-install mirtlecn/rime-radical-pinyin@master:config:schema=flypy
```

<details>

<summary>只使用小鹤双拼 --></summary>

```bash
bash rime-install mirtlecn/rime-radical-pinyin:flypy
```

</details>


### 2. 手动安装

前往本仓库的 Release 界面，下载 `radical_pinyin.zip`，解压后复制到 Rime 用户目录。

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

## 作为辅助码（反查候选）挂载

可以自行生成带辅码的词典，亦或者借助 lua。

本库提供了一个辅助码 lua 可供尝试，请参考 [search.lua](search.lua.md)。

## 注音

- 普通汉字：读本音
- 笔画：笔画读音（勾，点，横，竖，撇，捺，折）
- 生僻字：为常用的独立汉字的且不为笔画的，保留生僻字读音
- 多音字：一般保留最常用读音，都常用则同时保留
- 无读音的偏旁部首：使用学前教育时使用的助记法标音
- （部分汉字可能包含了其异体字的拆分方式）

以上读音可以同时存在，因而一个部件可能有多种拼法。

- 冂（本音 jiong、助记 tong）
- 一（本音 yi、笔画 heng）

词典文件的开头部分列出了一些注音可供参考。

## 反查带声调注音

本项目提供了三个编译好的带声调的词典可供取用，来源于 pinyin-data 项目。

plum 安装:

```bash
bash rime-install mirtlecn/rime-radical-pinyin:extra
```

若要手动安装，请前往 Release 界面下载 extra.zip，解压后，在其中的 build 文件夹内有以下三个文件：

- `zdict.reverse.bin`：汉典注音，无音者注 `n/a`（推荐）
- `kMandarin.reverse.bin`: 单字注最常用的一到两个读音（推荐）
- `pinyin.reverse.bin`: 单字注所有可能的读音（会包含异体字、通假字等音）

下载复制进 build 目录后。更改提示码词典指向它们，如下图所示：

```yaml
radical_reverse_lookup:
    dictionary: zdict # 提示码词表
    # dictionary: kMandarin
    # dictionary: pinyin
```

## 问题

开启用户词典后，双拼状态下，会产生未被算法转化的含引号全拼编码，出现一些意外候选。简单的解决办法是设定 enable_user_dict 为 false（已经在本方案设定，仍需在主方案中设定）。

也可以自行将词典直接转化为双拼编码，`build` 分支下有示例脚本，Release 界面有生成的词典。

## Credit

词典数据：

- [汉字拆字字典](https://github.com/mirtlecn/chaizi-re)（@開放詞典 / henrysting / Mirtle CC BY-SA 4.0），转换而成
- https://gitlab.chise.org/CHISE/ids （GPLv2 or later）
- https://github.com/yi-bai/ids （MIT）

除在文件内另行注明的，本仓库文件均发布在 GPLv3 许可协议下。
