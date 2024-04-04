# RIME 辅助码反查滤镜 search.lua

使用此 lua ，你可以使用其他方案提供的编码反查候选。

其效果类似某些输入法提供的候选内笔画、部件反查。

![image](https://raw.githubusercontent.com/mirtlecn/rime-radical-pinyin/master/res/reverse.gif)

如上图所示，输入十个化学元素的名称。这些汉字大多为生僻字，正常情况下在候选中排序靠后。

借助此 lua ，输入完拼音后，你可以先输入一个引导符号，紧接着输入每个汉字的部首拼音，相关的汉字自动被调整到排序靠前的位置，方便选择。

## 安装与使用

### 一、安装并启用辅助编码的输入方案

此滤镜仅为挂载辅助码的脚本，辅助编码方案和词典需要自行准备。您不需要制作额外的辅助码词典或者码表，只需要像其他 RIME 输入方案一样安装并启用用于辅助检索的方案。

词典不宜过大，仅包含单字为佳。你可以尝试以下方案：

- stroke （五笔画，RIME 预装）
- radical_pinyin （本方案，部件拆字拼音）

你需要启用辅码方案，使之正确编译，即在 default[.custom].yaml 中：

```yaml
schema_list:
    # ...
    - {schema: stroke}
    - {schema: radical_pinyin}
```

你也可以将它们作为主方案的依赖方案挂载主方案下，即在 [xxx].schema.yaml 中：

```yaml
schema:
  dependencies:
    - radical_pinyin
    - stroke
```

### 二、引入 lua

下载 [search.lua](https://github.com/mirtlecn/rime-radical-pinyin/blob/extra/lua/search.lua) 到 RIME 用户目录的 lua 文件夹下。

找到主方案的 filter 列表，在 **`uniquifier` 去重滤镜之前，繁简转换 filter 之后**，添加 `lua_filter@*search` ，如下所示：

```yaml
# example.schema.yaml
engine:
  filters:
    # ...
    - simplifier@simplify
    - lua_filter@*search
    - uniquifier
```

### 三、配置 lua

修改方案配置如下：

```yaml
search:
  schema: radical_pinyin # 指定辅码方案
key_binder:
  search: "`" # 此为辅码引导键
speller:
  alphabet: zyxwvutsrqponmlkjüihgfedcba` # 请将辅码引导键加入到 alphabet 后
```

此时，你应当可以进行辅码检索了。

### 四、使用

正常输入按键，出现候选。

```
nihao ->
你好 拟好 你 尼 妮
```

此时，输入辅码引导键（默认为 <kbd>\`</kbd>，再输入查询的辅码，例如 `ren`

```
nihao`ren ->
你好 你 倪 伲 伱
```

这种情况下，将用辅码匹配单字，若为词组，则匹配第一个字。

<details>

<summary>db 反查支持输入第二个辅码</summary>

您如果使用的是 db 辅码反查（见下一节的解释），还可以接着输入第二个辅码引导键，接着输入辅码，此时将用第二个辅码检索词组的第二个字，或者重复匹配单字。例如

```
yiyi ->
意义 一一 异议 依依 一亿

yiyi`h -> 用 h 匹配第一个字（横）
一一 一亿 一役 一揖 一意

yiyi`h`ren -> h 匹配第一个字，并且 ren 匹配词组的第二个字，或者单字同样含 ren 后候选
一亿 一役 夷 柂
```

其中，`一亿 一役` 为第一个字匹配 `h`，第二个字匹配 `ren` 的候选；而 `夷 柂` 为同时匹配 `h` 和 `ren` 的候选。对于单字而言，第二个辅码使用正则匹配。

```
yi`3`mu -> 匹配第三声，且含 mu 读音部件的字
椅 栺 檥
```

</details>

选字后，如果为词组，辅码将继续存在。如果为单字，辅码将消失（不会跟随上屏）

## 配置

search.lua 还有更多可以定制的参数和配置方法。

```yaml
switch:
  - name: search_single_char # 辅码检索时，是否单字优先
  # reset: 0
    abbrev: [词, 单]
    states: [正常, 单字]
key_binder:
  search: '`'
  bindings:
    - { accept: "Control+s", toggle: search_single_char, when: has_menu } # 按下 Control+s，切换单字优先模式
search:
  tags:
    - abc # 检索特定 tag 的候选，默认为 abc
  # key: '`' # 辅码引导键，优先级低于 key_binder/search 设置，此按键需要加入 speller/alphabet 中。
  show_other_cands: false # 候选不匹配辅助码时，仅将其置后，而非隐藏。
  schema: radical_pinyin # 方案反查，支持经过算法转换后的编码，检索大码表时较慢
  schema_search_limit: 500 # 方案反查单词检索的数量限制，不设置时为 1000，设置为 0 则无限制。大码表（如五笔画 stroke）请设置合理的数值以保证不卡顿。
  wildcard: '~' # db 反查的通配符。此符号需要加入 speller/alphabet 表中。
  db: # db 反查，速度快，仅支持编入字典的硬编码。指定一个或多个 build 目录下的 reverse.bin 文件的文件名。
    - stroke # 指定五笔画作为 db 反查的数据库
    - tone # 指定音调编码作为 db 反查的数据库
  fuma_format: # 辅码用于检索前，经过 fuma_format 的转换
    - xlit/ABCD/1234 # 此规则作用：用户输入 ni`A 得到所有读第一声 ni 的候选（须配合音调编码反查）
  # input2code_format: # 将输入码转化为编码的规则，检测到此规则，脚本将尝试强制将提交的词汇写入用户词库，推入输入历史。当前仅支持两键定长码方案（如双拼），其他方案请不要使用。
    # -
speller:
  alphabet: zyxwvutsrqponmlkjüihgfedcba`~ # 字母表中需要在原有配置后，添加辅码引导键（search/key）、通配键（search/wildcard 如有）
```

## 具体案例

你可以直接在 filter 处直接指定辅码方案（等同于 `schema: radical_pinyin`）：

```yaml
engine:
  filters:
    # ...
    - lua_filter@*search@radical_pinyin
```

你可以指定方案反查。该辅码工作方式为以码查字（检索 table.bin、prism.bin），支持经过算法转化的编码：大词库（生成的 prism 和 table 大小超过 1 MB）请指定合理的检索条目限制。

```yaml
search:
  show_other_cands: true # 设置为 true 则仅执行排序，而不过滤掉不符合辅码的候选
  schema: radical_pinyin # 方案反查，建议小词库使用；
  schema_search_limit: 1000 # 方案反查条目限制，越大越精确越卡
```

数据库反查，以字查码（检索 reverse.bin），仅支持查编入词典（dict.yaml）的编码。消耗小，速度快，支持指定多个数据库。

```yaml
search:
  show_other_cands: true
  wildcard: "-" # 通配符，仅支持 db 反查，需要加入 alphabet 中
  db: # 数据库反查，一个列表写一个，为 build 目录下 reverse.bin 前面的名字（一般为方案所用词典的词典名）
    - stroke
    - wubi98
```

如果你不清楚 （table.bin、prism.bin、reverse.bin）的区别，以下是简单判断使用 `schema` 还是 `db` 辅码反查的方法：

- 打开辅码方案所用的词典（dict.yaml）文件，你应当可以看到每行都是「词 \<tab\> 码」的格式；
```
你  ni
好  hao
二  hh
三  heng'heng'heng
```
- 这里看到的码就是能用于 db 辅码反查的编码：如果你能 **完全** 按照此处看到的编码打出方案里的字来，就用 db 反查；
- 反之，用 schema 反查。

举例来说：

- stroke 五笔画方案字典内容编码都是 hspnz，用这五个字母完全可以拼出字来，因而采用 db 方式；
- 双拼方案，字典中是全拼的编码，但完全按照字典内的编码是打不出对应的字来的，因为这些编码在双拼方案中被转化为了双拼，因而应当使用 schema 的辅码方案。

本项目 radical_pinyin 同理，不做词库更改的情况下，应当在 schema 处指定。

当然，schema 和 db 可以同时指定，以下写法将同时使用笔画和部件辅码：

```yaml
search:
  schema: radical_pinyin
  show_other_cands: false
  wildcard: "-"
  db:
    - stroke
```

```
-- Copyright (C) [Mirtle](https://github.com/mirtlecn)
-- License: CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/)
-- Extending my gratitude to https://github.com/HowcanoeWang/rime-lua-aux-code for inspiring and serving as a valuable reference for this lua
```
