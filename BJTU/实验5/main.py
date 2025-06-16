import re


def extract_words(text):
    """
    从给定的文本内容中提取所有单词
    :param text: 文本内容
    :type text: str
    :return: list, 提取的单词列表
    """
    words = re.findall(r'\b\w+\b', text.lower())
    return words


def count_words(words):
    """
    统计单词出现的频率
    :param words: 单词列表
    :type words: list
    :return: dict: 单词及其出现次数的字典
    """
    word_count = {}
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


try:
    with open('article.txt', 'r', encoding='utf-8') as file:
        content = file.read()
except FileNotFoundError:
    print("错误：文件 'article.txt' 不存在。请确保文件在当前目录下。")
    exit(1)
words = extract_words(content)
word_count = count_words(words)
# 按照单词出现次数排序
for word, count in sorted(word_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{word}: {count}")
