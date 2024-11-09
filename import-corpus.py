import sys
from collections import Counter, defaultdict

import common

corpus_file = sys.argv[0]
conn = common.init_db()
with open(corpus_file, "r", encoding="utf-8") as f:
    for line in f:
        words = (
            line.lower().translate(str.maketrans("", "", string.punctuation)).split()
        )
        self.word_freq.update(words)
