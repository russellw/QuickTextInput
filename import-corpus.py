import re
import sys
from collections import Counter, defaultdict

import common

file_path = sys.argv[1]

lower_words = set()
with open("words_alpha.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip()
        if line.islower():
            lower_words.add(line)

conn = common.init_db()


# Dictionary to keep counts of each word, separate for lowercase and title case.
word_counts = defaultdict(int)


# Open and read the file line by line
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        for word in re.findall(r"\b\w+\b", line):
            if not word.isalpha():
                continue
            lo = word.lower()
            if lo in lower_words:
                word = lo
            word_counts[word] += 1
print(len(word_counts))

cursor = conn.cursor()
for word, count in word_counts.items():
    cursor.execute(
        """
    INSERT INTO words (word, count) 
    VALUES (?, 1)
    ON CONFLICT(word) DO UPDATE SET count = count + 1
    """,
        (word,),
    )
