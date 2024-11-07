import string
import sys
from collections import Counter, defaultdict


class ContextualAutocompleteProgram:
    def __init__(self, corpus_file, target_file):
        self.corpus_file = corpus_file
        self.target_file = target_file
        self.word_freq = Counter()
        self.bigram_freq = defaultdict(Counter)
        self.prefix_dict = defaultdict(list)

    def build_word_frequency(self):
        """Read the corpus file and build unigram and bigram frequency dictionaries."""
        with open(self.corpus_file, "r", encoding="utf-8") as f:
            previous_word = None
            for line in f:
                words = (
                    line.lower()
                    .translate(str.maketrans("", "", string.punctuation))
                    .split()
                )

                for word in words:
                    self.word_freq[word] += 1
                    if previous_word:
                        self.bigram_freq[previous_word][word] += 1
                    previous_word = word

        # Populate prefix-based dictionary using both unigram and bigram frequencies
        for word in self.word_freq:
            # For each prefix of a word, add the word to the prefix dictionary
            for i in range(1, len(word) + 1):
                prefix = word[:i]
                self.prefix_dict[prefix].append(word)

        # Limit each prefix entry to the 10 most frequent words
        for prefix in self.prefix_dict:
            self.prefix_dict[prefix] = sorted(
                self.prefix_dict[prefix], key=lambda w: -self.word_freq[w]
            )[:10]

    def calculate_keystrokes_saved(self):
        """Simulate typing the target file and calculate keystrokes saved."""
        total_keystrokes = 0
        saved_keystrokes = 0
        previous_word = None

        with open(self.target_file, "r", encoding="utf-8") as f:
            for line in f:
                words = (
                    line.lower()
                    .translate(str.maketrans("", "", string.punctuation))
                    .split()
                )

                for word in words:
                    total_keystrokes += len(word)
                    saved_keystrokes += self.keystrokes_for_word(word, previous_word)
                    previous_word = word

        return total_keystrokes, saved_keystrokes

    def keystrokes_for_word(self, word, previous_word):
        """Calculate keystrokes saved for a given word, considering the previous word context."""
        predictions = self.get_predictions(word, previous_word)

        for i in range(1, len(word) + 1):
            prefix = word[:i]
            if word in predictions.get(prefix, []):
                return len(word) - i  # Keystrokes saved by selecting the word
        return 0  # No savings if the word isn't predicted

    def get_predictions(self, word, previous_word):
        """Get the top 10 predicted words based on prefix and previous word context."""
        predictions = {}
        if previous_word in self.bigram_freq:
            bigram_candidates = self.bigram_freq[previous_word]
            for prefix in set(word[:i] for i in range(1, len(word) + 1)):
                # Get top 10 predictions for this prefix in the context of previous_word
                candidates = sorted(
                    bigram_candidates.keys(), key=lambda w: -bigram_candidates[w]
                )
                predictions[prefix] = candidates[:10]

        # Fallback to unigram predictions if no bigram data is available
        if not predictions:
            for prefix in set(word[:i] for i in range(1, len(word) + 1)):
                predictions[prefix] = self.prefix_dict.get(prefix, [])

        return predictions

    def run(self):
        # Step 1: Build frequency models from corpus
        self.build_word_frequency()

        # Step 2: Calculate keystroke savings for the target file
        total_keystrokes, saved_keystrokes = self.calculate_keystrokes_saved()

        print(f"Total keystrokes without autocomplete: {total_keystrokes}")
        print(f"Keystrokes saved with autocomplete: {saved_keystrokes}")
        print(
            f"Percentage keystrokes saved: {100 * saved_keystrokes / total_keystrokes:.2f}%"
        )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python contextual_autocomplete.py <corpus_file> <target_file>")
        sys.exit(1)

    corpus_file = sys.argv[1]
    target_file = sys.argv[2]

    program = ContextualAutocompleteProgram(corpus_file, target_file)
    program.run()
