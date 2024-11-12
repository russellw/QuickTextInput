import argparse
import os
import re
import sqlite3
import sys
from collections import defaultdict

import common

# Set up argparse
parser = argparse.ArgumentParser(
    description="Open an SQLite database and import a text file."
)
parser.add_argument("text_file", type=str, help="Path to the text file to import")
parser.add_argument(
    "--db",
    type=str,
    default=None,
    help="Path to the SQLite database file (default: ~/Documents/QuickTextInput.db)",
)

args = parser.parse_args()

# Determine the database path
if args.db:
    db_path = args.db
else:
    # Default file path
    user_profile = os.environ["USERPROFILE"]
    documents_dir = os.path.join(user_profile, "Documents")
    db_path = os.path.join(documents_dir, "QuickTextInput.db")

# Path to the text file to import
file_path = args.text_file

lower_words = set()
with open("words.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip()
        if line.islower():
            lower_words.add(line)

# Connect to database
conn = common.init_db(db_path)

# Dictionary to keep counts of each word, separate for lowercase and title case.
word_counts = defaultdict(int)

# Open and read the file line by line
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        for word in re.findall(r"\b\w+\b", line):
            if not word.isalpha():
                continue
            if len(word) == 1 and word.islower():
                continue
            lo = word.lower()
            if lo in lower_words:
                word = lo
            word_counts[word] += 1
print(len(word_counts))

with conn:
    cursor = conn.cursor()
    for word, count in word_counts.items():
        cursor.execute(
            """
            INSERT INTO words (word, count)
            VALUES (?, ?)
            ON CONFLICT(word) DO UPDATE SET count = count + ?
            """,
            (word, count, count),
        )
