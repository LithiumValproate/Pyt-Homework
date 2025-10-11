import re

text = input()
words = re.findall(r'[A-Za-z]+', text)
if not words:
    print('No words found')
else:
    max_len = max(len(w) for w in words)
    longest_words = [w for w in words if len(w) == max_len]
    print(' '.join(longest_words))
