import re
import sys
from collections import Counter, defaultdict

import common

file_path = sys.argv[1]
conn = common.init_db()


def count_words(file_path):
    # Dictionary to keep counts of each word, separate for lowercase and title case.
    word_counts = defaultdict(int)

    # Dictionary to track context to help resolve ambiguous title-case words at the start of sentences.
    title_case_tracking = defaultdict(lambda: {"title": 0, "lower": 0})

    # Open and read the file line by line
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Split line into sentences
            sentences = re.split(r"(?<=[.!?])\s+", line.strip())
            for sentence in sentences:
                # Split sentence into words
                words = re.findall(r"\b\w+\b", sentence)
                if not words:
                    continue

                # Track the first word separately for ambiguity checking
                first_word = words[0]
                if first_word.istitle():
                    # If the word appears frequently in lowercase elsewhere, assume lowercase
                    if (
                        title_case_tracking[first_word.lower()]["lower"]
                        > title_case_tracking[first_word.lower()]["title"]
                    ):
                        word_counts[first_word.lower()] += 1
                        title_case_tracking[first_word.lower()]["lower"] += 1
                    else:
                        word_counts[first_word] += 1
                        title_case_tracking[first_word.lower()]["title"] += 1
                else:
                    # Normal lowercase word
                    word_counts[first_word.lower()] += 1
                    title_case_tracking[first_word.lower()]["lower"] += 1

                # Process remaining words in the sentence normally
                for word in words[1:]:
                    if word.islower():
                        word_counts[word] += 1
                        title_case_tracking[word]["lower"] += 1
                    elif word.istitle():
                        word_counts[word] += 1
                        title_case_tracking[word.lower()]["title"] += 1
                    else:
                        word_counts[word.lower()] += 1  # handle uppercase as lowercase

    return dict(word_counts)


word_counts = count_words(file_path)
print(word_counts)
