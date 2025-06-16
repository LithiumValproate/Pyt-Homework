# -*- coding: utf-8 -*-
"""
文件处理、词频统计与词云生成

功能描述:
1.  读取文本文件内容。
2.  使用 jieba 库对中文文本进行分词。
3.  统计分词后的词频。
4.  将词频统计结果写入 CSV 文件。
5.  根据词频生成词云图像。
6.  分析多个文本的关键词并进行比较。

运行前准备:
+ 确保已安装必要的库:
  pip install jieba wordcloud pandas matplotlib
+ **关键**: 准备一个中文字体文件 (如 msyh.ttf 等), 并将其路径更新到脚本中的 `font_file` 变量。
"""

import jieba
import jieba.analyse
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import os


# --- 辅助函数定义 ---

def read_file(file_p, encoding='utf-8'):
    """
    从指定文件路径读取内容。

    :param file_p: 文件的完整路径
    :type file_p: str

    :param encoding: 文件编码，默认为 utf-8
    :type encoding: str

    :return: 文件内容，如果文件不存在或读取错误则返回 None
    :rtype: str
    """
    print(f'正在读取文件: {file_p}')
    if not os.path.exists(file_p):
        print(f'错误: 文件 "{file_p}" 不存在。')
        return '这是一个示例文本，因为原始文件未找到。\n全世界都认为汉语是世界上最美丽的语言之一。'
    try:
        with open(file_p, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        # 如果 UTF-8 解码失败，尝试使用 GBK 编码
        print(f"使用 '{encoding}' 编码读取文件 '{file_p}' 失败，尝试 'gbk'...")
        try:
            with open(file_p, 'r', encoding='gbk') as f:
                print(f"成功使用 'gbk' 编码读取文件。")
                return f.read()
        except Exception as e:
            print(f"尝试使用 'gbk' 编码读取文件时也出错: {e}")
            return None
    except Exception as e:
        print(f'读取文件 "{file_p}" 时出错: {e}')
        return None


def write_file(file_p, data):
    """
    将词频数据写入 CSV 文件。

    :param file_p: 要保存的 CSV 文件的路径
    :type file_p: str

    :param data: 包含 (词, 频率) 元组的列表
    :type data: list
    """
    print(f'正在将词频数据写入到: {file_p}')
    df = pd.DataFrame(data, columns=['词语', '频率'])
    df.to_csv(file_p, index=False, encoding='utf-8-sig')
    print(f'写入完成，文件已保存至: {os.path.abspath(file_p)}')


def process_text_n_generate_wordcloud(text, stopwords_p, font_p, outputCsv_p, outputWordCloud_p):
    """
    处理文本、统计词频并生成词云。

    :param text: 待处理的文本
    :type text: str

    :param stopwords_p: 停用词文件路径
    :type stopwords_p: str

    :param font_p: 用于生成词云的中文字体路径
    :type font_p: str

    :param outputCsv_p: 输出 CSV 文件的路径
    :type outputCsv_p: str

    :param outputWordCloud_p: 输出词云图片的路径
    :type outputWordCloud_p: str
    """
    if not text:
        print('输入文本为空，已跳过处理。')
        return

    stopwords = set()
    if os.path.exists(stopwords_p):
        with open(stopwords_p, 'r', encoding='utf-8') as f:
            stopwords = {line.strip() for line in f}
    print(f'加载了 {len(stopwords)} 个停用词。')

    text = re.sub(r'[^\u4e00-\u9fa5]+', '', text)
    words = [word for word in jieba.cut(text) if len(word) > 1 and word not in stopwords]

    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    word_counts_list = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    if word_counts_list:
        write_file(outputCsv_p, word_counts_list)
    else:
        print("没有可供写入的词频数据。")

    print(f'正在生成词云图像: {outputWordCloud_p}')
    if not os.path.exists(font_p):
        print(f"!!! 警告: 字体文件 '{font_p}' 未找到。词云中的中文可能无法正确显示。")
        print('!!! 请务必将一个有效的中文字体文件 (如 simhei.ttf) 放置在相同目录下或提供其完整路径。')
        return

    if not word_counts:
        print("没有词频数据，无法生成词云。")
        return

    wc = WordCloud(
        font_path=font_p,
        background_color='white',
        width=800,
        height=600,
        max_words=100,
        margin=5
    ).generate_from_frequencies(word_counts)

    plt.figure(figsize=(10, 8), facecolor=None)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)

    plt.savefig(outputWordCloud_p)
    print(f'词云生成并保存成功，文件已保存至: {os.path.abspath(outputWordCloud_p)}')
    plt.show()


