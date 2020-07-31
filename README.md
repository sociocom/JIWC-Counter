# JIWC-Counter
An automatic tool for getting word counts related to emotions with JIWC dictionary

Requires JIWC-B csv file version 2018 or later as input argument to work.

#### Requirements for JIWC-Counter
1. Install Juman++ (recommended ver.1.02) and pyknp (recommended ver.0.3)\
or\
MeCab (recommended ver.0.996) and mecab-python3 (recommended ver.1.0.1)

2. Install pandas (recommended ver.1.0.1)

#### How to use

1. Basic usage
```
$ python jiwc_counter.py --doc  ~/Documents/Texts/foo.txt --dict ~/Documents/JIWC_dict/JIWC-B_2018.csv
Tokenizing files with jumanpp...
========================================
Total Counts by Category

悲しい/Sad: 7
不安/Anxiety: 31
怒り/Anger: 12
嫌悪感/Disgust: 18
信頼感/Trust: 12
驚き/Surprise: 19
楽しい/Joy: 3
```

2. Printing words from emotion categories
```
$ python jiwc_counter.py --doc  ~/Documents/Texts/foo.txt --dict ~/Documents/JIWC_dict/JIWC-B_2018.csv --print_categ ang anx
Tokenizing files with jumanpp...
========================================
怒り/Anger words:  な, 多い, 中心, し, 消費, 国, 変更, 企業, 事務, 高い, 問題, さ, 

不安/Anxiety words:  大学, 教育, 受け, 社会, 会社, 就職, 生活, 投資, 将来, 資格, 変更, ついて, よる, 給与, 希望, 環境, 面, 少ない, 

========================================
Total Counts by Category

悲しい/Sad: 17
不安/Anxiety: 28
怒り/Anger: 18
嫌悪感/Disgust: 18
信頼感/Trust: 17
驚き/Surprise: 30
楽しい/Joy: 23
```
Words in 'foo.txt' can be printed for emotion categories from the first three categories

3. Printing only 3 words from the category
```
$ python jiwc_counter.py --doc  ~/Documents/Texts/foo.txt --dict ~/Documents/JIWC_dict/JIWC-B_2018.csv --print_categ ang anx --num 3
Tokenizing files with jumanpp...
========================================
怒り/Anger words:  な, 多い, 中心, 

不安/Anxiety words:  大学, 教育, 受け,

========================================
Total Counts by Category

悲しい/Sad: 17
不安/Anxiety: 28
怒り/Anger: 18
嫌悪感/Disgust: 18
信頼感/Trust: 17
驚き/Surprise: 30
楽しい/Joy: 23
```
