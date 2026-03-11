# [RIME](https://rime.im/) 部件拆字 | 拼音输入方案 & 辅码插件

℞ `mirtlecn/rime-radical-pinyin`

[![License: GPL 3.0](https://img.shields.io/badge/license-GPLv3-red)](https://www.gnu.org/licenses/gpl-3.0.txt)
[![GitHub Release](https://img.shields.io/github/v/release/mirtlecn/rime-radical-pinyin)](https://github.com/mirtlecn/rime-radical-pinyin/releases/latest)

<!-- TOC -->

- [简介](#简介)
- [安装](#安装)
    - [1. 东风破 plum](#1-东风破-plum)
    - [2. 手动安装](#2-手动安装)
- [作为反查方案挂载](#作为反查方案挂载)
- [作为辅助码（反查候选）挂载](#作为辅助码反查候选挂载)
- [注音](#注音)
- [反查带声调注音](#反查带声调注音)
- [已知问题](#已知问题)
- [Build & Contribute](#contribute)
- [Credit](#credit)

<!-- /TOC -->

## 简介

用拼音输入一个汉字的每一个组成部分（偏旁、部首等部件），组合拼出字来，例如输入 `wu niao`（敄 鸟）或者 `mao wen niao`（矛 夂 鸟）得 `鹜`。

适配各类双拼方案（例图为小鹤双拼）。

不适于用作输入常用字，适于

- 应用于反查，便于打出不清楚读音的生僻字，演示（`禺+页=颙`，`王+炎=琰`，`讠+益=谥`）：（[配置方法](#作为反查方案挂载) -> ）

![image](res/reverse.gif)

- 用作辅助码，快速找到候选字词（`镓锗砷锡溴氪铷锶钇锆->钅钅石钅氵气钅钅钅钅`）（[配置方法](search.lua.md) -> ）：

![image](res/fuma.gif)

## 安装

### 1. 东风破 [plum](https://github.com/rime/plum)

<details>

<summary>请先安装 /plum/</summary>

```bash
# 请安装 git

cd ~
git clone https://github.com/rime/plum.git
# 使用 plum
cd ~/plum
bash rime-install <recipe_name>
```

</details>
<br>
全拼 / 双拼用户请以下命令按安装：

```bash
# 安装词典文件
bash rime-install mirtlecn/rime-radical-pinyin

# 若使用双拼，请额外执行
# 将命令末尾（schema=?）替换为你想要安装的双拼名称，支持
#   - flypy（小鹤双拼）
#   - double_pinyin（自然码双拼）
#   - mspy（微软双拼）
#   - sogou（搜狗双拼）
#   - abc（智能 ABC 双拼）
#   - ziguang（紫光双拼）
#   - jiajia（拼音加加）

bash rime-install mirtlecn/rime-radical-pinyin:config:schema=flypy
```

如果只使用小鹤双拼，建议使用下面的命令：

```bash
bash rime-install mirtlecn/rime-radical-pinyin:flypy
```

### 2. 手动安装

前往本仓库的 Release 界面，下载 `radical_pinyin.zip`，解压后复制到 Rime 用户目录。

双拼用户请直接修改，或以打补丁的方式修改方案文件的 algebra 的 __include 部分

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
    # __include: radical_pinyin.schema.yaml:/algebra_jiajia
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

词典文件的开头部分列出了一些注音可供参考。

## 反查带声调注音

本项目提供了三个编译好的带声调的词典可供取用，来源于 pinyin-data 项目。

plum 安装:

```bash
bash rime-install mirtlecn/rime-radical-pinyin:extra
```

若要手动安装，请前往 Release 界面下载 extra.zip，解压后，在其中的 build 文件夹内有以下三个文件：

- `kMandarin.reverse.bin`: 单字注最常用的一到两个读音（推荐）
- `zdict.reverse.bin`：注音更全，无音者注 `n/a`
- `pinyin.reverse.bin`: 单字注所有可能的读音（会包含异体字、通假字等音，不推荐）

下载复制进 build 目录后。更改提示码词典指向它们，如下图所示：

```yaml
radical_reverse_lookup:
    dictionary: zdict # 提示码词表
    # dictionary: kMandarin
    # dictionary: pinyin
```

## 已知问题

**问题：** 对于双拼用户，开启用户词典，会产生未被算法转化的含引号全拼编码，出现一些意外候选。（不影响全拼用户）

**解决方案 1：** 请务必设定 enable_user_dict 为 false（已经在本方案设定，仍需在主方案中设定）。

**解决方案 2：** 将词典直接转化为双拼编码，`build` 分支下有示例脚本，Release 界面有生成的小鹤双拼词典。

## Contribute

添字、修正拆分等请修改 `src/dict/radical.yaml`。

修改注音，请修改 `src/script/gen_dict.py`。

[源文件和构建说明](./src/README.md)

## Credit

©2026 [Mirtle](https://github.com/mirtlecn)

GPLv3