def analyze_accident_reports(report_p_list, userDict_p):
    """
    利用 jieba 库分析轨道交通事故报告。

    :param report_p_list: 包含事故报告文件路径的列表
    :type report_p_list: list

    :param userDict_p: 自定义词典的路径
    :type userDict_p: str
    """
    print('\n--- 开始分析事故报告 ---')

    if os.path.exists(userDict_p):
        jieba.load_userdict(userDict_p)
        print(f'已成功加载自定义词典: {userDict_p}')

    # 用于存储每个关键词的来源报告
    keyword_sources = {}
    # 用于存储每个报告提取出的原始关键词列表
    report_specific_keywords = {path: [] for path in report_p_list}

    for path in report_p_list:
        print(f'\n--- 正在分析报告: {path} ---')
        content = read_file(path)
        if content:
            keywords = jieba.analyse.extract_tags(content, topK=10, withWeight=False)
            print('提取的关键词:', '、'.join(keywords) if keywords else '无')

            report_specific_keywords[path] = keywords

            # 记录每个关键词的来源
            for keyword in keywords:
                if keyword not in keyword_sources:
                    keyword_sources[keyword] = []
                keyword_sources[keyword].append(path)

    # --- 动态生成分析总结 ---
    common_keywords = {k for k, v in keyword_sources.items() if len(v) > 1}
    unique_keywords_summary = {}

    for path, keywords in report_specific_keywords.items():
        unique_list = [kw for kw in keywords if kw not in common_keywords]
        if unique_list:
            # os.path.basename 用于从完整路径中只获取文件名
            unique_keywords_summary[os.path.basename(path)] = unique_list[:4]  # 最多显示4个特性词

    print('\n--- 分析总结 (根据程序运行结果生成) ---')
    print('通过比较不同报告的关键词，我们发现了事故原因的一些共性和特性：')

    if common_keywords:
        print(f"  - 共性问题: 在多个报告中都提到了 '{'、'.join(common_keywords)}'，这些可能是需要普遍关注的问题。")
    else:
        print("  - 共性问题: 本次分析未发现贯穿多个报告的共同关键词。")

    if unique_keywords_summary:
        print("  - 特性问题: 各报告也反映了特定事故的独特原因，例如：")
        for path_basename, keywords in unique_keywords_summary.items():
            print(f"    * 报告 '{path_basename}' 突出了 '{'、'.join(keywords)}' 等方面。")

    print("  - 改进建议: 使用自定义词典 (如 '追尾事故', '道岔故障') 可以帮助我们更准确地识别和统计关键信息。")


def create_dummy_files():
    """
    创建脚本运行所需的示例文件，方便直接运行和测试。
    """
    print("--- 正在创建演示所需的示例文件 ---")

    files_to_create = {
        '全世界都认为汉语是婴儿语.txt': '全世界都认为汉语是婴儿语，这种说法是完全错误的。汉语是联合国六种官方工作语言之一，也是世界上使用人数最多的语言。汉语的语法结构、发音系统和汉字书写都博大精深，蕴含着丰富的文化和历史。学习汉语，探索中华文化，是一件非常有意义的事情。',
        'stopwords.txt': '的\n是\n了\n也\n和\n在\n我们\n一个\n这种\n都\n是\n与\n学习\n本次\n导致\n由于\n相关',
        'user_dict.txt': '追尾事故 10 n\n信号系统 10 n\n道岔故障 10 n\n应急预案 10 n',
        'report1.txt': '本次事故的主要原因是信号系统故障，导致列车错误地进入了已被占用的区间，最终发生了追尾事故。相关部门的管理存在疏漏，应急预案未能及时启动。设备维护需要加强，安全意识有待提高。',
        'report2.txt': '由于夜间突降暴雪，道岔被积雪覆盖，引发了道岔故障。尽管操作人员尽力排险，但未能避免列车脱轨。此次事故暴露了我们在恶劣天气下的应急处理能力不足，设备维护也存在问题。',
        'report3.txt': '调查发现，本次安全事故源于人为操作失误，调度员未严格遵守操作规程。同时，设备的日常巡检记录不全，管理上存在漏洞，安全培训不到位。'
    }

    for filename, content in files_to_create.items():
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'已创建示例文件: {filename}')
        else:
            print(f'文件已存在: {filename}')


# --- 主程序入口 ---
if __name__ == '__main__':

    create_dummy_files()

    # --- 任务一：文件读写与词云制作 ---
    print('\n--- 开始执行任务一：文件读写与词云制作 ---')
    text_file_path = '全世界都认为汉语是婴儿语.txt'
    stopwords_file = 'stopwords.txt'

    # !!! ================================================================= !!!
    # !!! 重要提示：请务必修改下面的 `font_file` 变量！                      !!!
    # !!! 常见字体路径参考:                                                 !!!
    # !!! - Windows: 'C:/Windows/Fonts/simhei.ttf' 或 'C:/Windows/Fonts/msyh.ttf'
    # !!! - macOS: '/System/Library/Fonts/PingFang.ttc'
    # !!! ================================================================= !!!
    font_file = '/System/Library/Fonts/Hiragino Sans GB.ttc'

    csv_output_path = '词频统计结果.csv'
    wordcloud_output_path = '词云图像.png'

    article_text = read_file(text_file_path)

    if article_text:
        process_text_n_generate_wordcloud(article_text, stopwords_file, font_file, csv_output_path,
                                          wordcloud_output_path)
    print('--- 任务一执行完毕 ---')

    # --- 任务二：分析轨道交通事故报告 ---
    print('\n--- 开始执行任务二：分析轨道交通事故报告 ---')
    accident_report_files = ['report1.txt', 'report2.txt', 'report3.txt']
    custom_dict_file = 'user_dict.txt'

    analyze_accident_reports(accident_report_files, custom_dict_file)
    print('--- 任务二执行完毕 ---')
